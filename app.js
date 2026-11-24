import { boxes, boxNames, boxOf, boxCounts, sessionPlan, isDue } from "./progress.js?v=2";
import { connectAccount } from "./account.js?v=5";
import { renderDashboard, boxBar, boxLegend, fitLabels, studyStreak } from "./dashboard.js?v=3";
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
const partLabel = /^\((?:[a-h]|i{1,3}|iv|v|vi)\)(?:\((?:i{1,3}|iv|v|vi)\))?\s+/;

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
  if (accountChanged) {
    flushMotion();
    cancelQuestionTask();
  }
  progress = next;
  if (!cards.length) return;
  renderProgress();
  if (accountChanged && activeDeck === "session") {
    resetQueue({ keepStats: true });
    if (view === "study") renderCard();
  } else if (view === "study") {
    renderBoxChip(queue[position]);
    if (accountChanged && questionMode && queue[position] && !questionRoundFinished) renderQuestion(queue[position]);
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
  cancelQuestionTask();
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

/* ---------- Questions ----------
 * A question is set out like the exam paper. You say or type your answer, an AI examiner marks
 * it against the worked solution, and the result moves the card between boxes. Signed out, or
 * when the examiner can't be reached, you check your answer against the worked solution yourself.
 *
 * Each question has three views: the question ("question"), your answer ("answer") and the
 * marking with the worked solution ("result"). Tabs move between them once there's an answer.
 */
// Marking runs on CS Revise's Vercel project, which holds the AI providers' keys.
const markingApi = "https://csrevise.vercel.app/api/";
const letterLabel = /^\(([a-h])\)\s*/;
const numeralLabel = /^\((i{1,3}|iv|v|vi)\)\s*/;
const longestRecording = 120_000;
const maxRecordingBytes = 3 * 1024 * 1024;
const speechSupported = Boolean(navigator.mediaDevices?.getUserMedia && window.MediaRecorder);
let questionTask = null;

function questionAttempt(card) {
  let attempt = questionAttempts.get(card);
  if (!attempt) {
    attempt = { face: "question", status: "", answer: "", spoken: false, result: null, outcome: null, move: "", firstCorrect: null };
    questionAttempts.set(card, attempt);
  }
  return attempt;
}

// The paper's pieces: each line with its part label, sub-part numeral and marks.
function paperLines(card) {
  const marks = Array.isArray(card.marks) ? card.marks : [];
  let letter = null;
  return frontLines(card).map((text, index) => {
    let rest = text;
    let label = "";
    let sub = "";
    const part = letterLabel.exec(rest);
    if (part) {
      letter = part[1];
      label = "(" + letter + ")";
      rest = rest.slice(part[0].length);
    }
    const numeral = numeralLabel.exec(rest);
    if (numeral) {
      sub = "(" + numeral[1] + ")";
      rest = rest.slice(numeral[0].length);
    }
    return { text: rest, label, sub, letter, marks: marks[index] || 0 };
  });
}

// What the examiner marks: each part that carries marks, or the whole question. When one
// mark covers several sub-parts, as "(c) (i) … (ii) … (3)" does, the part is marked as a whole.
function markingParts(card) {
  const lines = paperLines(card);
  if (!lines.some((line) => line.marks)) return [{ label: "", marks: null }];
  const parts = [];
  let since = [];
  for (const line of lines) {
    since.push(line);
    if (!line.marks) continue;
    const subs = since.filter((other) => other.letter && other.letter === line.letter && other.sub);
    const label = line.letter
      ? "(" + line.letter + ")" + (subs.length > 1 ? "" : line.sub)
      : line.sub;
    parts.push({ label, marks: line.marks });
    since = [];
  }
  return parts;
}

function renderPaper(card) {
  const exam = isExam(card);
  const number = exam ? /Q(\d+)$/.exec(card.source ?? "")?.[1] : null;
  const head = document.createElement("p");
  head.className = "paper-head";
  head.textContent = exam && card.source ? card.source.replace(/ · Q\d+$/, "") : topics.get(card.topic)?.title ?? "Question";
  const lines = paperLines(card).map((line, index) => {
    const row = document.createElement("p");
    // A numeral with no letter before it, as in "(i) Prove that…", is a part of its own.
    const numeralPart = line.sub && !line.letter;
    row.className = "paper-line" + (line.label || numeralPart ? " part" : line.sub ? " sub" : "") + (line.label && line.sub ? " with-sub" : "");
    if (index === 0 && number) {
      const tag = document.createElement("span");
      tag.className = "paper-number";
      tag.textContent = number + ".";
      row.append(tag);
    }
    for (const [text, className] of [[line.label, "paper-label"], [line.sub, "paper-label" + (line.label ? " sub" : "")]]) {
      if (!text) continue;
      const tag = document.createElement("span");
      tag.className = className;
      tag.textContent = text;
      row.append(tag);
    }
    const text = document.createElement("span");
    text.className = "paper-text";
    appendMath(text, line.text, false);
    row.append(text);
    if (line.marks) {
      const marks = document.createElement("span");
      marks.className = "paper-marks";
      marks.textContent = "(" + line.marks + ")";
      marks.setAttribute("aria-label", plural(line.marks, "mark"));
      row.append(marks);
    }
    return row;
  });
  const parts = [head, ...lines];
  if (exam && card.total && number) {
    const total = document.createElement("p");
    total.className = "paper-total";
    total.textContent = `(Total for Question ${number} is ${plural(card.total, "mark")})`;
    parts.push(total);
  }
  ui["question-prompt"].replaceChildren(...parts);
}

function resultElement(tag, className, text) {
  const element = document.createElement(tag);
  element.className = className;
  if (text !== undefined) appendMath(element, text, false);
  return element;
}

const verdictNames = { correct: "Right", partial: "Partly right", wrong: "Not right", missing: "Not answered" };

// The marking: how it went, the examiner's comment on each part, then the worked solution.
function renderResult(card, attempt) {
  const panel = ui["question-result"];
  const result = attempt.result;
  if (!result) {
    panel.replaceChildren();
    return;
  }
  const items = [];
  const banner = document.createElement("p");
  const icon = document.createElement("span");
  icon.className = "result-icon";
  icon.setAttribute("aria-hidden", "true");
  const title = document.createElement("span");
  title.className = "result-title";
  const exam = isExam(card);
  let tone = "neutral";
  if (result.revealed) {
    title.textContent = "Answer shown.";
  } else if (result.self) {
    if (attempt.outcome) {
      tone = attempt.outcome === "correct" ? "right" : "wrong";
      title.textContent = attempt.outcome === "correct" ? "Marked right." : "Marked for review.";
    } else {
      title.textContent = "Check your answer against the worked solution.";
    }
  } else {
    tone = result.correct ? "right" : "wrong";
    title.textContent = result.correct ? "Right" : "Not quite";
  }
  icon.dataset.icon = tone === "right" ? "✓" : tone === "wrong" ? "✗" : "i";
  banner.className = "result-banner " + tone;
  banner.append(icon, title);
  if (!result.self && !result.revealed && exam) {
    const score = document.createElement("span");
    score.className = "result-score";
    score.textContent = result.score + "/" + result.outOf;
    score.setAttribute("aria-label", result.score + " out of " + plural(result.outOf, "mark"));
    banner.append(score);
  }
  items.push(banner);
  if (attempt.move) items.push(resultElement("p", "result-move", attempt.move));
  if (result.self && !attempt.outcome && result.reason) items.push(resultElement("p", "result-note", result.reason));
  if (!result.self && !result.revealed) {
    if (!result.correct && result.overall) items.push(resultElement("p", "result-overall", result.overall));
    const parts = markingParts(card);
    for (const [index, part] of result.parts.entries()) {
      const row = document.createElement("p");
      row.className = "result-part " + part.verdict;
      const head = document.createElement("span");
      head.className = "result-part-head";
      const dot = document.createElement("span");
      dot.className = "result-dot";
      dot.setAttribute("aria-hidden", "true");
      const name = document.createElement("span");
      name.textContent = parts[index]?.label || (result.parts.length > 1 ? "Part " + (index + 1) : "Your answer");
      const verdict = document.createElement("span");
      verdict.className = "result-verdict";
      verdict.textContent = verdictNames[part.verdict] ?? "";
      head.append(dot, name, verdict);
      if (exam) {
        const marks = document.createElement("span");
        marks.className = "result-marks";
        marks.textContent = part.marks + "/" + part.max;
        marks.setAttribute("aria-label", part.marks + " out of " + plural(part.max, "mark"));
        head.append(marks);
      }
      row.append(head);
      const text = resultElement("span", "result-part-text", part.feedback);
      row.append(text);
      items.push(row);
    }
  }
  items.push(resultElement("p", "result-heading keep-with-next", "Worked solution"));
  items.push(...mathLines(card.back, "answer-line"));
  panel.replaceChildren(...items);
}

function setFace(attempt) {
  const box = ui["question-card"];
  box.dataset.face = attempt.face;
  const hasAnswer = Boolean(attempt.answer.trim()) || attempt.face === "answer";
  ui["question-tabs"].hidden = !(hasAnswer || attempt.result) || ["requesting", "recording"].includes(attempt.status);
  ui["tab-answer"].hidden = !hasAnswer;
  ui["tab-result"].hidden = !attempt.result;
  for (const tab of ui["question-tabs"].querySelectorAll("[data-face]")) {
    tab.setAttribute("aria-pressed", String(tab.dataset.face === attempt.face));
  }
}

// The buttons under a question change with the view and with what's happening.
function renderAnswerBar(attempt) {
  const signedIn = account.signedIn();
  const finished = Boolean(attempt.outcome);
  const pendingSelf = Boolean(attempt.result?.self) && !finished;
  const busy = attempt.status;
  const onQuestion = attempt.face === "question";
  const onAnswer = attempt.face === "answer";
  const canSpeak = signedIn && speechSupported && !finished && !pendingSelf && busy !== "marking";

  ui["speak-answer"].hidden = !(canSpeak && (onQuestion || onAnswer));
  ui["speak-answer"].classList.toggle("recording", busy === "recording");
  ui["speak-answer"].disabled = busy === "requesting" || busy === "transcribing";
  const speakLabels = { requesting: "Opening microphone…", recording: "Stop recording", transcribing: "Transcribing…" };
  ui["speak-label"].textContent = speakLabels[busy] ?? (onAnswer ? "Add by speaking" : "Say your answer");
  ui["speak-answer"].setAttribute("aria-pressed", String(busy === "recording"));

  ui["speak-answer"].classList.toggle("compact", onAnswer && busy !== "recording");
  ui["type-answer"].hidden = !onQuestion || finished || pendingSelf || busy !== "";
  ui["type-answer"].classList.toggle("wide", !canSpeak);
  ui["type-answer"].querySelector(".type-label").textContent = canSpeak ? "Type" : "Type your answer";

  ui["mark-answer"].hidden = !onAnswer || finished || pendingSelf || (busy && busy !== "marking");
  ui["mark-answer"].disabled = Boolean(busy);
  ui["mark-answer"].setAttribute("aria-busy", String(busy === "marking"));
  ui["mark-answer"].textContent = busy === "marking" ? "Marking…" : signedIn ? "Mark my answer" : "Check my answer";

  ui["self-mark"].hidden = !pendingSelf || attempt.face !== "result";
  ui["reveal-question"].hidden = finished || pendingSelf || busy !== "" || attempt.face === "result";
  ui["sign-in-to-mark"].hidden = signedIn || !onQuestion || finished || pendingSelf;
  ui["answer-secondary"].hidden = ui["sign-in-to-mark"].hidden && ui["reveal-question"].hidden;

  let status = "";
  if (busy === "recording") status = "Recording " + recordingTime();
  else if (busy === "requesting") status = "Allow microphone access to record.";
  else if (busy === "transcribing") status = "Writing down what you said…";
  else if (busy === "marking" && !onAnswer) status = "The examiner is marking it…";
  const feedback = ui["question-feedback"];
  if (feedback.textContent !== status) feedback.textContent = status;
  const actionsShown = !ui["speak-answer"].hidden || !ui["type-answer"].hidden || !ui["mark-answer"].hidden;
  // Speaking gets the full width, with typing and giving up side by side underneath.
  ui["answer-bar"].dataset.layout = !ui["speak-answer"].hidden && !ui["type-answer"].hidden ? "speak"
    : !ui["type-answer"].hidden ? "type" : onAnswer ? "answer" : "";
  ui["answer-bar"].querySelector(".answer-actions").hidden = !actionsShown;
  ui["answer-bar"].hidden = !actionsShown && ui["self-mark"].hidden && ui["answer-secondary"].hidden && !status;
}

function renderQuestion(card) {
  const attempt = questionAttempt(card);
  const fresh = displayedQuestion !== attempt;
  if (fresh) {
    displayedQuestion = attempt;
    ui["question-card"].classList.toggle("exam", isExam(card));
    renderPaper(card);
    ui["answer-input"].value = attempt.answer;
    const parts = markingParts(card).filter((part) => part.label);
    ui["answer-input"].placeholder = parts.length > 1
      ? "Write each part with any working.\n" + parts.slice(0, 3).map((part) => part.label + " …").join("\n")
      : "Write your answer, with any working.";
  }
  ui["answer-input"].readOnly = Boolean(attempt.outcome || attempt.result || attempt.status);
  const answerHint = attempt.spoken ? "Check your transcription before marking." : "Use notation like x^2 or write it in words.";
  ui["answer-hint"].textContent = attempt.result ? ""
    : account.signedIn() ? answerHint : "You’ll check it against the worked solution. Sign in to have it marked by AI.";
  renderResult(card, attempt);
  setFace(attempt);
  renderAnswerBar(attempt);
  fitFace(attempt);
}

const fitMinimum = { question: 0.8, result: 0.8 };

function fitFace(attempt) {
  const box = ui["question-card"];
  const holder = attempt.face === "result" ? ui["question-result"] : attempt.face === "question" ? ui["question-prompt"] : null;
  if (holder) {
    layoutPages(box, holder, ui["question-pager"], fitMinimum[attempt.face]);
  } else {
    clearPages(box, ui["question-pager"]);
    fitText(box, 1);
  }
  markScrollable();
}

function showFace(face, { animate = true, focus = false } = {}) {
  if (view !== "study" || !questionMode || questionRoundFinished) return;
  flushMotion();
  const card = queue[position];
  const attempt = card && questionAttempts.get(card);
  if (!attempt || attempt.status === "recording" || attempt.status === "requesting") return;
  if (face === "result" && !attempt.result) return;
  const changed = attempt.face !== face;
  attempt.face = face;
  const swap = () => {
    if (changed) ui["question-card"].scrollTop = 0;
    renderQuestion(card);
  };
  if (changed && animate && !focus) animateSwap(ui["question-card"], swap, ...fade, { out: 110, in: 260 });
  else swap();
  if (face === "answer" && focus) ui["answer-input"].focus({ preventScroll: true });
}

function refreshQuestion(card) {
  if (questionMode && view === "study" && !questionRoundFinished && queue[position] === card) {
    renderQuestion(card);
    renderNextButton();
  }
}

// Saves the result of a question, once: the first verdict is the one that counts.
function finishQuestion(card, attempt, correct, outcome = correct ? "correct" : "wrong") {
  if (attempt.firstCorrect !== null) return;
  attempt.firstCorrect = correct;
  attempt.outcome = outcome;
  const result = recordAnswer(card, correct);
  attempt.move = moveText(result.before, result.after, correct) + (result.saved ? "" : " Progress couldn’t be saved on this device.");
  flashMove(result.before, result.after);
  if (!correct) requeue(card);
  renderProgress();
  presentResult(card, attempt);
}

function presentResult(card, attempt) {
  attempt.face = "result";
  animateSwap(ui["question-card"], () => {
    ui["question-card"].scrollTop = 0;
    renderQuestion(card);
    renderNextButton();
    ui["question-result"].focus({ preventScroll: true });
  }, ...fade, { out: 110, in: 280 });
}

function revealAnswer() {
  flushMotion();
  const card = queue[position];
  const attempt = card && questionAttempt(card);
  if (!attempt || attempt.outcome || attempt.status) return;
  attempt.result = { revealed: true };
  finishQuestion(card, attempt, false, "revealed");
}

function selfMark(correct) {
  flushMotion();
  const card = queue[position];
  const attempt = card && questionAttempts.get(card);
  if (!attempt || attempt.face !== "result" || attempt.outcome || !attempt.result?.self) return;
  pulse(correct ? ui["self-right"] : ui["self-wrong"]);
  finishQuestion(card, attempt, correct);
}

function beginQuestionTask(card, attempt, status) {
  const task = { card, attempt, controller: new AbortController() };
  questionTask = task;
  setQuestionTaskStatus(task, status);
  return task;
}

function setQuestionTaskStatus(task, status) {
  task.attempt.status = status;
  refreshQuestion(task.card);
}

function endQuestionTask(task) {
  if (questionTask !== task) return false;
  questionTask = null;
  task.attempt.status = "";
  return true;
}

function cancelQuestionTask() {
  const task = questionTask;
  if (!task) return;
  endQuestionTask(task);
  task.controller.abort();
  task.stop?.();
}

async function callApi(task, path, body, ms) {
  const { signal } = task.controller;
  const timer = setTimeout(() => task.controller.abort(), ms);
  try {
    const token = await account.accessToken();
    if (!token) throw new Error("signin");
    const response = await fetch(markingApi + path, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + token },
      body: JSON.stringify(body),
      signal,
    });
    if (response.status === 401) throw new Error("signin");
    if (!response.ok) throw new Error(response.status === 429 ? "busy" : "unavailable");
    return await response.json();
  } finally {
    clearTimeout(timer);
  }
}

