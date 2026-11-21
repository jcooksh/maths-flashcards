export const guestKey = "maths-flashcards.progress.v2";
const legacyKey = "maths-flashcards.ratings.v1";
const day = 24 * 60 * 60 * 1000;
const intervals = [1, 3, 7, 14, 30, 60];
const validId = (id) => id.length > 0 && id.length <= 120;

export function readProgress(key = guestKey) {
  try {
    const stored = localStorage.getItem(key);
    if (stored === null && key === guestKey) {
      const legacy = JSON.parse(localStorage.getItem(legacyKey)) ?? {};
      return new Map(Object.entries(legacy)
        .filter(([id, rating]) => validId(id) && (rating === "review" || rating === "known"))
        .map(([id, rating]) => [id, { rating, streak: 0, ratedAt: 0, dueAt: 0 }]));
    }

    const entries = Object.entries(JSON.parse(stored) ?? {});
    return new Map(entries.filter(([id, record]) => validId(id) && record &&
      (record.rating === "review" || record.rating === "known") &&
      Number.isInteger(record.streak) && record.streak >= 0 && record.streak <= intervals.length &&
      Number.isSafeInteger(record.ratedAt) && record.ratedAt >= 0 &&
      Number.isSafeInteger(record.dueAt) && record.dueAt >= record.ratedAt));
  } catch {
    return new Map();
  }
}

export function saveProgress(progress, key = guestKey) {
  try {
    localStorage.setItem(key, JSON.stringify(Object.fromEntries(progress)));
    return true;
  } catch {
    return false;
  }
}

export function mergeProgress(progress, recent, preferIncoming = false) {
  let changed = false;
  for (const [id, record] of recent) {
    const before = progress.get(id);
    const tie = before?.ratedAt === record.ratedAt;
    const same = tie && before.rating === record.rating && before.streak === record.streak && before.dueAt === record.dueAt;
    if (!before || record.ratedAt > before.ratedAt || (preferIncoming && tie && !same)) {
      progress.set(id, record);
      changed = true;
    }
  }
  return changed;
}

export function rateProgress(previous, rating, now = Date.now()) {
  const ratedAt = Math.max(now, (previous?.ratedAt ?? -1) + 1);
  if (rating === "review") return { rating, streak: 0, ratedAt, dueAt: ratedAt };

  if (previous?.rating === "known" && ratedAt < previous.dueAt) {
    return { ...previous, ratedAt };
  }

  const streak = Math.min((previous?.streak ?? 0) + 1, intervals.length);
  return { rating, streak, ratedAt, dueAt: ratedAt + intervals[streak - 1] * day };
}

/* ---------- Leitner boxes ----------
 * Every card starts in the red box. A right answer moves it up one box
 * (red → amber → green); a wrong answer sends it back to red.
 * Amber cards come back after a day, green cards after 3, 7, 14, 30 then 60 days.
 * A right answer before a card is due keeps it where it is, so cramming can't promote it.
 */
export const boxes = ["red", "amber", "green"];
export const boxNames = { red: "Red", amber: "Amber", green: "Green" };

export function boxOf(record) {
  if (!record || record.rating === "review") return "red";
  return record.streak >= 2 ? "green" : "amber";
}

export function isDue(record, now = Date.now()) {
  return Boolean(record) && (record.rating === "review" || record.dueAt <= now);
}

export function boxCounts(cards, progress, now = Date.now()) {
  const counts = { red: 0, amber: 0, green: 0, fresh: 0, due: 0, total: cards.length };
  for (const card of cards) {
    const record = progress.get(card.id);
    counts[boxOf(record)]++;
    if (!record) counts.fresh++;
    else if (isDue(record, now)) counts.due++;
  }
  return counts;
}

// The order cards come up in a session: missed (red) cards first, then amber and green
// cards that are due, then cards not seen yet. Cards that aren't due yet wait in `ahead`.
export function sessionPlan(cards, progress, now = Date.now(), shuffle = (items) => items) {
  const missed = [];
  const due = [];
  const fresh = [];
  const ahead = [];
  for (const card of cards) {
    const record = progress.get(card.id);
    if (!record) fresh.push(card);
    else if (record.rating === "review") missed.push(card);
    else if (record.dueAt <= now) due.push(card);
    else ahead.push(card);
  }
  const at = (card) => progress.get(card.id);
  missed.sort((a, b) => at(a).ratedAt - at(b).ratedAt);
  due.sort((a, b) => (at(a).streak - at(b).streak) || (at(a).dueAt - at(b).dueAt));
  ahead.sort((a, b) => at(a).dueAt - at(b).dueAt);
  return { queue: [...missed, ...due, ...shuffle(fresh)], ahead, due: missed.length + due.length, fresh: fresh.length };
}
