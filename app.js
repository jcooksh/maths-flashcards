"use strict";

const ui = Object.fromEntries(Array.from(document.querySelectorAll("[id]"), (element) => [element.id, element]));
const deckButtons = Array.from(document.querySelectorAll("[data-deck]"));
const storageKey = "maths-flashcards.ratings.v1";
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
let ratings = new Map();
let queue = [];
let activeDeck = "all";
let position = 0;
let answerVisible = false;

function loadRatings() {
  try {
    const stored = JSON.parse(localStorage.getItem(storageKey));
    return new Map(Object.entries(stored ?? {}).filter(([, value]) => value === "review" || value === "known"));
  } catch {
    return new Map();
  }
}

function saveRatings() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(Object.fromEntries(ratings)));
  } catch {
    ui.announcer.textContent += " Progress is available for this session.";
  }
}

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
  if (activeDeck === "review") return ratings.get(card.id) === "review";
  return topics.get(card.topic).collection === activeDeck;
}

function renderProgress() {
  const known = cards.filter((card) => ratings.get(card.id) === "known").length;
  const review = cards.filter((card) => ratings.get(card.id) === "review").length;
  const revision = cards.filter((card) => topics.get(card.topic).collection === "revision").length;
  ui["count-all"].textContent = cards.length;
  ui["count-revision"].textContent = revision;
  ui["count-trigonometry"].textContent = cards.length - revision;
  ui["count-review"].textContent = review;
  ui["known-count"].textContent = known;
  ui["known-total"].textContent = "of " + cards.length;
  ui["known-fill"].style.width = (100 * known / cards.length) + "%";
}

function renderCard(announcement = "") {
  const card = queue[position];
  ui.practice.hidden = !card;
  ui.empty.hidden = Boolean(card);
  ui.shuffle.disabled = queue.length < 2;
  if (!card) {
    const message = activeDeck === "review" && ui.topic.value === "all"
      ? "Your review deck is empty. Choose “Review again” on any answer to add a card here."
      : "There are no cards for this topic in this deck.";
    ui["empty-message"].textContent = message;
    ui.announcer.textContent = announcement || message;
    return;
  }

  ui["position-label"].textContent = (position + 1) + " of " + queue.length;
  ui["position-fill"].style.width = (100 * (position + 1) / queue.length) + "%";
  ui["card-topic"].textContent = topics.get(card.topic).title;
  ui.flashcard.setAttribute("aria-pressed", String(answerVisible));
  ui["card-face-label"].hidden = !answerVisible;
  ui["flip-label"].textContent = answerVisible ? "Show question" : "Show answer";
  ui["reference-label"].hidden = !answerVisible || !card.reference;
  ui["reference-label"].textContent = answerVisible ? referenceLabels[card.reference] ?? "" : "";
  ui.rating.hidden = !answerVisible;
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
  queue = cards.filter((card) => matchesDeck(card) && (ui.topic.value === "all" || ui.topic.value === card.topic));
  position = 0;
  answerVisible = false;
}

function changeDeck(deck) {
  activeDeck = deck;
  for (const button of deckButtons) {
    const active = button.dataset.deck === deck;
    button.setAttribute("aria-pressed", String(active));
    if (active) ui["deck-title"].textContent = button.firstElementChild.textContent;
  }

  ui.topic.replaceChildren(new Option("All topics", "all"));
  for (const topic of topics.values()) {
    if (deck === "all" || deck === "review" || deck === topic.collection) {
      ui.topic.add(new Option(topic.title, topic.id));
    }
  }
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
  if (!card || !answerVisible) return;
  ratings.set(card.id, rating);
  let announcement = rating === "known" ? "Marked as known." : "Added to your review deck.";

  if (activeDeck === "review" && rating === "known") {
    queue.splice(position, 1);
    position = Math.max(0, Math.min(position, queue.length - 1));
    answerVisible = false;
    if (!queue.length) announcement += " No cards left for review in this selection.";
  } else if (position < queue.length - 1) {
    position++;
    answerVisible = false;
  }

  renderProgress();
  renderCard(announcement);
  saveRatings();
  (queue.length ? ui.flashcard : ui["return-to-deck"]).focus();
}

async function start() {
  try {
    const response = await fetch("./cards.json", { cache: "no-cache" });
    if (!response.ok) throw new Error("Flashcard deck request failed");
    const data = await response.json();
    cards = data.cards;
    topics = new Map(data.topics.map((topic) => [topic.id, topic]));
    ratings = loadRatings();

    ui.loading.hidden = true;
    ui.topic.disabled = false;
    renderProgress();
    changeDeck("all");

    const directLink = new URLSearchParams(window.location.search).get("card");
    const directPosition = queue.findIndex((card) => card.id === directLink);
    if (directPosition >= 0) {
      position = directPosition;
      renderCard();
    }
  } catch (error) {
    console.error(error);
    ui.loading.hidden = false;
    ui.loading.textContent = "The flashcards couldn’t load. Reload the page to try again.";
  }
}

for (const button of deckButtons) {
  button.addEventListener("click", () => {
    if (cards.length && activeDeck !== button.dataset.deck) changeDeck(button.dataset.deck);
  });
}
ui.topic.addEventListener("change", () => {
  resetQueue();
  renderCard();
});
ui.shuffle.addEventListener("click", shuffleCards);
ui.flashcard.addEventListener("click", flipCard);
ui.previous.addEventListener("click", () => moveCard(-1));
ui.next.addEventListener("click", () => moveCard(1));
ui["know-card"].addEventListener("click", () => rateCard("known"));
ui["review-card"].addEventListener("click", () => rateCard("review"));
ui["return-to-deck"].addEventListener("click", () => {
  changeDeck("all");
  ui.flashcard.focus();
});
document.addEventListener("keydown", (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey || !queue.length || event.defaultPrevented) return;
  if (event.target.closest("input, select, textarea, [contenteditable]")) return;
  if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    moveCard(event.key === "ArrowLeft" ? -1 : 1);
  } else if (event.code === "Space" && !event.repeat && !event.target.closest("button, a")) {
    event.preventDefault();
    flipCard();
  }
});
start();