async function markAnswer() {
  flushMotion();
  const card = queue[position];
  const attempt = questionAttempts.get(card);
  if (!attempt || attempt.face !== "answer" || attempt.outcome || questionTask || attempt.result) return;
  const answer = attempt.answer.trim();
  if (!answer) return toast("Say or type your answer first.");
  ui["answer-input"].blur();
  if (!account.signedIn()) {
    attempt.result = { self: true };
    presentResult(card, attempt);
    return;
  }

  const task = beginQuestionTask(card, attempt, "marking");
  const parts = markingParts(card);
  try {
    const result = await callApi(task, "maths-mark", {
      question: frontLines(card),
      parts,
      solution: card.back,
      answer,
      spoken: attempt.spoken,
    }, 65_000);
    if (!Array.isArray(result?.parts) || result.parts.length !== parts.length ||
        typeof result.correct !== "boolean" || !Number.isInteger(result.score) || !Number.isInteger(result.outOf)) {
      throw new Error("unavailable");
    }
    if (!endQuestionTask(task)) return;
    attempt.result = result;
    finishQuestion(card, attempt, result.correct);
  } catch (error) {
    if (!endQuestionTask(task)) return;
    const reasons = {
      signin: "Your sign-in has expired, so check this one yourself. Sign in again to have answers marked.",
      busy: "The examiner is busy, so check this one yourself.",
    };
    attempt.result = { self: true, reason: reasons[error.message] ?? "The examiner couldn’t be reached, so check this one yourself." };
    presentResult(card, attempt);
  }
}

