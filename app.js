import { studyPlan } from "./progress.js?v=1";
import { connectAccount } from "./account.js?v=1";

const ui = Object.fromEntries(Array.from(document.querySelectorAll("[id]"), (element) => [element.id, element]));
const deckLabels = { all: "All cards", revision: "Revision", trigonometry: "Trig rules", review: "To review", study: "Study next" };
const topicHues = {
  differentiation: 155, sequences: 255, logarithms: 305, integration: 60, algebra: 20, modelling: 200,
  triangles: 100, graphs: 230, identities: 330, angles: 40, equations: 175, "trig-calculus": 280,
};
const topicsDialog = ui["topics-dialog"];
const mobileLayout = window.matchMedia("(max-width: 720px)");
const referenceLabels = {
  recall: "Recall for the exam",
  booklet: "In the formula booklet",
};
const mathOptions = {
  macros: { "\\cosec": "\\operatorname{cosec}" },
  throwOnError: false,
  trust: false,
};
const pageParams = new URLSearchParams(window.location.search);

let cards = [];
let questionCards = [];
let topics = new Map();
let progress = new Map();
let queue = [];
let activeDeck = "all";
let activeTopic = "all";
let position = 0;
let answerVisible = false;
let questionMode = pageParams.get("mode") === "questions";
let questionRoundFinished = false;
let displayedQuestion;
const questionAttempts = new Map();

function appendMath(element, value, standalone = true) {
  const segments = value.split(/(\$[^$]+\$)/g);
  const displayMode = standalone && segments.length === 3 && segments[0] === "" && segments[2] === "";
  if (displayMode) element.classList.add("formula");
  for (const segment of segments) {
    if (!segment) continue;
    if (segment.startsWith("$") && segment.endsWith("$") && window.katex) {
      const math = document.createElement("span");
      window.katex.render(segment.slice(1, -1), math, { ...mathOptions, displayMode });
      element.append(math);
    } else {
      element.append(document.createTextNode(segment));
    }
  }
}

function mathLines(lines, className) {
  return lines.map((line) => {
    const element = document.createElement("span");
    element.className = className;
    appendMath(element, line);
    return element;
  });
}

function availableCards() {
  return questionMode ? questionCards : cards;
}

function matchesDeck(card) {
  if (activeDeck === "all") return true;
  if (activeDeck === "review") return progress.get(card.id)?.rating === "review";
  return topics.get(card.topic).collection === activeDeck;
}

function renderProgress() {
  const available = availableCards();
  const known = available.filter((card) => progress.get(card.id)?.rating === "known").length;
  const review = available.filter((card) => progress.get(card.id)?.rating === "review").length;
  const plan = studyPlan(available, progress);
  ui["count-all"].textContent = available.length;
  ui["count-review"].textContent = review;
  ui["known-count"].textContent = known;
  ui["study-next"].disabled = !plan.queue.length;
  ui["study-next-label"].textContent = plan.queue.length ? "Study next" : "All caught up";
  ui["study-next-count"].textContent = plan.reviewCount ? plan.reviewCount + " due" : plan.queue.length ? plan.queue.length + " new" : "";
}

function useProgress(next, accountChanged) {
  progress = next;
  if (!cards.length) return;
  renderProgress();
  if (activeDeck === "study" && accountChanged) {
    resetQueue();
    renderCard();
  }
  if (activeDeck === "review" && (accountChanged || !questionMode)) {
    const previousCard = queue[position];
    const previousFace = answerVisible;
    resetQueue();
    const currentPosition = queue.indexOf(previousCard);
    if (currentPosition !== -1) {
      position = currentPosition;
      answerVisible = previousFace;
    }
    renderCard();
  }
}

function renderTopics() {
  for (const topic of topics.values()) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "topic-button";
    button.dataset.deck = topic.collection;
    button.dataset.topic = topic.id;
    button.style.setProperty("--hue", topicHues[topic.id] ?? 155);

    const dot = document.createElement("span");
    dot.className = "topic-dot";
    dot.setAttribute("aria-hidden", "true");
    const name = document.createElement("span");
    name.className = "topic-name";
    name.textContent = topic.title;
    const count = document.createElement("span");
    count.className = "topic-count";
    button.append(dot, name, count);
    ui[topic.collection + "-topics"].append(button);
    ui["review-topic"].add(new Option(topic.title, topic.id));
  }
}

