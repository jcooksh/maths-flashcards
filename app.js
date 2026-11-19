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

let cards = [];
let topics = new Map();
let progress = new Map();
let queue = [];
let activeDeck = "all";
let activeTopic = "all";
let position = 0;
let answerVisible = false;

function appendMath(element, value) {
  const segments = value.split(/(\$[^$]+\$)/g);
  const displayMode = segments.length === 3 && segments[0] === "" && segments[2] === "";
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

function matchesDeck(card) {
  if (activeDeck === "all") return true;
  if (activeDeck === "review") return progress.get(card.id)?.rating === "review";
  return topics.get(card.topic).collection === activeDeck;
}

function renderProgress() {
  const known = cards.filter((card) => progress.get(card.id)?.rating === "known").length;
  const review = cards.filter((card) => progress.get(card.id)?.rating === "review").length;
  const plan = studyPlan(cards, progress);
  ui["count-all"].textContent = cards.length;
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
  if (activeDeck === "review") {
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
    count.textContent = cards.filter((card) => card.topic === topic.id).length;
    button.append(dot, name, count);
    ui[topic.collection + "-topics"].append(button);
    ui["review-topic"].add(new Option(topic.title, topic.id));
  }
}

function renderCard(announcement = "") {
  const card = queue[position];
  const topic = topics.get(card?.topic ?? activeTopic);
  ui.practice.hidden = !card;
  ui.empty.hidden = Boolean(card);
  ui["collection-label"].textContent = deckLabels[activeDeck];
  ui["deck-title"].textContent = topic?.title ?? deckLabels[activeDeck];
  ui["position-label"].textContent = card ? (position + 1) + " of " + queue.length : "";
  ui.shuffle.disabled = queue.length < 2;
  if (!card) {
    let message = "There are no cards for this topic in this deck.";
    if (activeDeck === "study") {
      message = ui["study-next"].disabled
        ? "You’re caught up. Come back when more cards are due."
        : "You’ve finished this round. Use Study next when you’re ready for another.";
    }
    if (activeDeck === "review" && activeTopic === "all") {
      message = "Your review deck is empty. Choose “Not yet” on a card to add it here.";
    }
    ui["empty-message"].textContent = message;
    ui.announcer.textContent = announcement || message;
    return;
  }

  ui.flashcard.setAttribute("aria-pressed", String(answerVisible));
  ui["flip-card"].setAttribute("aria-pressed", String(answerVisible));
  ui["flip-card"].textContent = answerVisible ? "Show question" : "Show answer";
  ui["card-face-label"].hidden = !answerVisible;
  ui["flip-hint"].hidden = answerVisible;
  ui["reference-label"].hidden = !answerVisible || !card.reference;
  ui["reference-label"].textContent = answerVisible ? referenceLabels[card.reference] ?? "" : "";
  ui.previous.disabled = position === 0;
  ui.next.disabled = position === queue.length - 1;

  const lines = answerVisible ? card.back : [card.front];
  ui["card-content"].replaceChildren(...lines.map((line) => {
    const element = document.createElement("span");
    element.className = answerVisible ? "answer-line" : "prompt";
    appendMath(element, line);
    return element;
  }));
  ui.announcer.textContent = announcement || (answerVisible ? "Answer shown." : "Question " + (position + 1) + " of " + queue.length + ".");
}

function resetQueue() {
  queue = activeDeck === "study"
    ? studyPlan(cards, progress).queue
    : cards.filter((card) => matchesDeck(card) && (activeTopic === "all" || activeTopic === card.topic));
  position = 0;
  answerVisible = false;
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
  if (!queue.length) return;
  answerVisible = !answerVisible;
  renderCard();
}

function moveCard(direction) {
  const target = position + direction;
  if (target < 0 || target >= queue.length) return;
  position = target;
  answerVisible = false;
  renderCard();
  if (document.activeElement === document.body) ui.flashcard.focus();
}

function shuffleCards() {
  if (queue.length < 2) return;
  const currentId = queue[position].id;
  for (let i = queue.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [queue[i], queue[j]] = [queue[j], queue[i]];
  }
  if (queue[0].id === currentId) {
    [queue[0], queue[1]] = [queue[1], queue[0]];
  }
  position = 0;
  answerVisible = false;
  renderCard("Cards shuffled. Question 1 of " + queue.length + ".");
}

function rateCard(rating) {
  const card = queue[position];
  if (!card) return;
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
  (queue.length ? ui.flashcard : ui["return-to-deck"]).focus();
}

async function start() {
  try {
    const response = await fetch("./cards.json", { cache: "no-cache" });
    if (!response.ok) throw new Error("Flashcard deck request failed");
    const data = await response.json();
    cards = data.cards;
    topics = new Map(data.topics.map((topic) => [topic.id, topic]));

    ui.loading.hidden = true;
    renderTopics();
    renderProgress();

    const cardId = new URLSearchParams(window.location.search).get("card");
    const directCard = cards.find((card) => card.id === cardId);
    const topic = topics.get(directCard?.topic) ?? topics.values().next().value;
    changeDeck(topic.collection, topic.id);
    if (directCard) {
      position = queue.findIndex((card) => card.id === cardId);
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
    (queue.length ? ui.flashcard : ui["return-to-deck"]).focus({ preventScroll: true });
  }
});
ui["review-topic"].addEventListener("change", (event) => {
  changeDeck("review", event.target.value);
});
ui["study-next"].addEventListener("click", () => {
  changeDeck("study");
  (queue.length ? ui.flashcard : ui["return-to-deck"]).focus({ preventScroll: true });
});
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
  changeDeck("all");
  ui.flashcard.focus();
});
document.addEventListener("keydown", (event) => {
  if (topicsDialog.open || ui["account-dialog"].open || event.altKey || event.ctrlKey || event.metaKey || !queue.length || event.defaultPrevented) return;
  if (event.target.closest("input, select, textarea, [contenteditable]")) return;
  if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    moveCard(event.key === "ArrowLeft" ? -1 : 1);
  } else if (event.code === "Space" && !event.repeat && !event.target.closest("button, a")) {
    event.preventDefault();
    flipCard();
  }
});
const account = connectAccount(ui, useProgress);
start();
window.setInterval(() => { if (cards.length) renderProgress(); }, 60_000);