/* ---------- Speaking an answer ----------
 * The answer is recorded in the browser and sent to Whisper, and the words it heard go into the
 * answer box, where they can be checked and corrected before marking.
 */
function recordingTime() {
  const seconds = Math.floor((performance.now() - questionTask.started) / 1000);
  return Math.floor(seconds / 60) + ":" + String(seconds % 60).padStart(2, "0");
}

async function startRecording() {
  flushMotion();
  const card = queue[position];
  const attempt = questionAttempts.get(card);
  if (!attempt || attempt.result || questionTask || !speechSupported || !account.signedIn()) return;
  ui["answer-input"].blur();
  const task = beginQuestionTask(card, attempt, "requesting");
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } });
    task.stop = () => {
      for (const track of stream.getTracks()) track.stop();
    };
    if (questionTask !== task) return task.stop();
    recordSpeech(task, stream);
  } catch {
    if (!endQuestionTask(task)) return;
    task.stop?.();
    toast("Couldn’t open the microphone. Check your browser permissions or type your answer.");
    refreshQuestion(card);
  }
}

function recordSpeech(task, stream) {
  const type = ["audio/webm;codecs=opus", "audio/mp4", "audio/webm", "audio/ogg;codecs=opus"].find((candidate) => MediaRecorder.isTypeSupported?.(candidate));
  const media = type ? new MediaRecorder(stream, { mimeType: type, audioBitsPerSecond: 32_000 }) : new MediaRecorder(stream);
  const chunks = [];
  const releaseMic = task.stop;
  let bytes = 0;
  let timer;
  task.stop = () => {
    clearInterval(timer);
    try {
      if (media.state !== "inactive") media.stop();
    } finally {
      releaseMic();
    }
  };
  media.addEventListener("dataavailable", (event) => {
    if (!event.data.size || questionTask !== task) return;
    chunks.push(event.data);
    bytes += event.data.size;
    if (bytes >= maxRecordingBytes * 0.9) stopRecording();
  });
  media.addEventListener("stop", () => finishRecording(task, chunks, media.mimeType), { once: true });
  media.addEventListener("error", () => {
    if (!endQuestionTask(task)) return;
    task.stop();
    toast("The recording stopped. Try again or type your answer.");
    refreshQuestion(task.card);
  }, { once: true });
  media.start(1000);
  task.started = performance.now();
  setQuestionTaskStatus(task, "recording");
  timer = setInterval(() => {
    if (performance.now() - task.started >= longestRecording) stopRecording();
    else renderAnswerBar(task.attempt);
  }, 1000);
  navigator.vibrate?.(10);
}

