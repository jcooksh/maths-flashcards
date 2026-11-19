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

export function studyPlan(cards, progress, now = Date.now()) {
  const missed = [];
  const due = [];
  const newCards = [];
  for (const card of cards) {
    const record = progress.get(card.id);
    if (!record) newCards.push(card);
    else if (record.rating === "review") missed.push(card);
    else if (record.dueAt <= now) due.push(card);
  }

  const oldestFirst = (first, second) => progress.get(first.id).dueAt - progress.get(second.id).dueAt;
  const reviewCount = missed.length + due.length;
  const queue = reviewCount ? [...missed.sort(oldestFirst), ...due.sort(oldestFirst)] : newCards.slice(0, 10);
  return { queue, reviewCount };
}
