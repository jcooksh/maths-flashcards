import { boxes, boxNames, boxOf, boxCounts, sessionPlan, isDue } from "./progress.js?v=2";
import { connectAccount } from "./account.js?v=4";
import { renderDashboard, boxBar, boxLegend, fitLabels, studyStreak } from "./dashboard.js?v=1";
import { dayKey } from "./activity.js?v=1";

const ui = Object.fromEntries(Array.from(document.querySelectorAll("[id]"), (element) => [element.id, element]));
const deckLabels = { all: "All cards", revision: "Revision", trigonometry: "Trig rules", papers: "Past papers", session: "Session" };
const collections = ["revision", "trigonometry", "papers"];
const collectionHues = { revision: 155, trigonometry: 330, papers: 240 };
const topicHues = {
  differentiation: 155, sequences: 255, logarithms: 305, integration: 60, algebra: 20, modelling: 200,
  identities: 330, compound: 40, double: 0, factor: 100, harmonic: 210, exact: 235,
  inverse: 270, "small-angle": 80, triangles: 125, equations: 175, "trig-calculus": 295,
};
const topicsDialog = ui["topics-dialog"];
const studyArea = document.querySelector(".study");
const accountDialog = ui["account-dialog"];
const mobileLayout = window.matchMedia("(max-width: 720px)");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const darkScheme = window.matchMedia("(prefers-color-scheme: dark)");
const themeKey = "maths-flashcards.theme";
const selectionKey = "maths-flashcards.excluded-topics.v1";
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
let usingPointer = false;
// Keyed by the queue entry, so a card that comes back later in a session gets a fresh attempt.
const questionAttempts = new Map();
let view = "home";
let navDepth = 0;
let session = null;
let lastSession = null;
let excludedTopics = readExcluded();
let pickerCollection = null;

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
  return topics.get(card.topic).collection === activeDeck;
}

const plural = (count, word) => count + " " + word + (count === 1 ? "" : "s");

/* ---------- Boxes ---------- */

// Where a card goes if the next answer is right or wrong.
function destination(record, correct, now = Date.now()) {
  if (!correct) return "red";
  if (!record || record.rating === "review") return "amber";
  return record.dueAt <= now ? "green" : boxOf(record);
}

function moveText(before, after, correct) {
  if (after !== before) return "Moved to " + boxNames[after] + ".";
  if (!correct) return "Still in Red.";
  return after === "green" ? "Stays in Green." : "Stays in " + boxNames[after] + " until it’s due.";
}

function sessionSummary(stats) {
  let text = plural(stats.done, "card") + ", " + stats.right + " right";
  if (stats.up) text += ", " + stats.up + " moved up";
  return text;
}

// Saves one answer, updates the session tally and logs it for the progress charts.
function recordAnswer(card, correct) {
  const before = boxOf(progress.get(card.id));
  const saved = account.rate(card.id, correct ? "known" : "review");
  const after = boxOf(progress.get(card.id));
  account.logReview(correct, boxCounts(cards, progress));
  if (activeDeck === "session" && session) {
    session.stats.done++;
    if (correct) session.stats.right++;
    if (boxes.indexOf(after) > boxes.indexOf(before)) session.stats.up++;
    if (boxes.indexOf(after) < boxes.indexOf(before)) session.stats.down++;
  }
  return { saved, before, after };
}

// A missed card comes back a few cards later in the same session.
function requeue(card) {
  if (activeDeck !== "session") return;
  const at = Math.min(queue.length, position + 5);
  queue.splice(at, 0, { ...card });
}

function renderProgress() {
  if (!cards.length) return;
  const available = availableCards();
  const counts = boxCounts(available, progress);
  ui["rail-boxes"].replaceChildren(boxBar(counts));
  ui["rail-legend"].replaceChildren(...boxes.map((box) => {
    const item = document.createElement("span");
    item.className = "rail-count";
    const swatch = document.createElement("span");
    swatch.className = "swatch " + box;
    item.append(swatch, boxNames[box] + " " + counts[box]);
    return item;
  }));
  ui["rail-summary"].setAttribute("aria-label", `Your boxes: ${counts.red} red, ${counts.amber} amber, ${counts.green} green. Open your progress`);

  for (const button of ui.library.querySelectorAll("[data-topic]")) {
    const topicCards = available.filter((card) => card.topic === button.dataset.topic);
    const green = topicCards.filter((card) => boxOf(progress.get(card.id)) === "green").length;
    button.style.setProperty("--mastery", topicCards.length ? green / topicCards.length : 0);
    button.toggleAttribute("data-started", topicCards.some((card) => progress.has(card.id)));
    button.title = `${green} of ${topicCards.length} in Green`;
  }
  if (view === "home") renderHome();
  if (view === "progress") renderProgressView();
  renderSessionChip();
}