function stopRecording() {
  const task = questionTask;
  if (task?.attempt.status !== "recording") return;
  setQuestionTaskStatus(task, "transcribing");
  task.stop();
}

function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(",")[1] ?? "");
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(blob);
  });
}

async function finishRecording(task, chunks, type) {
  if (questionTask !== task) return;
  task.stop();
  const { card, attempt } = task;
  const blob = new Blob(chunks, { type: type || chunks[0]?.type || "audio/webm" });
  if (blob.size > maxRecordingBytes) {
    endQuestionTask(task);
    toast("That recording was too long. Try a shorter answer or type the rest.");
    refreshQuestion(card);
    return;
  }
  if (blob.size < 1500) {
    endQuestionTask(task);
    toast("The recording was too short. Try speaking for a little longer.");
    refreshQuestion(card);
    return;
  }
  setQuestionTaskStatus(task, "transcribing");
  try {
    const audio = await blobToBase64(blob);
    if (questionTask !== task) return;
    const { text } = await callApi(task, "maths-transcribe", { audio, type: blob.type }, 35_000);
    const heard = typeof text === "string" ? text.trim() : "";
    if (!heard) throw new Error("silent");
    if (!endQuestionTask(task)) return;
    const answer = [attempt.answer.trimEnd(), heard].filter(Boolean).join("\n");
    const input = ui["answer-input"];
    attempt.answer = answer.slice(0, input.maxLength);
    attempt.spoken = true;
    attempt.face = "answer";
    input.value = attempt.answer;
    ui["question-card"].scrollTop = 0;
    ui.announcer.textContent = "Transcription ready to review.";
    if (answer.length > input.maxLength) toast("The answer reached its length limit. Check the transcription before marking.");
  } catch (error) {
    if (!endQuestionTask(task)) return;
    toast(error.message === "silent"
      ? "Nothing was heard. Check the microphone and try again."
      : error.message === "signin"
        ? "Sign in again to answer out loud."
        : "That couldn’t be written down. Try again, or type your answer.");
  }
  refreshQuestion(card);
}