function renderMode() {
  ui["question-mode"].setAttribute("aria-pressed", String(questionMode));
  ui["flashcard-mode"].setAttribute("aria-pressed", String(!questionMode));
  ui["all-deck-label"].textContent = questionMode ? "All questions" : deckLabels.all;
  ui.practice.setAttribute("aria-label", questionMode ? "Maths questions practice" : "Flashcard practice");
  ui.practice.classList.toggle("question-mode", questionMode);
  ui.flashcard.hidden = questionMode;
  ui["flashcard-actions"].hidden = questionMode;
  ui["question-card"].hidden = !questionMode;

  const available = availableCards();
  for (const button of ui.library.querySelectorAll("[data-topic]")) {
    button.querySelector(".topic-count").textContent = available.filter((card) => card.topic === button.dataset.topic).length;
  }
}

function changeMode(showQuestions) {
  if (questionMode === showQuestions) return;
  const card = queue[position];
  questionMode = showQuestions;

  const url = new URL(window.location.href);
  if (questionMode) url.searchParams.set("mode", "questions");
  else url.searchParams.delete("mode");
  history.replaceState(history.state, "", url);

  renderMode();
  if (!cards.length) return;
  renderProgress();
  resetQueue();
  if (queue.includes(card)) position = queue.indexOf(card);
  renderCard();
}

function renderQuestion(card) {
  let attempt = questionAttempts.get(card.id);
  if (!attempt) {
    const options = shuffled(card.choices.map((text, index) => ({ text, correct: index === 0 })));
    attempt = { options, wrong: new Set(), outcome: null, firstCorrect: null };
    questionAttempts.set(card.id, attempt);
  }

  const optionList = ui["question-options"];
  if (displayedQuestion !== attempt) {
    displayedQuestion = attempt;
    ui["question-prompt"].replaceChildren();
    appendMath(ui["question-prompt"], card.front, false);
    optionList.replaceChildren(...attempt.options.map((option, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "question-option";
      button.dataset.choice = index;
      const letter = document.createElement("span");
      letter.className = "option-letter";
      letter.setAttribute("aria-hidden", "true");
      const text = document.createElement("span");
      text.className = "option-text";
      appendMath(text, option.text, false);
      button.append(letter, text);
      return button;
    }));
  }

  for (const [index, button] of Array.from(optionList.children).entries()) {
    const correct = attempt.outcome && attempt.options[index].correct;
    const wrong = attempt.wrong.has(index);
    button.dataset.result = correct ? "correct" : wrong ? "wrong" : "";
    button.setAttribute("aria-disabled", String(Boolean(attempt.outcome) || wrong));
    button.firstElementChild.textContent = correct ? "✓" : wrong ? "×" : "ABCD"[index];
  }

  let message = attempt.wrong.size ? "Try another answer." : "";
  if (attempt.outcome === "revealed") message = "Answer shown. It’s on your review list.";
  if (attempt.outcome === "correct") message = attempt.firstCorrect ? "Correct." : "Correct. It’s on your review list.";
  ui["question-feedback"].textContent = message;
  ui["question-feedback"].dataset.outcome = attempt.outcome ?? "";
  ui["reveal-question"].hidden = Boolean(attempt.outcome);
  ui["question-explanation"].hidden = !attempt.outcome;
  if (attempt.outcome) ui["question-explanation"].replaceChildren(...mathLines(card.back, "answer-line"));
}

function answerQuestion(choiceIndex) {
  const card = queue[position];
  if (!questionMode || !card || questionRoundFinished) return;
  const attempt = questionAttempts.get(card.id);
  if (!attempt || attempt.outcome || attempt.wrong.has(choiceIndex)) return;
  const revealed = choiceIndex === undefined;
  const correct = !revealed && attempt.options[choiceIndex].correct;
  let saved = true;
  if (attempt.firstCorrect === null) {
    attempt.firstCorrect = correct;
    saved = account.rate(card.id, correct ? "known" : "review");
    renderProgress();
  }
  if (revealed || correct) attempt.outcome = revealed ? "revealed" : "correct";
  else attempt.wrong.add(choiceIndex);
  renderQuestion(card);
  if (!saved) ui["question-feedback"].textContent += " Progress couldn’t be saved on this device.";
  if (revealed) ui["question-feedback"].focus({ preventScroll: true });
}