function useProgress(next, accountChanged) {
  progress = next;
  if (!cards.length) return;
  renderProgress();
  if (accountChanged && activeDeck === "session") {
    resetQueue({ keepStats: true });
    if (view === "study") renderCard();
  } else if (view === "study") {
    renderBoxChip(queue[position]);
  }
}

function useActivity() {
  if (!cards.length) return;
  if (view === "progress") renderProgressView();
  if (view === "home") renderHome();
}

/* ---------- Home ---------- */

function readExcluded() {
  try {
    const stored = JSON.parse(localStorage.getItem(selectionKey));
    return new Set(Array.isArray(stored) ? stored.filter((id) => typeof id === "string") : []);
  } catch {
    return new Set();
  }
}

function saveExcluded() {
  try { localStorage.setItem(selectionKey, JSON.stringify([...excludedTopics])); } catch {}
}

function selectedCards() {
  return availableCards().filter((card) => !excludedTopics.has(card.topic));
}

function topicsIn(collection) {
  return [...topics.values()].filter((topic) => topic.collection === collection);
}

function greeting() {
  const hour = new Date().getHours();
  return hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
}

function renderHome() {
  if (!cards.length) return;
  const pool = availableCards();
  const chosen = selectedCards();
  const counts = boxCounts(chosen, progress);
  ui["home-greeting"].textContent = greeting();
  const days = account.activity();
  const today = days.get(dayKey()) ?? { n: 0, right: 0 };
  const figures = document.createElement("dl");
  figures.className = "home-figures";
  for (const [label, value] of [["Due now", counts.due], ["Answered today", today.n], ["Day streak", studyStreak(days)]]) {
    const item = document.createElement("div");
    const term = document.createElement("dt");
    term.textContent = label;
    const detail = document.createElement("dd");
    detail.textContent = value;
    item.append(term, detail);
    figures.append(item);
  }
  ui["home-boxes"].replaceChildren(boxBar(counts, { tall: true }), boxLegend(counts, { fresh: counts.fresh }), figures);
  ui["home-due"].textContent = counts.due ? counts.due + " due now" : "Nothing due";
  ui["home-due"].dataset.due = String(counts.due > 0);
  ui["home-selected"].textContent = chosen.length === pool.length ? "All " + pool.length + " cards" : chosen.length + " of " + pool.length + " cards";

  ui["group-picker"].replaceChildren(...collections.map((collection) => {
    const groupTopics = topicsIn(collection).filter((topic) => pool.some((card) => card.topic === topic.id));
    const included = groupTopics.filter((topic) => !excludedTopics.has(topic.id));
    const groupCards = pool.filter((card) => topics.get(card.topic)?.collection === collection && !excludedTopics.has(card.topic));
    const groupCounts = boxCounts(groupCards, progress);
    const row = document.createElement("li");
    row.className = "group-row";
    row.style.setProperty("--hue", collectionHues[collection]);
    row.dataset.state = !included.length ? "off" : included.length === groupTopics.length ? "on" : "some";

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "group-check";
    toggle.dataset.collection = collection;
    toggle.setAttribute("aria-pressed", !included.length ? "false" : included.length === groupTopics.length ? "true" : "mixed");
    const box = document.createElement("span");
    box.className = "check-box";
    box.setAttribute("aria-hidden", "true");
    box.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>';
    const name = document.createElement("span");
    name.className = "group-name";
    name.textContent = deckLabels[collection];
    const count = document.createElement("span");
    count.className = "group-count";
    count.textContent = groupCards.length ? groupCounts.green + " of " + groupCards.length + " green" : "Not included";
    toggle.append(box, name, count);

    const choose = document.createElement("button");
    choose.type = "button";
    choose.className = "group-topics";
    choose.dataset.collection = collection;
    choose.setAttribute("aria-label", "Choose " + deckLabels[collection] + " topics, " + included.length + " of " + groupTopics.length + " chosen");
    choose.innerHTML = '<span></span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>';
    choose.firstChild.textContent = included.length + "/" + groupTopics.length;

    row.append(toggle, choose, boxBar(groupCounts));
    return row;
  }));

  const plan = sessionPlan(chosen, progress);
  ui["start-session"].disabled = !chosen.length;
  ui["start-detail"].textContent = !chosen.length ? "Choose some topics first"
    : plan.due ? plan.due + " due" + (plan.fresh ? ", then new cards" : "")
      : plan.fresh ? plural(plan.fresh, "new card") : "Practise ahead";
  ui["last-session"].textContent = lastSession ? "Saved. Last session: " + sessionSummary(lastSession) + "." : "";
  ui["last-session"].hidden = !lastSession;
}