/* ---------- Pages ----------
 * When a card's lines don't fit even at the smallest readable size, they're split into pages
 * that each fit. More (or swiping up) shows the next page, so nothing ever scrolls.
 */
const pages = new WeakMap();

function clearPages(box, pager) {
  const state = pages.get(box);
  if (state) for (const line of state.lines) line.hidden = false;
  pages.delete(box);
  box.classList.remove("paged");
  pager.hidden = true;
}

// Splits lines greedily into pages that each fit at one text size, with the pager showing.
function groupLines(box, lines, scale) {
  box.style.setProperty("--fit", String(scale));
  const fits = () => box.scrollHeight <= box.clientHeight + 1;
  const groups = [];
  let group = [];
  for (const line of lines) line.hidden = true;
  for (const line of lines) {
    line.hidden = false;
    group.push(line);
    if (!fits() && group.length > 1) {
      group.pop();
      // A heading never ends a page: it moves over with what it introduces.
      const carried = [];
      while (group.length > 1 && group.at(-1).classList.contains("keep-with-next")) carried.unshift(group.pop());
      for (const shown of group) shown.hidden = true;
      for (const moved of carried) moved.hidden = false;
      groups.push(group);
      group = [...carried, line];
    }
  }
  groups.push(group);
  return groups;
}