function renderCard(announcement = "") {
  const card = questionRoundFinished ? undefined : queue[position];
  const topic = topics.get(card?.topic ?? activeTopic);
  ui.practice.hidden = !card;
  ui.empty.hidden = Boolean(card);
  const deckName = questionMode && activeDeck === "all" ? "All questions" : deckLabels[activeDeck];
  ui["collection-label"].textContent = deckName;
  ui["deck-title"].textContent = topic?.title ?? deckName;
  ui["position-label"].textContent = card ? (position + 1) + " of " + queue.length : "";
  ui.shuffle.disabled = queue.length < 2;
  if (!card) {
    let message = questionMode ? "There are no questions for this topic." : "There are no cards for this topic in this deck.";
    if (activeDeck === "study") {
      message = ui["study-next"].disabled
        ? "You’re caught up. Come back when more cards are due."
        : "You’ve finished this round. Use Study next when you’re ready for another.";
    }
    if (activeDeck === "review" && activeTopic === "all") {
      message = questionMode ? "Questions you miss will appear here." : "Your review deck is empty. Choose “Not yet” on a card to add it here.";
    }
    if (questionRoundFinished) {
      const attempted = [...questionAttempts.values()].filter((attempt) => attempt.firstCorrect !== null);
      const correct = attempted.filter((attempt) => attempt.firstCorrect).length;
      message = attempted.length ? `${correct} of ${attempted.length} correct on your first try.` : "You’ve reached the end of this set.";
    }
    ui["return-to-deck"].textContent = questionRoundFinished ? "Start another round" : questionMode ? "Study all questions" : "Study all cards";
    ui["empty-message"].textContent = message;
    ui.announcer.textContent = announcement || message;
    return;
  }

  ui.previous.disabled = position === 0;
  ui.next.disabled = !questionMode && position === queue.length - 1;
  ui.next.textContent = questionMode ? (position === queue.length - 1 ? "Finish round" : "Next question") : "Next card";
  if (questionMode) {
    renderQuestion(card);
    ui.announcer.textContent = announcement || "Question " + (position + 1) + " of " + queue.length + ".";
    return;
  }

  ui.flashcard.setAttribute("aria-pressed", String(answerVisible));
  ui["flip-card"].setAttribute("aria-pressed", String(answerVisible));
  ui["flip-card"].textContent = answerVisible ? "Show question" : "Show answer";
  ui["card-face-label"].hidden = !answerVisible;
  ui["flip-hint"].hidden = answerVisible;
  ui["reference-label"].hidden = !answerVisible || !card.reference;
  ui["reference-label"].textContent = answerVisible ? referenceLabels[card.reference] ?? "" : "";
  const lines = answerVisible ? card.back : [card.front];
  ui["card-content"].replaceChildren(...mathLines(lines, answerVisible ? "answer-line" : "prompt"));
  ui.announcer.textContent = announcement || (answerVisible ? "Answer shown." : "Question " + (position + 1) + " of " + queue.length + ".");
}

function resetQueue() {
  const available = availableCards();
  queue = activeDeck === "study"
    ? studyPlan(available, progress).queue
    : available.filter((card) => matchesDeck(card) && (activeTopic === "all" || activeTopic === card.topic));
  position = 0;
  answerVisible = false;
  questionRoundFinished = false;
  questionAttempts.clear();
  displayedQuestion = null;
}

function changeDeck(deck, topic = "all") {
  activeDeck = deck;
  activeTopic = topic;
  for (const button of ui.library.querySelectorAll("[data-deck]")) {
    const active = button.dataset.deck === deck && (
      deck === "review" || (button.dataset.topic ?? "all") === topic
    );
    button.setAttribute("aria-pressed", String(active));
  }
  ui["review-filter"].hidden = deck !== "review";
  ui["review-topic"].value = deck === "review" ? topic : "all";
  resetQueue();
  renderCard();
}

function flipCard() {
  if (questionMode || !queue.length) return;
  answerVisible = !answerVisible;
  renderCard();
}

function focusPractice(options) {
  const target = questionRoundFinished || !queue.length
    ? ui["return-to-deck"]
    : questionMode ? ui["question-prompt"] : ui.flashcard;
  target.focus(options);
}

function moveCard(direction) {
  const target = position + direction;
  if (questionRoundFinished) return;
  if (questionMode && direction === 1 && target === queue.length && queue.length) {
    questionRoundFinished = true;
    renderCard();
    focusPractice();
    return;
  }
  if (target < 0 || target >= queue.length) return;
  position = target;
  answerVisible = false;
  renderCard();
  if (questionMode || document.activeElement === document.body) focusPractice();
}

function shuffled(items) {
  for (let i = items.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [items[i], items[j]] = [items[j], items[i]];
  }
  return items;
}

function shuffleCards() {
  if (queue.length < 2) return;
  const currentId = queue[position].id;
  shuffled(queue);
  if (queue[0].id === currentId) {
    [queue[0], queue[1]] = [queue[1], queue[0]];
  }
  position = 0;
  answerVisible = false;
  renderCard("Cards shuffled. Question 1 of " + queue.length + ".");
  if (questionMode) focusPractice();
}

