// Daily study totals for the progress charts.
// Each browser keeps its own days. When signed in it uploads them under its device id,
// and the charts add up every device's days.
export const activityKey = "maths-flashcards.activity.v1";
const deviceKey = "maths-flashcards.device";
const keepDays = 400;
const day = 24 * 60 * 60 * 1000;

const validDay = (value) => /^\d{4}-\d{2}-\d{2}$/.test(value);
const whole = (value) => Number.isSafeInteger(value) && value >= 0;
const validEntry = (entry) => entry && whole(entry.n) && whole(entry.right) && entry.right <= entry.n &&
  whole(entry.red) && whole(entry.amber) && whole(entry.green) && whole(entry.at);

export function deviceId() {
  try {
    let id = localStorage.getItem(deviceKey);
    if (!id || !/^[A-Za-z0-9-]{8,64}$/.test(id)) {
      id = crypto.randomUUID?.() ?? (Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 14));
      localStorage.setItem(deviceKey, id);
    }
    return id;
  } catch {
    return "browser-without-storage";
  }
}

// The local calendar day, so a late-night session counts towards the day it felt like.
export function dayKey(time = Date.now()) {
  const date = new Date(time);
  const pad = (value) => String(value).padStart(2, "0");
  return date.getFullYear() + "-" + pad(date.getMonth() + 1) + "-" + pad(date.getDate());
}

export function readActivity(key = activityKey) {
  try {
    const stored = JSON.parse(localStorage.getItem(key)) ?? {};
    return new Map(Object.entries(stored).filter(([date, entry]) => validDay(date) && validEntry(entry)));
  } catch {
    return new Map();
  }
}

export function saveActivity(activity, key = activityKey) {
  const cutoff = dayKey(Date.now() - keepDays * day);
  for (const date of activity.keys()) if (date < cutoff) activity.delete(date);
  try {
    if (activity.size) localStorage.setItem(key, JSON.stringify(Object.fromEntries(activity)));
    else localStorage.removeItem(key);
    return true;
  } catch {
    return false;
  }
}

// Box counts are a snapshot: the latest one recorded that day wins.
function addDay(total, entry) {
  if (!total) return { ...entry };
  const latest = entry.at > total.at ? entry : total;
  return {
    n: total.n + entry.n,
    right: total.right + entry.right,
    red: latest.red,
    amber: latest.amber,
    green: latest.green,
    at: Math.max(total.at, entry.at),
  };
}

export function recordReview(activity, correct, counts, now = Date.now()) {
  const date = dayKey(now);
  const entry = activity.get(date) ?? { n: 0, right: 0, red: 0, amber: 0, green: 0, at: 0 };
  activity.set(date, {
    n: entry.n + 1,
    right: entry.right + (correct ? 1 : 0),
    red: counts.red,
    amber: counts.amber,
    green: counts.green,
    at: Math.max(now, entry.at + 1),
  });
}

// Moves a guest's days into their account the first time they sign in on this browser.
export function addActivity(activity, extra) {
  for (const [date, entry] of extra) activity.set(date, addDay(activity.get(date), entry));
}

// Totals per day across this browser and the account's other devices.
export function combineActivity(local, others) {
  const days = new Map();
  for (const source of [local, ...others.values()]) {
    for (const [date, entry] of source) days.set(date, addDay(days.get(date), entry));
  }
  return days;
}

export function toRows(activity, since = 0) {
  return Array.from(activity)
    .filter(([, entry]) => entry.at > since)
    .map(([date, entry]) => ({
      day: date, reviews: entry.n, correct: entry.right,
      red: entry.red, amber: entry.amber, green: entry.green, updated_at: entry.at,
    }));
}

export function fromRow(row) {
  const entry = {
    n: row.reviews, right: row.correct, red: row.red, amber: row.amber, green: row.green, at: Number(row.updated_at),
  };
  return validDay(row.day) && validEntry(entry) ? entry : null;
}

// Other devices' days, cached so the charts still show them offline.
export function readOthers(key) {
  try {
    const stored = JSON.parse(localStorage.getItem(key)) ?? {};
    return new Map(Object.entries(stored).map(([device, days]) => [
      device,
      new Map(Object.entries(days).filter(([date, entry]) => validDay(date) && validEntry(entry))),
    ]));
  } catch {
    return new Map();
  }
}

export function saveOthers(others, key) {
  try {
    const plain = Object.fromEntries(Array.from(others, ([device, days]) => [device, Object.fromEntries(days)]));
    localStorage.setItem(key, JSON.stringify(plain));
  } catch {}
}