function layoutPages(box, holder, pager, min) {
  clearPages(box, pager);
  if (fitText(box, min)) return;
  const lines = Array.from(holder.children);
  box.classList.add("paged");
  pager.hidden = false;
  // Fewest pages at the smallest readable size, unless full-size text needs only one more.
  const smallest = groupLines(box, lines, min);
  let groups = smallest;
  for (const scale of [1, 0.9]) {
    if (scale <= min) continue;
    const larger = groupLines(box, lines, scale);
    if (larger.length <= smallest.length + 1) {
      groups = larger;
      break;
    }
  }
  const fits = () => box.scrollHeight <= box.clientHeight + 1;
  // One text size for every page: the largest that fits them all.
  let scale = 1;
  for (const page of groups) {
    for (const line of lines) line.hidden = !page.includes(line);
    let low = min;
    let high = scale;
    box.style.setProperty("--fit", String(high));
    if (fits()) continue;
    for (let i = 0; i < 6; i++) {
      const middle = (low + high) / 2;
      box.style.setProperty("--fit", middle.toFixed(3));
      if (fits()) low = middle;
      else high = middle;
    }
    scale = low;
  }
  box.style.setProperty("--fit", scale.toFixed(3));
  box.classList.toggle("overflowing", false);
  pages.set(box, { lines, groups, index: 0, pager });
  showPage(box, 0, false);
}

function showPage(box, index, animate = true) {
  const state = pages.get(box);
  if (!state || index < 0 || index >= state.groups.length) return false;
  const apply = () => {
    state.index = index;
    for (const line of state.lines) line.hidden = !state.groups[index].includes(line);
    const label = state.pager.querySelector(".pager-label");
    label.textContent = (index + 1) + " / " + state.groups.length;
    state.pager.querySelector(".pager-prev").disabled = index === 0;
    state.pager.querySelector(".pager-next").disabled = index === state.groups.length - 1;
    fitFormulas(box);
    box.classList.toggle("overflowing", box.scrollHeight > box.clientHeight + 1);
    markScrollable();
  };
  if (animate && motionAllowed(box)) {
    const direction = index > state.index ? 1 : -1;
    const content = box === ui["card-content"] ? box : state.groups[index][0]?.parentElement ?? box;
    animateSwap(content, apply,
      [{ opacity: 1, transform: "translateY(0)" }, { opacity: 0, transform: `translateY(${-direction * 14}px)` }],
      [{ opacity: 0, transform: `translateY(${direction * 18}px)` }, { opacity: 1, transform: "translateY(0)" }],
      { out: 110, in: 260 });
  } else {
    apply();
  }
  ui.announcer.textContent = "Part " + (index + 1) + " of " + state.groups.length + ".";
  return true;
}

// The box whose pages the arrow keys and swipes move through.
function pagedBox() {
  if (view !== "study") return null;
  const box = questionMode ? ui["question-card"] : ui["card-content"];
  return pages.has(box) ? box : null;
}

function turnPage(direction) {
  const box = pagedBox();
  if (!box) return false;
  return showPage(box, pages.get(box).index + direction);
}

// Shrinks a box's text (through --fit) until everything in it fits, so nothing has to scroll.
// If it still doesn't fit at the smallest size, the box is marked as overflowing and scrolls.
// A long formula can't wrap like words can, so shrink any that is wider than its line.
// Otherwise it would stick out of the card and get cut off.
function blockOf(node) {
  let parent = node.parentElement;
  while (parent && /^(inline|contents)$/.test(getComputedStyle(parent).display)) parent = parent.parentElement;
  return parent;
}