function rateCard(rating) {
  const card = queue[position];
  if (!card || questionMode) return;
  const saved = account.rate(card.id, rating);
  let announcement = rating === "known" ? "Marked as known." : "Added to your review deck.";

  if (activeDeck === "study" || (activeDeck === "review" && rating === "known")) {
    queue.splice(position, 1);
    position = Math.max(0, Math.min(position, queue.length - 1));
    answerVisible = false;
    if (!queue.length) announcement += " You’ve finished this round.";
  } else if (position < queue.length - 1) {
    position++;
    answerVisible = false;
  }

  renderProgress();
  renderCard(announcement);
  if (!saved) ui.announcer.textContent += " Progress couldn’t be saved on this device.";
  focusPractice();
}

async function start() {
  try {
    const response = await fetch("./cards.json", { cache: "no-cache" });
    if (!response.ok) throw new Error("Flashcard deck request failed");
    const data = await response.json();
    cards = data.cards;
    questionCards = cards.filter(({ choices }) => Array.isArray(choices) && choices.length === 4 &&
      choices.every((choice) => typeof choice === "string" && choice.trim()) && new Set(choices).size === 4);
    topics = new Map(data.topics.map((topic) => [topic.id, topic]));

    ui.loading.hidden = true;
    renderTopics();
    renderMode();
    renderProgress();

    const cardId = pageParams.get("card");
    const directCard = cards.find((card) => card.id === cardId);
    const topic = topics.get(directCard?.topic) ?? topics.values().next().value;
    changeDeck(topic.collection, topic.id);
    if (directCard && queue.includes(directCard)) {
      position = queue.indexOf(directCard);
      renderCard();
    }
  } catch (error) {
    console.error(error);
    ui.loading.hidden = false;
    ui.loading.textContent = "The flashcards couldn’t load. Reload the page to try again.";
  }
}

ui.library.addEventListener("click", (event) => {
  const button = event.target.closest("[data-deck]");
  if (!button || !cards.length) return;
  if (button.getAttribute("aria-pressed") !== "true") changeDeck(button.dataset.deck, button.dataset.topic);
  if (topicsDialog.open) {
    topicsDialog.close();
    focusPractice({ preventScroll: true });
  }
});
ui["review-topic"].addEventListener("change", (event) => {
  changeDeck("review", event.target.value);
});
ui["study-next"].addEventListener("click", () => {
  changeDeck("study");
  focusPractice({ preventScroll: true });
});
ui["flashcard-mode"].addEventListener("click", () => changeMode(false));
ui["question-mode"].addEventListener("click", () => changeMode(true));
ui["question-options"].addEventListener("click", (event) => {
  const choice = event.target.closest("[data-choice]");
  if (choice) answerQuestion(Number(choice.dataset.choice));
});
ui["reveal-question"].addEventListener("click", () => answerQuestion());
ui["open-topics"].addEventListener("click", () => {
  ui["mobile-library"].append(ui.library);
  topicsDialog.showModal();
  ui["open-topics"].setAttribute("aria-expanded", "true");
});
topicsDialog.addEventListener("close", () => {
  if (topicsDialog.open) return;
  ui.sidebar.append(ui.library);
  ui["open-topics"].setAttribute("aria-expanded", "false");
});
mobileLayout.addEventListener("change", (event) => {
  if (!event.matches && topicsDialog.open) topicsDialog.close();
});
ui.shuffle.addEventListener("click", shuffleCards);
ui.flashcard.addEventListener("click", flipCard);
ui["flip-card"].addEventListener("click", flipCard);
ui.previous.addEventListener("click", () => moveCard(-1));
ui.next.addEventListener("click", () => moveCard(1));
ui["know-card"].addEventListener("click", () => rateCard("known"));
ui["review-card"].addEventListener("click", () => rateCard("review"));
ui["return-to-deck"].addEventListener("click", () => {
  if (questionRoundFinished) changeDeck(activeDeck, activeTopic);
  else changeDeck("all");
  focusPractice();
});
document.addEventListener("keydown", (event) => {
  if (topicsDialog.open || ui["account-dialog"].open || event.altKey || event.ctrlKey || event.metaKey || !queue.length || questionRoundFinished || event.defaultPrevented) return;
  if (event.target.closest("input, select, textarea, [contenteditable]")) return;
  if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    moveCard(event.key === "ArrowLeft" ? -1 : 1);
  } else if (!questionMode && event.code === "Space" && !event.repeat && !event.target.closest("button, a")) {
    event.preventDefault();
    flipCard();
  }
});
const account = connectAccount(ui, useProgress);
start();
window.setInterval(() => { if (cards.length) renderProgress(); }, 60_000);
