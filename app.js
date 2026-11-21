import { studyPlan } from "./progress.js?v=1";
import { connectAccount } from "./account.js?v=3";

const ui = Object.fromEntries(Array.from(document.querySelectorAll("[id]"), (element) => [element.id, element]));
const deckLabels = { all: "All cards", revision: "Revision", trigonometry: "Trig rules", papers: "Past papers", review: "To review", study: "Study next" };
const topicHues = {
  differentiation: 155, sequences: 255, logarithms: 305, integration: 60, algebra: 20, modelling: 200,
  identities: 330, compound: 40, double: 0, factor: 100, harmonic: 210, exact: 235,
  inverse: 270, "small-angle": 80, triangles: 125, equations: 175, "trig-calculus": 295,
};
const topicsDialog = ui["topics-dialog"];
const accountDialog = ui["account-dialog"];
const mobileLayout = window.matchMedia("(max-width: 720px)");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const darkScheme = window.matchMedia("(prefers-color-scheme: dark)");
const themeKey = "maths-flashcards.theme";
const themeColors = { light: "#141a2e", dark: "#090d19" };
const easeOut = "cubic-bezier(0.22, 1, 0.36, 1)";
const easeIn = "cubic-bezier(0.55, 0, 1, 0.45)";
const spring = "cubic-bezier(0.34, 1.56, 0.64, 1)";
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
let roundStats = { known: 0, review: 0 };
let usingPointer = false;
const questionAttempts = new Map();

/* ---------- Motion ---------- */

let pendingSwap = null;

function motionAllowed(element) {
  return !reducedMotion.matches && element.isConnected && element.getClientRects().length > 0;
}

function flushMotion() {
  if (pendingSwap) pendingSwap();
}

// Animates an element out, swaps its content, then animates it back in.
// State changes happen before this is called, so an interrupted swap can be flushed safely.
function animateSwap(element, swap, out, enter, timing = {}) {
  flushMotion();
  for (const animation of element.getAnimations()) animation.cancel();
  if (!motionAllowed(element)) {
    swap();
    return;
  }
  const leave = element.animate(out, { duration: timing.out ?? 140, easing: timing.outEasing ?? easeIn, fill: "forwards" });
  let done = false;
  const finish = () => {
    if (done) return;
    done = true;
    pendingSwap = null;
    swap();
    leave.cancel();
    if (motionAllowed(element)) {
      element.animate(enter, { duration: timing.in ?? 260, easing: timing.inEasing ?? easeOut });
    }
  };
  pendingSwap = finish;
  leave.finished.then(finish, () => {});
}

function play(element, keyframes, options) {
  if (!element || reducedMotion.matches) return;
  element.animate(keyframes, options);
}

function pulse(element) {
  play(element, [{ transform: "scale(1)" }, { transform: "scale(0.94)" }, { transform: "scale(1)" }], { duration: 240, easing: easeOut });
}

function bump(element) {
  play(element, [{ transform: "scale(1)" }, { transform: "scale(1.18)" }, { transform: "scale(1)" }], { duration: 360, easing: spring });
}

function setText(element, text, animate = true) {
  const value = String(text);
  if (element.textContent === value) return;
  element.textContent = value;
  if (animate) bump(element);
}

const slide = (direction) => [
  [{ opacity: 1, transform: "translateX(0)" }, { opacity: 0, transform: `translateX(${-direction * 36}px)` }],
  [{ opacity: 0, transform: `translateX(${direction * 36}px)` }, { opacity: 1, transform: "translateX(0)" }],
];
const fade = [
  [{ opacity: 1, transform: "translateY(0)" }, { opacity: 0, transform: "translateY(6px)" }],
  [{ opacity: 0, transform: "translateY(12px)" }, { opacity: 1, transform: "translateY(0)" }],
];

/* ---------- Toast ---------- */

let toastTimer;
function toast(text) {
  const element = ui.toast;
  element.textContent = text;
  element.classList.remove("show");
  void element.offsetWidth;
  element.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => element.classList.remove("show"), 3400);
}

/* ---------- Theme ---------- */