function fitFormulas(root) {
  const formulas = Array.from(root.querySelectorAll(".katex"));
  for (const formula of formulas) formula.style.removeProperty("font-size");
  const changes = [];
  for (const formula of formulas) {
    if (!formula.getClientRects().length) continue;
    const holder = blockOf(formula);
    if (!holder) continue;
    const style = getComputedStyle(holder);
    const room = holder.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    const parts = Array.from(formula.querySelectorAll(".katex-base, .base"), (part) => part.getBoundingClientRect());
    if (!parts.length || room <= 0) continue;
    // Unbreakable formulas need their whole width on one line; others only their widest piece.
    const needed = getComputedStyle(formula).whiteSpace === "nowrap"
      ? Math.max(...parts.map((part) => part.right)) - Math.min(...parts.map((part) => part.left))
      : Math.max(...parts.map((part) => part.width));
    if (needed <= room + 0.5) continue;
    const size = parseFloat(getComputedStyle(formula).fontSize) / parseFloat(getComputedStyle(formula.parentElement).fontSize);
    changes.push([formula, size * Math.max(0.5, Math.floor((room / needed) * 100) / 100)]);
  }
  for (const [formula, size] of changes) formula.style.fontSize = size.toFixed(3) + "em";
}

function fitText(box, min = 0.66) {
  if (box.hidden || !box.isConnected) return true;
  for (const formula of box.querySelectorAll(".katex[style]")) formula.style.removeProperty("font-size");
  const fits = () => box.scrollHeight <= box.clientHeight + 1;
  box.style.setProperty("--fit", "1");
  let ok = fits();
  if (!ok) {
    box.style.setProperty("--fit", String(min));
    ok = fits();
    if (ok) {
      let low = min;
      let high = 1;
      for (let i = 0; i < 6; i++) {
        const middle = (low + high) / 2;
        box.style.setProperty("--fit", middle.toFixed(3));
        if (fits()) low = middle;
        else high = middle;
      }
      box.style.setProperty("--fit", low.toFixed(3));
    }
  }
  fitFormulas(box);
  // Smaller formulas can be enough on their own.
  if (!ok) ok = fits();
  box.classList.toggle("overflowing", !ok);
  return ok;
}

// On phones, short answers sit in a 2×2 grid, but only if every one fits on a single line.
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
  layoutPages(ui["card-content"], ui["card-content"], ui["card-pager"], !answerVisible && !exam ? 0.6 : 0.8);
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
  cancelQuestionTask();
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
  if (next !== "study") cancelQuestionTask();
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
  cancelQuestionTask();
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
  const face = questionAttempts.get(queue[position])?.face;
  const target = questionRoundFinished || !queue.length
    ? ui["return-to-deck"]
    : questionMode ? ui[face === "result" ? "question-result" : face === "answer" ? "tab-answer" : "question-prompt"] : ui.flashcard;
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
  if (questionMode && target >= 0 && target <= queue.length) cancelQuestionTask();
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
  cancelQuestionTask();
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
        if (Math.abs(dy) > 36 && pagedBox()) {
          drag = null;
          suppressClickUntil = performance.now() + 400;
          turnPage(dy < 0 ? 1 : -1);
        }
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

// A long question or method is split into pages. On a touch screen a swipe up or down
// turns them, as on flashcards. (With a mouse, dragging still selects text.)
function setupPageSwipe() {
  const box = ui["question-card"];
  let start = null;
  let suppressClickUntil = 0;
  box.addEventListener("pointerdown", (event) => {
    start = event.isPrimary && event.pointerType !== "mouse" && pages.has(box)
      ? { x: event.clientX, y: event.clientY, id: event.pointerId }
      : null;
  });
  box.addEventListener("pointermove", (event) => {
    if (!start || event.pointerId !== start.id) return;
    const dx = event.clientX - start.x;
    const dy = event.clientY - start.y;
    if (Math.abs(dy) > 36 && Math.abs(dy) > Math.abs(dx) * 1.2) {
      start = null;
      suppressClickUntil = performance.now() + 400;
      turnPage(dy < 0 ? 1 : -1);
    }
  });
  const end = () => { start = null; };
  box.addEventListener("pointerup", end);
  box.addEventListener("pointercancel", end);
  // A swipe that ends on an answer or button shouldn't press it.
  box.addEventListener("click", (event) => {
    if (performance.now() < suppressClickUntil) {
      event.preventDefault();
      event.stopPropagation();
    }
  }, true);
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
    // Every card can be a question: you answer it in your own words and it's marked against its solution.
    questionCards = cards.filter((card) => Array.isArray(card.back) && card.back.length > 0);
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
  if (topicsDialog.open && link) topicsDialog.close();
  if (link) {
    if (link.dataset.view === "home" && view !== "home") goHome();
    else if (link.dataset.view !== view) setView(link.dataset.view);
    return;
  }
  if (button?.classList.contains("group-button") && ui["mobile-library"].contains(ui.library)) {
    const open = ui.library.dataset.group === button.dataset.deck;
    if (open) delete ui.library.dataset.group;
    else ui.library.dataset.group = button.dataset.deck;
    for (const group of ui.library.querySelectorAll(".group-button")) {
      group.setAttribute("aria-expanded", String(!open && group === button));
    }
    play(ui.library, fade[1], { duration: 260, easing: easeOut });
    return;
  }
  if (topicsDialog.open && button) topicsDialog.close();
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
ui["speak-answer"].addEventListener("click", () => {
  if (questionTask?.attempt.status === "recording") stopRecording();
  else startRecording();
});
ui["type-answer"].addEventListener("click", () => showFace("answer", { focus: true }));
ui["mark-answer"].addEventListener("click", markAnswer);
ui["sign-in-to-mark"].addEventListener("click", () => account.openSignIn());
ui["self-right"].addEventListener("click", () => selfMark(true));
ui["self-wrong"].addEventListener("click", () => selfMark(false));
ui["reveal-question"].addEventListener("click", revealAnswer);
ui["answer-input"].addEventListener("input", () => {
  const attempt = questionAttempts.get(queue[position]);
  if (!attempt || attempt.outcome || attempt.status) return;
  attempt.answer = ui["answer-input"].value;
});
ui["answer-input"].addEventListener("keydown", (event) => {
  if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
    event.preventDefault();
    markAnswer();
  } else if (event.key === "Escape") {
    ui["answer-input"].blur();
    ui["tab-answer"].focus({ preventScroll: true });
  }
});
window.addEventListener("pagehide", cancelQuestionTask);
window.addEventListener("pageshow", (event) => {
  if (event.persisted && queue[position]) refreshQuestion(queue[position]);
});
for (const pager of [ui["card-pager"], ui["question-pager"]]) {
  pager.addEventListener("pointerdown", (event) => event.stopPropagation());
  pager.addEventListener("click", (event) => {
    event.stopPropagation();
    const button = event.target.closest("button");
    if (button) turnPage(button.classList.contains("pager-next") ? 1 : -1);
  });
}
ui["question-tabs"].addEventListener("click", (event) => {
  const tab = event.target.closest("button[data-face]");
  if (tab) showFace(tab.dataset.face);
});
ui["theme-toggle"].addEventListener("click", toggleTheme);
darkScheme.addEventListener("change", renderTheme);