function toggleCollection(collection) {
  const groupTopics = topicsIn(collection);
  const anyIncluded = groupTopics.some((topic) => !excludedTopics.has(topic.id));
  for (const topic of groupTopics) {
    if (anyIncluded) excludedTopics.add(topic.id);
    else excludedTopics.delete(topic.id);
  }
  saveExcluded();
  renderHome();
}

function openPicker(collection) {
  pickerCollection = collection;
  ui["picker-title"].textContent = deckLabels[collection] + " topics";
  renderPicker();
  ui["topic-picker"].showModal();
}

function renderPicker() {
  const pool = availableCards();
  ui["picker-list"].replaceChildren(...topicsIn(pickerCollection).map((topic) => {
    const topicCards = pool.filter((card) => card.topic === topic.id);
    const item = document.createElement("li");
    const label = document.createElement("label");
    label.className = "picker-item";
    label.style.setProperty("--hue", topicHues[topic.id] ?? topic.hue ?? 155);
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = !excludedTopics.has(topic.id);
    input.dataset.topic = topic.id;
    input.disabled = !topicCards.length;
    const name = document.createElement("span");
    name.className = "picker-name";
    name.textContent = topic.title;
    const meta = document.createElement("span");
    meta.className = "picker-meta";
    const counts = boxCounts(topicCards, progress);
    meta.textContent = topicCards.length ? counts.green + "/" + topicCards.length + " green" : "No questions";
    label.append(input, name, meta);
    item.append(label);
    return item;
  }));
}

/* ---------- Progress page ---------- */

function renderProgressView() {
  renderDashboard(ui.dashboard, {
    cards,
    topics,
    progress,
    activity: account.activity(),
    onPractise: (topicId) => startSession(topicId),
  });
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
  }
}

function renderMode() {
  ui["question-mode"].setAttribute("aria-pressed", String(questionMode));
  ui["flashcard-mode"].setAttribute("aria-pressed", String(!questionMode));
  ui["study-modes"].dataset.active = questionMode ? "questions" : "flashcards";
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
  if (view !== "study") {
    renderMode();
    renderProgress();
    return;
  }
  resetQueue({ keepStats: true });
  if (queue.includes(card)) position = queue.indexOf(card);
  animateSwap(ui["deck-view"], () => {
    renderMode();
    renderProgress();
    renderCard();
  }, ...fade, { out: 120, in: 300 });
}