function currentTheme() {
  return document.documentElement.dataset.theme ?? (darkScheme.matches ? "dark" : "light");
}

function renderTheme() {
  const theme = currentTheme();
  ui["theme-toggle"].dataset.current = theme;
  ui["theme-toggle"].setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
  ui["theme-toggle"].title = theme === "dark" ? "Light mode" : "Dark mode";
  document.querySelector('meta[name="theme-color"]').content = themeColors[theme];
}

function toggleTheme() {
  const next = currentTheme() === "dark" ? "light" : "dark";
  const apply = () => {
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem(themeKey, next); } catch {}
    renderTheme();
  };
  if (!document.startViewTransition || reducedMotion.matches) {
    apply();
    return;
  }
  const rect = ui["theme-toggle"].getBoundingClientRect();
  const x = rect.left + rect.width / 2;
  const y = rect.top + rect.height / 2;
  const radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
  const transition = document.startViewTransition(apply);
  transition.ready.then(() => {
    document.documentElement.animate(
      { clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${radius}px at ${x}px ${y}px)`] },
      { duration: 560, easing: easeOut, pseudoElement: "::view-transition-new(root)" },
    );
  }).catch(() => {});
}

/* ---------- Rendering ---------- */

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

const lineLabel = /^(Spot|Use|Method|Answers?|Watch out|Check|Key idea|Tip):\s*/;
const partLabel = /^\((?:[a-h]|i{1,3}|iv|v|vi)\)\s+/;

// Lines can start with a label such as "Spot:" or a part such as "(a)". Both get their own styling.
function mathLines(lines, className) {
  return lines.map((line) => {
    const element = document.createElement("span");
    element.className = className;
    const label = lineLabel.exec(line);
    const part = label ? null : partLabel.exec(line);
    if (label) {
      const tag = document.createElement("span");
      tag.className = "line-label " + label[1].toLowerCase().replace(/\s+/g, "-");
      tag.textContent = label[1];
      element.append(tag);
      appendMath(element, line.slice(label[0].length), false);
    } else if (part) {
      const tag = document.createElement("span");
      tag.className = "part-label";
      tag.textContent = part[0].trim();
      element.append(tag, " ");
      appendMath(element, line.slice(part[0].length), false);
    } else {
      appendMath(element, line);
    }
    return element;
  });
}

function frontLines(card) {
  return Array.isArray(card.front) ? card.front : [card.front];
}

function isExam(card) {
  return topics.get(card?.topic)?.collection === "papers";
}

function availableCards() {
  return questionMode ? questionCards : cards;
}

function matchesDeck(card) {
  if (activeDeck === "all") return true;
  if (activeDeck === "review") return progress.get(card.id)?.rating === "review";
  return topics.get(card.topic).collection === activeDeck;
}

function renderProgress(animate = true) {
  const available = availableCards();
  const known = available.filter((card) => progress.get(card.id)?.rating === "known").length;
  const review = available.filter((card) => progress.get(card.id)?.rating === "review").length;
  const plan = studyPlan(available, progress);
  ui["count-all"].textContent = available.length;
  setText(ui["count-review"], review, animate);
  setText(ui["known-count"], known, animate);
  ui["mastery-fill"].style.transform = `scaleX(${available.length ? known / available.length : 0})`;
  ui["study-next"].disabled = !plan.queue.length;
  ui["study-next-label"].textContent = plan.queue.length ? "Study next" : "All caught up";
  setText(ui["study-next-count"], plan.reviewCount ? plan.reviewCount + " due" : plan.queue.length ? plan.queue.length + " new" : "", animate);

  for (const button of ui.library.querySelectorAll("[data-topic]")) {
    const topicCards = available.filter((card) => card.topic === button.dataset.topic);
    const topicKnown = topicCards.filter((card) => progress.get(card.id)?.rating === "known").length;
    button.style.setProperty("--mastery", topicCards.length ? topicKnown / topicCards.length : 0);
    button.toggleAttribute("data-started", topicKnown > 0);
    button.title = `${topicKnown} of ${topicCards.length} known`;
  }
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
  let index = 0;
  for (const topic of topics.values()) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "topic-button";
    button.dataset.deck = topic.collection;
    button.dataset.topic = topic.id;
    button.style.setProperty("--hue", topicHues[topic.id] ?? topic.hue ?? 155);
    button.style.setProperty("--i", index++);

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
  ui["study-modes"].dataset.active = questionMode ? "questions" : "flashcards";
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
  flushMotion();
  const card = queue[position];
  questionMode = showQuestions;

  const url = new URL(window.location.href);
  if (questionMode) url.searchParams.set("mode", "questions");
  else url.searchParams.delete("mode");
  history.replaceState(history.state, "", url);

  ui["study-modes"].dataset.active = questionMode ? "questions" : "flashcards";
  ui["question-mode"].setAttribute("aria-pressed", String(questionMode));
  ui["flashcard-mode"].setAttribute("aria-pressed", String(!questionMode));
  if (!cards.length) {
    renderMode();
    return;
  }
  resetQueue();
  if (queue.includes(card)) position = queue.indexOf(card);
  animateSwap(ui["deck-view"], () => {
    renderMode();
    renderProgress(false);
    renderCard();
  }, ...fade, { out: 120, in: 300 });
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
    const exam = isExam(card);
    ui["question-card"].classList.toggle("exam", exam);
    ui["question-prompt"].replaceChildren(...frontLines(card).map((line) => {
      const element = document.createElement("span");
      element.className = "prompt-line";
      appendMath(element, line, false);
      return element;
    }));
    if (exam) {
      const ask = document.createElement("span");
      ask.className = "ask-line";
      ask.textContent = card.ask ?? "How should you start?";
      ui["question-prompt"].append(ask);
    }
    const visibleLength = (text) => text.replace(/\\[a-zA-Z]+/g, "x").replace(/[${}^_\\\s]/g, "").length;
    optionList.dataset.fit = attempt.options.every((option) => visibleLength(option.text) <= 24) ? "try" : "";
    optionList.replaceChildren(...attempt.options.map((option, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "question-option";
      button.dataset.choice = index;
      button.style.setProperty("--i", index);
      button.setAttribute("aria-keyshortcuts", String(index + 1));
      const letter = document.createElement("span");
      letter.className = "option-letter";
      letter.setAttribute("aria-hidden", "true");
      const text = document.createElement("span");
      text.className = "option-text";
      appendMath(text, option.text, false);
      button.append(letter, text);
      return button;
    }));
    fitOptions();
  }

  for (const [index, button] of Array.from(optionList.children).entries()) {
    const correct = attempt.outcome && attempt.options[index].correct;
    const wrong = attempt.wrong.has(index);
    button.dataset.result = correct ? "correct" : wrong ? "wrong" : "";
    button.setAttribute("aria-disabled", String(Boolean(attempt.outcome) || wrong));
    button.firstElementChild.textContent = correct ? "✓" : wrong ? "×" : "ABCD"[index];
  }

  let message = attempt.wrong.size ? "Not quite. Try another answer." : "";
  if (attempt.outcome === "revealed") message = "Answer shown. It’s on your review list.";
  if (attempt.outcome === "correct") message = attempt.firstCorrect ? "Correct!" : "Correct. It’s on your review list.";
  ui["question-feedback"].textContent = message;
  ui["question-feedback"].dataset.outcome = attempt.outcome ?? (attempt.wrong.size ? "wrong" : "");
  ui["reveal-question"].hidden = Boolean(attempt.outcome);
  ui["question-explanation"].hidden = !attempt.outcome;
  if (attempt.outcome) ui["question-explanation"].replaceChildren(...mathLines(card.back, "answer-line"));
  markScrollable();
}

// On phones, short answers sit in a 2×2 grid, but only if every one fits on a single line.
function fitOptions() {
  const list = ui["question-options"];
  list.classList.toggle("compact", list.dataset.fit === "try");
  if (!list.classList.contains("compact")) return;
  const overflowing = Array.from(list.querySelectorAll(".option-text")).some((text) => text.scrollWidth > text.clientWidth + 1);
  if (overflowing) list.classList.remove("compact");
}

function answerQuestion(choiceIndex) {
  const card = queue[position];
  if (!questionMode || !card || questionRoundFinished) return;
  flushMotion();
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
  renderNextButton();

  const button = ui["question-options"].children[choiceIndex];
  if (correct) {
    play(button, [{ transform: "scale(1)" }, { transform: "scale(1.035)" }, { transform: "scale(1)" }], { duration: 420, easing: spring });
  } else if (button) {
    play(button, [
      { transform: "translateX(0)" }, { transform: "translateX(-8px)" }, { transform: "translateX(7px)" },
      { transform: "translateX(-4px)" }, { transform: "translateX(2px)" }, { transform: "translateX(0)" },
    ], { duration: 420, easing: "ease-out" });
  }
  play(ui["question-feedback"], [{ opacity: 0, transform: "translateY(4px)" }, { opacity: 1, transform: "none" }], { duration: 260, easing: easeOut });
  if (!saved) ui["question-feedback"].textContent += " Progress couldn’t be saved on this device.";
  if (revealed) ui["question-feedback"].focus({ preventScroll: true });
  if (attempt.outcome) {
    const card = ui["question-card"];
    requestAnimationFrame(() => {
      if (card.scrollHeight > card.clientHeight) {
        card.scrollTo({ top: card.scrollHeight, behavior: reducedMotion.matches ? "auto" : "smooth" });
      }
    });
  }
}

function renderNextButton() {
  const last = position === queue.length - 1;
  const label = questionMode ? (last ? "Finish" : "Next") : "Next";
  ui["next-label"].textContent = label;
  ui.next.setAttribute("aria-label", questionMode ? (last ? "Finish round" : "Next question") : "Next card");
  const attempt = questionMode ? questionAttempts.get(queue[position]?.id) : null;
  ui.next.classList.toggle("ready", Boolean(attempt?.outcome));
}

function renderCard(announcement = "") {
  const card = questionRoundFinished ? undefined : queue[position];
  const topic = topics.get(card?.topic ?? activeTopic);
  ui.practice.hidden = !card;
  ui.empty.hidden = Boolean(card);
  const deckName = questionMode && activeDeck === "all" ? "All questions" : deckLabels[activeDeck];
  ui["collection-label"].textContent = deckName;
  ui["deck-title"].textContent = topic?.title ?? deckName;
  ui["open-topics"].style.setProperty("--hue", topicHues[topic?.id] ?? topic?.hue ?? 155);
  ui["menu-label"].textContent = topic?.title ?? deckName;
  ui["open-topics"].setAttribute("aria-label", "Choose a topic. Current: " + (topic?.title ?? deckName));
  ui["position-label"].textContent = card ? (position + 1) + " / " + queue.length : "";
  ui["deck-progress-fill"].style.transform = `scaleX(${queue.length ? (position + 1) / queue.length : 0})`;
  ui.shuffle.disabled = queue.length < 2;
  if (!card) {
    const ratedThisRound = roundStats.known + roundStats.review;
    let done = false;
    let message = questionMode ? "There are no questions for this topic." : "There are no cards for this topic in this deck.";
    let action = questionMode ? "Study all questions" : "Study all cards";
    if (activeDeck === "study") {
      done = ratedThisRound > 0;
      if (done) {
        message = `Round complete. ${roundStats.known} got it, ${roundStats.review} to review.`;
        action = ui["study-next"].disabled ? "Study all cards" : "Next round";
      } else {
        message = ui["study-next"].disabled
          ? "You’re all caught up. Come back when more cards are due."
          : "You’ve finished this round. Use Study next when you’re ready for another.";
      }
    }
    if (activeDeck === "review" && activeTopic === "all") {
      message = questionMode ? "Questions you miss will appear here." : "Your review deck is empty. Choose “Not yet” on a card to add it here.";
    }
    if (questionRoundFinished) {
      const attempted = [...questionAttempts.values()].filter((attempt) => attempt.firstCorrect !== null);
      const correct = attempted.filter((attempt) => attempt.firstCorrect).length;
      done = true;
      message = attempted.length ? `${correct} of ${attempted.length} correct on your first try.` : "You’ve reached the end of this set.";
      action = "Start another round";
    }
    ui.empty.dataset.state = done ? "done" : "empty";
    ui["return-to-deck"].textContent = action;
    ui["empty-message"].textContent = message;
    ui.announcer.textContent = announcement || message;
    return;
  }

  ui.previous.disabled = position === 0;
  ui.next.disabled = !questionMode && position === queue.length - 1;
  renderNextButton();
  if (questionMode) {
    if (displayedQuestion !== questionAttempts.get(card.id)) ui["question-card"].scrollTop = 0;
    renderQuestion(card);
    ui.announcer.textContent = announcement || "Question " + (position + 1) + " of " + queue.length + ".";
    return;
  }

  ui.flashcard.setAttribute("aria-pressed", String(answerVisible));
  ui.flashcard.classList.toggle("answer-side", answerVisible);
  ui["flip-card"].setAttribute("aria-pressed", String(answerVisible));
  ui["flip-card"].textContent = answerVisible ? "Show question" : "Show answer";
  const exam = isExam(card);
  ui.flashcard.classList.toggle("exam", exam);
  ui["card-face-label"].textContent = answerVisible ? (exam ? "Method" : "Answer") : (card.source ?? "Question");
  ui["flip-hint"].hidden = answerVisible;
  ui["reference-label"].hidden = !answerVisible || !card.reference;
  ui["reference-label"].textContent = answerVisible ? referenceLabels[card.reference] ?? "" : "";
  const lines = answerVisible ? card.back : frontLines(card);
  ui["card-content"].replaceChildren(...mathLines(lines, answerVisible ? "answer-line" : exam ? "exam-line" : "prompt"));
  ui["card-content"].scrollTop = 0;
  markScrollable();
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
  roundStats = { known: 0, review: 0 };
  questionAttempts.clear();
  displayedQuestion = null;
}

function changeDeck(deck, topic = "all", animate = true) {
  flushMotion();
  activeDeck = deck;
  activeTopic = topic;
  for (const button of ui.library.querySelectorAll("[data-deck]")) {
    const active = button.dataset.deck === deck && (
      deck === "review" || (button.dataset.topic ?? "all") === topic
    );
    button.setAttribute("aria-pressed", String(active));
  }
  resetQueue();
  const render = () => {
    ui["review-filter"].hidden = deck !== "review";
    ui["review-topic"].value = deck === "review" ? topic : "all";
    renderCard();
  };
  if (animate) animateSwap(ui["deck-view"], render, ...fade, { out: 120, in: 320 });
  else render();
}

function stage() {
  return questionMode ? ui["question-card"] : ui.flashcard;
}

function flipCard() {
  if (questionMode || !queue.length) return;
  flushMotion();
  answerVisible = !answerVisible;
  const turn = answerVisible ? 1 : -1;
  animateSwap(ui.flashcard, () => renderCard(), [
    { transform: "perspective(1400px) rotateY(0deg) scale(1)" },
    { transform: `perspective(1400px) rotateY(${turn * 90}deg) scale(0.97)` },
  ], [
    { transform: `perspective(1400px) rotateY(${-turn * 90}deg) scale(0.97)` },
    { transform: "perspective(1400px) rotateY(0deg) scale(1)" },
  ], { out: 150, in: 320 });
}

function focusPractice() {
  if (usingPointer) return;
  const target = questionRoundFinished || !queue.length
    ? ui["return-to-deck"]
    : questionMode ? ui["question-prompt"] : ui.flashcard;
  target.focus({ preventScroll: true });
}

function moveCard(direction) {
  if (questionRoundFinished) return;
  flushMotion();
  const target = position + direction;
  if (questionMode && direction === 1 && target === queue.length && queue.length) {
    questionRoundFinished = true;
    animateSwap(stage(), () => {
      renderCard();
      focusPractice();
    }, ...fade, { out: 140 });
    return;
  }
  if (target < 0 || target >= queue.length) {
    play(stage(), [
      { transform: "translateX(0)" }, { transform: `translateX(${direction * 10}px)` }, { transform: "translateX(0)" },
    ], { duration: 260, easing: easeOut });
    return;
  }
  position = target;
  answerVisible = false;
  animateSwap(stage(), () => {
    renderCard();
    if (questionMode) focusPractice();
  }, ...slide(direction));
  if (!questionMode && document.activeElement === document.body) focusPractice();
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
  flushMotion();
  const currentId = queue[position].id;
  shuffled(queue);
  if (queue[0].id === currentId) {
    [queue[0], queue[1]] = [queue[1], queue[0]];
  }
  position = 0;
  answerVisible = false;
  play(ui.shuffle.querySelector("svg"), [{ transform: "rotate(0)" }, { transform: "rotate(360deg)" }], { duration: 520, easing: easeOut });
  animateSwap(stage(), () => {
    renderCard("Cards shuffled. Question 1 of " + queue.length + ".");
    if (questionMode) focusPractice();
  }, [
    { opacity: 1, transform: "scale(1) rotate(0deg)" },
    { opacity: 0, transform: "scale(0.94) rotate(-2deg)" },
  ], [
    { opacity: 0, transform: "scale(0.94) rotate(2deg)" },
    { opacity: 1, transform: "scale(1) rotate(0deg)" },
  ], { out: 160, in: 340 });
}

function rateCard(rating, { dragged = false } = {}) {
  const card = queue[position];
  if (!card || questionMode) return;
  flushMotion();
  const saved = account.rate(card.id, rating);
  roundStats[rating]++;
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
  const direction = rating === "known" ? 1 : -1;
  const flashcard = ui.flashcard;
  const from = flashcard.style.transform || "translateX(0) rotate(0deg)";
  flashcard.style.transform = "";
  flashcard.style.setProperty("--swipe", direction);
  pulse(rating === "known" ? ui["know-card"] : ui["review-card"]);
  animateSwap(flashcard, () => {
    flashcard.style.removeProperty("--swipe");
    renderCard(announcement);
    if (!saved) ui.announcer.textContent += " Progress couldn’t be saved on this device.";
  }, [
    { opacity: 1, transform: from },
    { opacity: 0, transform: `translateX(${direction * 115}%) rotate(${direction * 12}deg)` },
  ], [
    { opacity: 0, transform: "translateY(18px) scale(0.94)" },
    { opacity: 1, transform: "translateY(0) scale(1)" },
  ], { out: dragged ? 220 : 300, in: 380 });
  focusPractice();
}

/* ---------- Swipe to rate ---------- */

function setupSwipe() {
  const card = ui.flashcard;
  let drag = null;
  let suppressClickUntil = 0;

  card.addEventListener("pointerdown", (event) => {
    if (!event.isPrimary || event.button !== 0 || questionMode || !queue.length) return;
    drag = { x: event.clientX, y: event.clientY, time: performance.now(), id: event.pointerId, active: false };
  });

  card.addEventListener("pointermove", (event) => {
    if (!drag || event.pointerId !== drag.id) return;
    const dx = event.clientX - drag.x;
    const dy = event.clientY - drag.y;
    if (!drag.active) {
      if (Math.abs(dy) > 12 && Math.abs(dy) > Math.abs(dx)) {
        drag = null;
        return;
      }
      if (Math.abs(dx) < 10) return;
      drag.active = true;
      flushMotion();
      for (const animation of card.getAnimations()) animation.cancel();
      card.setPointerCapture(event.pointerId);
      card.classList.add("dragging");
    }
    const width = card.offsetWidth || 1;
    card.style.transform = `translateX(${dx}px) rotate(${(dx / width) * 9}deg)`;
    card.style.setProperty("--swipe", Math.max(-1, Math.min(1, dx / (width * 0.32))).toFixed(3));
  });

  const end = (event) => {
    if (!drag || event.pointerId !== drag.id) return;
    const current = drag;
    drag = null;
    if (!current.active) return;
    suppressClickUntil = performance.now() + 400;
    card.classList.remove("dragging");
    const dx = event.clientX - current.x;
    const velocity = dx / Math.max(1, performance.now() - current.time);
    const width = card.offsetWidth || 1;
    const committed = event.type !== "pointercancel" &&
      (Math.abs(dx) > width * 0.3 || (Math.abs(dx) > 50 && Math.abs(velocity) > 0.6));
    if (committed) {
      navigator.vibrate?.(12);
      rateCard(dx > 0 ? "known" : "review", { dragged: true });
      return;
    }
    const from = card.style.transform;
    card.style.transform = "";
    card.style.removeProperty("--swipe");
    play(card, [{ transform: from }, { transform: "translateX(0) rotate(0deg)" }], { duration: 480, easing: spring });
  };
  card.addEventListener("pointerup", end);
  card.addEventListener("pointercancel", end);
  ui["card-content"].addEventListener("scroll", markScrollable, { passive: true });
  ui["question-card"].addEventListener("scroll", markScrollable, { passive: true });
  card.addEventListener("keydown", (event) => {
    if ((event.key === "Enter" || event.key === " ") && !event.repeat) {
      event.preventDefault();
      flipCard();
    }
  });
  card.addEventListener("click", (event) => {
    if (performance.now() < suppressClickUntil) {
      event.preventDefault();
      return;
    }
    flipCard();
  });
}

/* ---------- Dialogs ---------- */

function closeOnBackdrop(dialog) {
  let downOutside = false;
  const outside = (event) => {
    const rect = dialog.getBoundingClientRect();
    return event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom;
  };
  dialog.addEventListener("pointerdown", (event) => { downOutside = event.target === dialog && outside(event); });
  dialog.addEventListener("click", (event) => {
    if (downOutside && event.target === dialog && outside(event)) dialog.close();
    downOutside = false;
  });
}

// Long cards scroll inside the card; a fade at the bottom shows there's more.
function markScrollable() {
  requestAnimationFrame(() => {
    for (const box of [ui["card-content"], ui["question-card"]]) {
      const more = !box.hidden && box.scrollHeight - box.clientHeight - box.scrollTop > 4;
      box.classList.toggle("scrollable", more);
    }
  });
}

/* ---------- Mobile header ---------- */

// On phones the theme and account buttons live in the top bar so the page fits on one screen.
function placeHeaderActions() {
  const target = mobileLayout.matches ? ui["mobile-actions"] : ui["study-modes"].parentElement;
  if (ui["topline-actions"].parentElement !== target) target.append(ui["topline-actions"]);
}

/* ---------- Start ---------- */

async function loadDeck(url) {
  const response = await fetch(url, { cache: "no-cache" });
  if (!response.ok) throw new Error("Deck request failed: " + url);
  return response.json();
}

async function start() {
  try {
    const [main, papers] = await Promise.all([loadDeck("./cards.json"), loadDeck("./papers.json").catch(() => null)]);
    const data = {
      topics: [...main.topics, ...(papers?.topics ?? [])],
      cards: [...main.cards, ...(papers?.cards ?? [])],
    };
    cards = data.cards;
    questionCards = cards.filter(({ choices }) => Array.isArray(choices) && choices.length === 4 &&
      choices.every((choice) => typeof choice === "string" && choice.trim()) && new Set(choices).size === 4);
    topics = new Map(data.topics.map((topic) => [topic.id, topic]));

    ui.loading.hidden = true;
    renderTopics();
    renderMode();
    renderProgress(false);

    const cardId = pageParams.get("card");
    const directCard = cards.find((card) => card.id === cardId);
    const topic = topics.get(directCard?.topic) ?? topics.values().next().value;
    changeDeck(topic.collection, topic.id, false);
    if (directCard && queue.includes(directCard)) {
      position = queue.indexOf(directCard);
      renderCard();
    }
  } catch (error) {
    console.error(error);
    ui.loading.hidden = false;
    ui.loading.replaceChildren("The flashcards couldn’t load. Reload the page to try again.");
  }
}

document.addEventListener("pointerdown", () => { usingPointer = true; }, true);
document.addEventListener("keydown", () => { usingPointer = false; }, true);

ui.library.addEventListener("click", (event) => {
  const button = event.target.closest("[data-deck]");
  if (!button || !cards.length) return;
  if (button.getAttribute("aria-pressed") !== "true") changeDeck(button.dataset.deck, button.dataset.topic);
  if (topicsDialog.open) topicsDialog.close();
});
ui["review-topic"].addEventListener("change", (event) => {
  changeDeck("review", event.target.value);
});
ui["study-next"].addEventListener("click", () => {
  changeDeck("study");
  focusPractice();
});
ui["flashcard-mode"].addEventListener("click", () => changeMode(false));
ui["question-mode"].addEventListener("click", () => changeMode(true));
ui["question-options"].addEventListener("click", (event) => {
  const choice = event.target.closest("[data-choice]");
  if (choice) answerQuestion(Number(choice.dataset.choice));
});
ui["reveal-question"].addEventListener("click", () => answerQuestion());
ui["theme-toggle"].addEventListener("click", toggleTheme);
darkScheme.addEventListener("change", renderTheme);

ui["open-topics"].addEventListener("click", () => {
  ui["mobile-library"].append(ui.library);
  topicsDialog.showModal();
  ui["open-topics"].setAttribute("aria-expanded", "true");
});
ui["close-topics"].addEventListener("click", () => topicsDialog.close());
topicsDialog.addEventListener("close", () => {
  ui["open-topics"].setAttribute("aria-expanded", "false");
  // Leave the list in the drawer until its closing animation has finished.
  setTimeout(() => {
    if (!topicsDialog.open) ui.sidebar.append(ui.library);
  }, mobileLayout.matches ? 360 : 0);
});
let fitFrame = 0;
window.addEventListener("resize", () => {
  cancelAnimationFrame(fitFrame);
  fitFrame = requestAnimationFrame(() => {
    if (questionMode) fitOptions();
    markScrollable();
  });
});
mobileLayout.addEventListener("change", (event) => {
  if (!event.matches && topicsDialog.open) topicsDialog.close();
  placeHeaderActions();
});
closeOnBackdrop(topicsDialog);
closeOnBackdrop(accountDialog);

ui.shuffle.addEventListener("click", shuffleCards);
ui["flip-card"].addEventListener("click", flipCard);
ui.previous.addEventListener("click", () => moveCard(-1));
ui.next.addEventListener("click", () => moveCard(1));
ui["know-card"].addEventListener("click", () => rateCard("known"));
ui["review-card"].addEventListener("click", () => rateCard("review"));
ui["return-to-deck"].addEventListener("click", () => {
  if (questionRoundFinished) changeDeck(activeDeck, activeTopic);
  else if (activeDeck === "study" && !ui["study-next"].disabled) changeDeck("study");
  else changeDeck("all");
  focusPractice();
});

document.addEventListener("keydown", (event) => {
  if (topicsDialog.open || accountDialog.open || event.altKey || event.ctrlKey || event.metaKey || !queue.length || questionRoundFinished || event.defaultPrevented) return;
  if (event.target.closest("input, select, textarea, [contenteditable]")) return;
  const key = event.key.toLowerCase();
  if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    moveCard(event.key === "ArrowLeft" ? -1 : 1);
  } else if (!questionMode && event.code === "Space" && !event.repeat && !event.target.closest("button, a")) {
    event.preventDefault();
    flipCard();
  } else if (!questionMode && (key === "1" || key === "2") && !event.repeat) {
    event.preventDefault();
    rateCard(key === "2" ? "known" : "review");
  } else if (questionMode && !event.repeat && ["1", "2", "3", "4", "a", "b", "c", "d"].includes(key)) {
    event.preventDefault();
    const index = "1234".includes(key) ? Number(key) - 1 : "abcd".indexOf(key);
    answerQuestion(index);
  } else if (questionMode && event.key === "Enter" && !event.target.closest("button, a")) {
    const attempt = questionAttempts.get(queue[position]?.id);
    if (attempt?.outcome) {
      event.preventDefault();
      moveCard(1);
    }
  }
});

setupSwipe();
placeHeaderActions();
// Math fonts load lazily, so measure the answer choices again once they arrive.
function refit() {
  if (questionMode) fitOptions();
  markScrollable();
}
document.fonts?.ready.then(refit);
document.fonts?.addEventListener("loadingdone", refit);
renderTheme();
const account = connectAccount(ui, useProgress, toast);
start();
window.setInterval(() => { if (cards.length) renderProgress(false); }, 60_000);