ui["open-topics"].addEventListener("click", () => {
  // While browsing a topic, the menu opens on that topic's group.
  const browsing = view === "study" && activeDeck !== "session" ? activeDeck : null;
  if (browsing && collections.includes(browsing)) ui.library.dataset.group = browsing;
  else delete ui.library.dataset.group;
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
function scheduleRefit() {
  cancelAnimationFrame(fitFrame);
  fitFrame = requestAnimationFrame(refit);
}
window.addEventListener("resize", scheduleRefit);
window.visualViewport?.addEventListener("resize", scheduleRefit);
let answerHeightBeforeKeyboard = 0;
ui["answer-input"].addEventListener("focus", () => {
  answerHeightBeforeKeyboard = window.visualViewport?.height ?? innerHeight;
});
ui["answer-input"].addEventListener("blur", scheduleRefit);
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
  if ((event.key === "ArrowDown" || event.key === "ArrowUp") && pagedBox()) {
    event.preventDefault();
    turnPage(event.key === "ArrowDown" ? 1 : -1);
  } else if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    moveCard(event.key === "ArrowLeft" ? -1 : 1);
  } else if (!questionMode && event.code === "Space" && !event.repeat && !event.target.closest("button, a")) {
    event.preventDefault();
    flipCard();
  } else if (!questionMode && (key === "1" || key === "2") && !event.repeat) {
    event.preventDefault();
    rateCard(key === "2" ? "known" : "review");
  } else if (questionMode && event.key === "Enter" && !event.target.closest("button, a")) {
    // Enter starts typing an answer, and once it's marked moves on to the next question.
    const attempt = questionAttempts.get(queue[position]);
    if (attempt?.outcome) {
      event.preventDefault();
      moveCard(1);
    } else if (attempt && !attempt.status && !attempt.result) {
      event.preventDefault();
      showFace("answer", { focus: true });
    }
  }
});

setupSwipe();
setupPageSwipe();
placeHeaderActions();
// Math fonts load lazily, so measure the card again once they arrive, and when the screen changes.
function refit() {
  const viewport = window.visualViewport;
  const height = viewport?.height ?? innerHeight;
  const keyboardOpen = mobileLayout.matches && document.activeElement === ui["answer-input"] &&
    answerHeightBeforeKeyboard - height > 100 && (viewport?.scale ?? 1) <= 1.01;
  document.body.toggleAttribute("data-answer-keyboard", keyboardOpen);
  if (keyboardOpen) document.body.style.setProperty("--answer-viewport-height", height + "px");
  else document.body.style.removeProperty("--answer-viewport-height");
  if (view === "study" && queue[position] && !questionRoundFinished) {
    if (questionMode) {
      const attempt = questionAttempts.get(queue[position]);
      if (attempt) fitFace(attempt);
    } else {
      const exam = isExam(queue[position]);
      layoutPages(ui["card-content"], ui["card-content"], ui["card-pager"], !answerVisible && !exam ? 0.6 : 0.8);
    }
  }
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