function renderQuestion(card) {
  let attempt = questionAttempts.get(card);
  if (!attempt) {
    const options = shuffled(card.choices.map((text, index) => ({ text, correct: index === 0 })));
    attempt = { options, wrong: new Set(), outcome: null, firstCorrect: null, move: "" };
    questionAttempts.set(card, attempt);
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

  let message = attempt.wrong.size ? "Not quite. " + attempt.move + " Try another answer." : "";
  if (attempt.outcome === "revealed") message = "Answer shown. " + attempt.move;
  if (attempt.outcome === "correct") message = (attempt.firstCorrect ? "Correct! " : "Correct. ") + attempt.move;
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
  const attempt = questionAttempts.get(card);
  if (!attempt || attempt.outcome || attempt.wrong.has(choiceIndex)) return;
  const revealed = choiceIndex === undefined;
  const correct = !revealed && attempt.options[choiceIndex].correct;
  let saved = true;
  if (attempt.firstCorrect === null) {
    attempt.firstCorrect = correct;
    const result = recordAnswer(card, correct);
    saved = result.saved;
    attempt.move = moveText(result.before, result.after, correct);
    flashMove(result.before, result.after);
    if (!correct) requeue(card);
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
  const inSession = activeDeck === "session";
  const label = questionMode ? (last ? "Finish" : "Next") : inSession ? "Skip" : "Next";
  ui["next-label"].textContent = label;
  ui.next.setAttribute("aria-label", questionMode ? (last ? "Finish round" : "Next question") : inSession ? "Skip this card for now" : "Next card");
  const attempt = questionMode ? questionAttempts.get(queue[position]) : null;
  ui.next.classList.toggle("ready", Boolean(attempt?.outcome));
}

function renderCard(announcement = "") {
  const card = questionRoundFinished ? undefined : queue[position];
  const inSession = activeDeck === "session";
  const topic = inSession ? topics.get(session?.topic) : topics.get(card?.topic ?? activeTopic);
  ui.practice.hidden = !card;
  ui.empty.hidden = Boolean(card);
  const deckName = questionMode && activeDeck === "all" ? "All questions" : deckLabels[activeDeck];
  ui["collection-label"].textContent = inSession ? (questionMode ? "Questions session" : "Flashcard session") : deckName;
  ui["deck-title"].textContent = topic?.title ?? (inSession ? "Today’s cards" : deckName);
  renderMenuButton();
  ui.practice.classList.toggle("in-session", inSession);
  ui.previous.hidden = inSession;
  ui.shuffle.hidden = inSession;
  if (inSession) {
    const dueLeft = queue.slice(position).filter((entry) => isDue(progress.get(entry.id))).length;
    ui["position-label"].textContent = card ? (dueLeft ? dueLeft + " due left" : "New cards") : "";
    ui["deck-progress-fill"].style.transform = `scaleX(${session.due ? 1 - dueLeft / Math.max(session.due, dueLeft) : 1})`;
  } else {
    ui["position-label"].textContent = card ? (position + 1) + " / " + queue.length : "";
    ui["deck-progress-fill"].style.transform = `scaleX(${queue.length ? (position + 1) / queue.length : 0})`;
  }
  ui.shuffle.disabled = queue.length < 2;
  renderSessionChip();
  if (!card) {
    let done = false;
    let message = questionMode ? "There are no questions for this topic." : "There are no cards for this topic in this deck.";
    let action = "Back to home";
    let showHome = false;
    if (inSession) {
      const later = session.ahead.length;
      done = session.stats.done > 0;
      message = done
        ? "That’s everything due for now. This session: " + sessionSummary(session.stats) + "."
        : "Nothing is due in the topics you picked.";
      if (session.stats.up) message += " Cards you moved up come back in a day or more, to check they’ve stuck.";
      if (later) message += " " + plural(later, "card") + (later === 1 ? " is" : " are") + " waiting for later. You can practise them now, but they won’t move up until they’re due.";
      action = later ? "Keep practising" : "Back to home";
      showHome = Boolean(later);
    } else if (questionRoundFinished) {
      const attempted = [...questionAttempts.values()].filter((attempt) => attempt.firstCorrect !== null);
      const correct = attempted.filter((attempt) => attempt.firstCorrect).length;
      done = true;
      message = attempted.length ? `${correct} of ${attempted.length} correct on your first try.` : "You’ve reached the end of this set.";
      action = "Start another round";
      showHome = true;
    }
    ui.empty.dataset.state = done ? "done" : "empty";
    ui["return-to-deck"].textContent = action;
    ui["empty-home"].hidden = !showHome;
    ui["empty-message"].textContent = message;
    ui.announcer.textContent = announcement || message;
    return;
  }

  ui.previous.disabled = position === 0;
  ui.next.disabled = !questionMode && (inSession ? queue.length - position < 2 : position === queue.length - 1);
  renderNextButton();
  if (questionMode) {
    if (displayedQuestion !== questionAttempts.get(card)) ui["question-card"].scrollTop = 0;
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
  renderBoxChip(card);
  const lines = answerVisible ? card.back : frontLines(card);
  ui["card-content"].replaceChildren(...mathLines(lines, answerVisible ? "answer-line" : exam ? "exam-line" : "prompt"));
  ui["card-content"].scrollTop = 0;
  markScrollable();
  ui.announcer.textContent = announcement || (answerVisible ? "Answer shown." : "Question " + (position + 1) + " of " + queue.length + ".");
}

function renderBoxChip(card) {
  if (!card) return;
  const record = progress.get(card.id);
  const box = boxOf(record);
  ui["box-chip"].dataset.box = box;
  ui["box-chip-label"].textContent = record ? boxNames[box] : "Red · new";
  ui["box-chip"].title = record ? "In the " + box + " box" : "Not seen yet. Every card starts in Red.";
  const up = destination(record, true);
  ui["stamp-known-box"].textContent = record && up === box ? "stays " + boxNames[up] : "→ " + boxNames[up];
  ui["stamp-review-box"].textContent = record && box === "red" ? "stays Red" : "→ Red";
}

function renderSessionChip() {
  const inSession = view === "study" && activeDeck === "session" && session;
  ui["session-chip"].hidden = !inSession;
  if (!inSession) return;
  const { done, right } = session.stats;
  ui["session-chip"].replaceChildren();
  const main = document.createElement("span");
  main.textContent = done ? done + " done" : "Session";
  ui["session-chip"].append(main);
  if (done) {
    const extra = document.createElement("span");
    extra.className = "chip-extra";
    extra.textContent = " · " + right + " right";
    ui["session-chip"].append(extra);
  }
}

// Briefly shows where the last card went, above the next card.
let moveTimer;
function flashMove(before, after) {
  const element = ui["box-move"];
  element.dataset.box = after;
  element.textContent = after === before ? (after === "red" ? "Still Red" : "Stays " + boxNames[after]) : boxNames[after] + (boxes.indexOf(after) > boxes.indexOf(before) ? " ↑" : " ↓");
  element.classList.remove("show");
  void element.offsetWidth;
  element.classList.add("show");
  clearTimeout(moveTimer);
  moveTimer = setTimeout(() => element.classList.remove("show"), 1400);
}

function resetQueue({ keepStats = false } = {}) {
  const available = availableCards();
  if (activeDeck === "session") {
    const topic = session?.topic ?? null;
    const pool = topic ? available.filter((card) => card.topic === topic) : selectedCards();
    const plan = sessionPlan(pool, progress, Date.now(), shuffled);
    queue = plan.queue;
    session = {
      topic,
      stats: keepStats && session ? session.stats : { done: 0, right: 0, up: 0, down: 0 },
      ahead: plan.ahead,
      due: plan.due,
    };
  } else {
    queue = available.filter((card) => matchesDeck(card) && (activeTopic === "all" || activeTopic === card.topic));
  }
  position = 0;
  answerVisible = false;
  questionRoundFinished = false;
  questionAttempts.clear();
  displayedQuestion = null;
}

function changeDeck(deck, topic = "all", animate = true) {
  flushMotion();
  activeDeck = deck;
  activeTopic = topic;
  resetQueue();
  renderNav();
  if (animate) animateSwap(ui["deck-view"], () => renderCard(), ...fade, { out: 120, in: 320 });
  else renderCard();
}

function practiseAhead() {
  if (!session?.ahead.length) return goHome();
  flushMotion();
  queue = session.ahead;
  session.ahead = [];
  session.due = 0;
  position = 0;
  answerVisible = false;
  questionRoundFinished = false;
  questionAttempts.clear();
  displayedQuestion = null;
  animateSwap(ui["deck-view"], () => renderCard(), ...fade, { out: 120, in: 320 });
}

/* ---------- Views ---------- */

function viewUrl(next) {
  const url = new URL(window.location.href);
  if (next === "progress") url.searchParams.set("view", "progress");
  else url.searchParams.delete("view");
  if (next !== "study") url.searchParams.delete("card");
  return url;
}

function renderMenuButton() {
  let label = view === "progress" ? "Progress" : "Home";
  let hue = 155;
  if (view === "study") {
    const topic = topics.get(activeDeck === "session" ? session?.topic : activeTopic);
    label = topic?.title ?? (activeDeck === "session" ? "Session" : deckLabels[activeDeck]);
    hue = topicHues[topic?.id] ?? topic?.hue ?? collectionHues[activeDeck] ?? 155;
  }
  ui["menu-label"].textContent = label;
  ui["open-topics"].style.setProperty("--hue", hue);
  ui["open-topics"].setAttribute("aria-label", "Open the menu. You’re on: " + label);
}

function renderNav() {
  for (const link of ui.library.querySelectorAll(".view-link")) {
    if (link.dataset.view === view) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  }
  for (const button of ui.library.querySelectorAll("[data-deck]")) {
    const active = view === "study" && activeDeck !== "session" &&
      button.dataset.deck === activeDeck && (button.dataset.topic ?? "all") === activeTopic;
    button.setAttribute("aria-pressed", String(active));
  }
  renderMenuButton();
}

function setView(next, { push = true } = {}) {
  flushMotion();
  const previous = view;
  if (previous === "study" && next !== "study" && activeDeck === "session" && session?.stats.done) {
    lastSession = { ...session.stats };
    toast("Progress saved. " + sessionSummary(lastSession) + ".");
    session.stats = { done: 0, right: 0, up: 0, down: 0 };
  }
  view = next;
  if (push && previous !== next) {
    history.pushState({ view: next }, "", viewUrl(next));
    navDepth++;
  } else if (!push) {
    history.replaceState({ view: next }, "", viewUrl(next));
  }
  const pages = { home: ui["home-view"], progress: ui["progress-view"], study: ui["deck-view"] };
  for (const [name, element] of Object.entries(pages)) element.hidden = name !== next;
  document.body.dataset.view = next;
  ui["exit-study"].hidden = next !== "study";
  const closeLabel = activeDeck === "session" ? "End session" : "Close";
  ui["exit-study"].setAttribute("aria-label", closeLabel);
  ui["exit-study"].title = closeLabel;
  renderNav();
  renderSessionChip();
  if (next === "home") renderHome();
  if (next === "progress") renderProgressView();
  studyArea.scrollTop = 0;
  if (previous !== next) play(pages[next], fade[1], { duration: 320, easing: easeOut });
}

function goHome() {
  if (view === "home") return;
  if (navDepth > 0) history.back();
  else setView("home", { push: false });
}

function startSession(topicId = null) {
  if (!cards.length) return;
  flushMotion();
  activeDeck = "session";
  activeTopic = "all";
  session = { topic: topicId, stats: { done: 0, right: 0, up: 0, down: 0 }, ahead: [], due: 0 };
  resetQueue();
  setView("study");
  renderCard();
  focusPractice();
}

function browse(deck, topic = "all") {
  const animate = view === "study";
  changeDeck(deck, topic, animate);
  if (view !== "study") setView("study");
  focusPractice();
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
  if (usingPointer || view !== "study") return;
  const target = questionRoundFinished || !queue.length
    ? ui["return-to-deck"]
    : questionMode ? ui["question-prompt"] : ui.flashcard;
  target.focus({ preventScroll: true });
}

function moveCard(direction) {
  if (questionRoundFinished) return;
  flushMotion();
  // In a session, Skip sends the card to the back of the queue.
  if (activeDeck === "session" && !questionMode) {
    if (direction !== 1 || queue.length - position < 2) {
      play(stage(), [
        { transform: "translateX(0)" }, { transform: `translateX(${direction * 10}px)` }, { transform: "translateX(0)" },
      ], { duration: 260, easing: easeOut });
      return;
    }
    queue.push(queue.splice(position, 1)[0]);
    answerVisible = false;
    animateSwap(stage(), () => renderCard("Skipped. It comes back later in this session."), ...slide(1));
    return;
  }
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
  const correct = rating === "known";
  const { saved, before, after } = recordAnswer(card, correct);
  let announcement = (correct ? "Got it. " : "Not yet. ") + moveText(before, after, correct);
  flashMove(before, after);

  if (activeDeck === "session") {
    queue.splice(position, 1);
    if (!correct) requeue(card);
    position = Math.max(0, Math.min(position, queue.length - 1));
    answerVisible = false;
    if (!queue.length) announcement += " That’s everything due.";
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

    const cardId = pageParams.get("card");
    const directCard = cards.find((card) => card.id === cardId);
    if (directCard) {
      const topic = topics.get(directCard.topic);
      changeDeck(topic.collection, topic.id, false);
      if (queue.includes(directCard)) position = queue.indexOf(directCard);
      setView("study", { push: false });
      renderCard();
    } else {
      setView(pageParams.get("view") === "progress" ? "progress" : "home", { push: false });
    }
    renderProgress();
  } catch (error) {
    console.error(error);
    ui.loading.hidden = false;
    ui.loading.replaceChildren("The flashcards couldn’t load. Reload the page to try again.");
  }
}

document.addEventListener("pointerdown", () => { usingPointer = true; }, true);
document.addEventListener("keydown", () => { usingPointer = false; }, true);

ui.library.addEventListener("click", (event) => {
  if (!cards.length) return;
  const link = event.target.closest("button[data-view]");
  const button = event.target.closest("button[data-deck]");
  if (topicsDialog.open && (link || button)) topicsDialog.close();
  if (link) {
    if (link.dataset.view === "home" && view !== "home") goHome();
    else if (link.dataset.view !== view) setView(link.dataset.view);
    return;
  }
  if (button && (view !== "study" || button.getAttribute("aria-pressed") !== "true")) browse(button.dataset.deck, button.dataset.topic);
});
window.addEventListener("popstate", (event) => {
  navDepth = Math.max(0, navDepth - 1);
  const next = event.state?.view ?? "home";
  setView(next === "study" && !queue.length ? "home" : next, { push: false });
  if (next === "study") renderCard();
});
ui["exit-study"].addEventListener("click", goHome);
ui["start-session"].addEventListener("click", () => startSession());
ui["empty-home"].addEventListener("click", goHome);
ui["group-picker"].addEventListener("click", (event) => {
  const button = event.target.closest("button[data-collection]");
  if (!button) return;
  const collection = button.dataset.collection;
  if (button.classList.contains("group-topics")) {
    openPicker(collection);
    return;
  }
  toggleCollection(collection);
  ui["group-picker"].querySelector(`.group-check[data-collection="${collection}"]`)?.focus({ preventScroll: true });
});
ui["picker-list"].addEventListener("change", (event) => {
  const input = event.target.closest("input[data-topic]");
  if (!input) return;
  if (input.checked) excludedTopics.delete(input.dataset.topic);
  else excludedTopics.add(input.dataset.topic);
  saveExcluded();
  renderPicker();
  ui["picker-list"].querySelector(`input[data-topic="${input.dataset.topic}"]`)?.focus({ preventScroll: true });
});
for (const [id, include] of [["picker-all", true], ["picker-none", false]]) {
  ui[id].addEventListener("click", () => {
    for (const topic of topicsIn(pickerCollection)) {
      if (include) excludedTopics.delete(topic.id);
      else excludedTopics.add(topic.id);
    }
    saveExcluded();
    renderPicker();
  });
}
ui["picker-close"].addEventListener("click", () => ui["topic-picker"].close());
ui["picker-done"].addEventListener("click", () => ui["topic-picker"].close());
ui["topic-picker"].addEventListener("close", () => {
  renderHome();
  ui["group-picker"].querySelector(`.group-topics[data-collection="${pickerCollection}"]`)?.focus({ preventScroll: true });
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
  fitFrame = requestAnimationFrame(refit);
});
mobileLayout.addEventListener("change", (event) => {
  if (!event.matches && topicsDialog.open) topicsDialog.close();
  placeHeaderActions();
});
closeOnBackdrop(topicsDialog);
closeOnBackdrop(accountDialog);
closeOnBackdrop(ui["topic-picker"]);

ui.shuffle.addEventListener("click", shuffleCards);
ui["flip-card"].addEventListener("click", flipCard);
ui.previous.addEventListener("click", () => moveCard(-1));
ui.next.addEventListener("click", () => moveCard(1));
ui["know-card"].addEventListener("click", () => rateCard("known"));
ui["review-card"].addEventListener("click", () => rateCard("review"));
ui["return-to-deck"].addEventListener("click", () => {
  if (activeDeck === "session") {
    if (session?.ahead.length) practiseAhead();
    else return goHome();
  } else if (questionRoundFinished) changeDeck(activeDeck, activeTopic);
  else return goHome();
  focusPractice();
});

document.addEventListener("keydown", (event) => {
  if (view !== "study" || topicsDialog.open || accountDialog.open || ui["topic-picker"].open || event.altKey || event.ctrlKey || event.metaKey || !queue.length || questionRoundFinished || event.defaultPrevented) return;
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
    const attempt = questionAttempts.get(queue[position]);
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
  for (const bar of document.querySelectorAll(".box-bar.tall")) fitLabels(bar);
}
document.fonts?.ready.then(refit);
document.fonts?.addEventListener("loadingdone", refit);
renderTheme();
const account = connectAccount(ui, useProgress, toast, useActivity);
start();
// Cards fall due while the page is open, so refresh the counts now and then.
let lastDue = -1;
window.setInterval(() => {
  if (!cards.length || view === "study") return;
  const due = boxCounts(availableCards(), progress).due;
  if (due !== lastDue) renderProgress();
  lastDue = due;
}, 60_000);
