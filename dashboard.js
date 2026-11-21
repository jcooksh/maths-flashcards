// The progress page: box split, activity and green-box charts, and a breakdown by group.
// Charts are plain SVG. Every value is also reachable as text: a figure, a legend or a table.
import { boxes, boxNames, boxCounts } from "./progress.js?v=2";
import { dayKey } from "./activity.js?v=1";

const svgNS = "http://www.w3.org/2000/svg";
const dayMs = 24 * 60 * 60 * 1000;
const numberFormat = new Intl.NumberFormat("en-GB");
const shortDate = new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short" });
const longDate = new Intl.DateTimeFormat("en-GB", { weekday: "short", day: "numeric", month: "short" });
const collectionNames = { revision: "Revision", trigonometry: "Trig rules", papers: "Past papers" };
const observers = new WeakMap();

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function svg(tag, attributes = {}) {
  const node = document.createElementNS(svgNS, tag);
  for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, value);
  return node;
}

const format = (value) => numberFormat.format(value);
const plural = (count, word) => format(count) + " " + word + (count === 1 ? "" : "s");
const percent = (part, whole) => (whole ? Math.round((part / whole) * 100) : 0);

/* ---------- Data ---------- */

// The last `count` calendar days, oldest first, as { key, date } pairs.
function lastDays(count, now) {
  const days = [];
  const today = new Date(now);
  for (let offset = count - 1; offset >= 0; offset--) {
    const date = new Date(today.getFullYear(), today.getMonth(), today.getDate() - offset, 12);
    days.push({ key: dayKey(date.getTime()), date });
  }
  return days;
}

export function studyStreak(activity, now = Date.now()) {
  let streak = 0;
  const today = new Date(now);
  // Today doesn't break the streak until it's over.
  let offset = (activity.get(dayKey(now))?.n ?? 0) > 0 ? 0 : 1;
  while (true) {
    const date = new Date(today.getFullYear(), today.getMonth(), today.getDate() - offset, 12);
    if ((activity.get(dayKey(date.getTime()))?.n ?? 0) === 0) return streak;
    streak++;
    offset++;
  }
}

function weekTotals(activity, now) {
  let n = 0;
  let right = 0;
  for (const { key } of lastDays(7, now)) {
    n += activity.get(key)?.n ?? 0;
    right += activity.get(key)?.right ?? 0;
  }
  return { n, right };
}

// Green count per day. Days without study carry the last known count forward,
// and today uses the live count.
function greenSeries(activity, days, liveGreen) {
  const sorted = Array.from(activity).sort(([a], [b]) => (a < b ? -1 : 1));
  let last = null;
  for (const [key, entry] of sorted) if (key < days[0].key) last = entry.green;
  return days.map(({ key }, index) => {
    if (index === days.length - 1) return liveGreen;
    const entry = activity.get(key);
    if (entry) last = entry.green;
    return last;
  });
}

/* ---------- Shared pieces ---------- */

function chartCard(title, subtitle, { table } = {}) {
  const card = el("section", "dash-card");
  const head = el("div", "dash-card-head");
  const titles = el("div", "dash-titles");
  titles.append(el("h2", "dash-title", title));
  if (subtitle) titles.append(el("p", "dash-subtitle", subtitle));
  head.append(titles);
  const body = el("div", "dash-card-body");
  card.append(head, body);
  if (table) {
    const toggle = el("button", "table-toggle", "Table");
    toggle.type = "button";
    toggle.setAttribute("aria-pressed", "false");
    head.append(toggle);
    toggle.addEventListener("click", () => {
      const showing = toggle.getAttribute("aria-pressed") === "true";
      toggle.setAttribute("aria-pressed", String(!showing));
      toggle.textContent = showing ? "Table" : "Chart";
      body.classList.toggle("show-table", !showing);
    });
    body.append(table);
  }
  return { card, body };
}

function dataTable(caption, columns, rows) {
  const wrap = el("div", "dash-table-wrap");
  const table = el("table", "dash-table");
  table.append(el("caption", "visually-hidden", caption));
  const head = el("tr");
  for (const column of columns) {
    const cell = el("th", "", column);
    cell.scope = "col";
    head.append(cell);
  }
  const thead = el("thead");
  thead.append(head);
  table.append(thead);
  const body = el("tbody");
  for (const row of rows) {
    const line = el("tr");
    row.forEach((value, index) => {
      const cell = el(index ? "td" : "th", "", value);
      if (!index) cell.scope = "row";
      line.append(cell);
    });
    body.append(line);
  }
  table.append(body);
  wrap.append(table);
  return wrap;
}

function tooltipFor(container) {
  const tip = el("div", "chart-tip");
  tip.setAttribute("aria-hidden", "true");
  tip.hidden = true;
  container.append(tip);
  return {
    show(lines, x, y) {
      tip.replaceChildren(...lines.map(([strong, label], index) => {
        const line = el("p", index ? "tip-line" : "tip-line tip-main");
        if (strong) line.append(el("strong", "", strong));
        if (label) line.append(document.createTextNode((strong ? " " : "") + label));
        return line;
      }));
      tip.hidden = false;
      const width = container.clientWidth;
      const tipWidth = tip.offsetWidth;
      tip.style.left = Math.max(0, Math.min(width - tipWidth, x - tipWidth / 2)) + "px";
      tip.style.top = Math.max(0, y - tip.offsetHeight - 10) + "px";
    },
    hide() { tip.hidden = true; },
  };
}

// Clean round tick values for a y-axis that starts at zero.
function niceTicks(max, count = 3) {
  if (max <= 0) return [0, 1];
  const rough = max / count;
  const power = 10 ** Math.floor(Math.log10(rough));
  const step = [1, 2, 5, 10].map((m) => m * power).find((value) => value >= rough) ?? 10 * power;
  const ticks = [];
  for (let value = 0; value <= max + step * 0.001; value += step) ticks.push(Math.round(value));
  if (ticks[ticks.length - 1] < max) ticks.push(ticks[ticks.length - 1] + step);
  return ticks;
}

// Redraws a chart whenever its box changes width.
function responsive(container, draw) {
  observers.get(container)?.disconnect();
  let width = 0;
  const observer = new ResizeObserver(([entry]) => {
    const next = Math.round(entry.contentRect.width);
    if (next && next !== width) {
      width = next;
      draw(width);
    }
  });
  observer.observe(container);
  observers.set(container, observer);
}

// Arrow keys move through the points; the focused point shows the same tooltip as hover.
function keyboardPoints(focusable, count, show, hide, describe) {
  let index = count - 1;
  const live = el("p", "visually-hidden");
  live.setAttribute("aria-live", "polite");
  focusable.after(live);
  focusable.addEventListener("focus", () => {
    show(index);
    live.textContent = describe(index);
  });
  focusable.addEventListener("blur", hide);
  focusable.addEventListener("keydown", (event) => {
    const moves = { ArrowLeft: -1, ArrowRight: 1, Home: -count, End: count };
    if (event.key === "Escape") return hide();
    if (!(event.key in moves)) return;
    event.preventDefault();
    index = Math.max(0, Math.min(count - 1, index + moves[event.key]));
    show(index);
    live.textContent = describe(index);
  });
}

/* ---------- Figures ---------- */

function statTile(label, value, detail) {
  const tile = el("div", "stat-tile");
  tile.append(el("p", "stat-label", label), el("p", "stat-value", value));
  if (detail) tile.append(el("p", "stat-detail", detail));
  return tile;
}

// One whole split into the three boxes. Counts print inside a block only when they fit.
export function boxBar(counts, { tall = false } = {}) {
  const bar = el("div", "box-bar" + (tall ? " tall" : ""));
  const total = counts.red + counts.amber + counts.green;
  bar.setAttribute("role", "img");
  bar.setAttribute("aria-label", boxes.map((box) => boxNames[box] + " " + format(counts[box])).join(", "));
  for (const box of boxes) {
    if (!counts[box]) continue;
    const part = el("span", "box-part " + box);
    part.style.flexGrow = counts[box];
    part.title = boxNames[box] + ": " + format(counts[box]) + " (" + percent(counts[box], total) + "%)";
    if (tall) part.append(el("span", "box-part-label", format(counts[box])));
    bar.append(part);
  }
  if (!total) bar.append(el("span", "box-part empty"));
  if (tall) requestAnimationFrame(() => fitLabels(bar));
  return bar;
}

export function fitLabels(bar) {
  for (const label of bar.querySelectorAll(".box-part-label")) {
    label.hidden = false;
    label.hidden = label.scrollWidth + 12 > label.parentElement.clientWidth;
  }
}

export function boxLegend(counts, { fresh } = {}) {
  const list = el("ul", "box-legend");
  for (const box of boxes) {
    const item = el("li", "legend-item");
    item.append(el("span", "swatch " + box), el("span", "legend-name", boxNames[box]), el("strong", "legend-count", format(counts[box])));
    if (box === "red" && fresh) item.append(el("span", "legend-note", "· " + format(fresh) + " not started"));
    list.append(item);
  }
  return list;
}

/* ---------- Charts ---------- */

function columnChart(days, values, rights) {
  const wrap = el("div", "chart");
  const plot = el("div", "chart-plot");
  plot.tabIndex = 0;
  plot.setAttribute("role", "img");
  const total = values.reduce((sum, value) => sum + value, 0);
  plot.setAttribute("aria-label", "Cards answered per day for the last " + days.length + " days, " + plural(total, "card") + " in total. Use the arrow keys to read each day.");
  wrap.append(plot);
  const tip = tooltipFor(wrap);
  const describe = (index) => {
    const n = values[index];
    return longDate.format(days[index].date) + ": " + plural(n, "card") + (n ? ", " + format(rights[index]) + " right first time" : "");
  };
  let columns = [];
  let geometry = null;

  const show = (index) => {
    columns.forEach((column, i) => column.classList.toggle("active", i === index));
    const n = values[index];
    tip.show([
      [plural(n, "card"), ""],
      [n ? format(rights[index]) + " right first time" : "", longDate.format(days[index].date)],
    ], geometry.x(index) + geometry.slot / 2, geometry.top(index));
  };
  const hide = () => {
    columns.forEach((column) => column.classList.remove("active"));
    tip.hide();
  };

  responsive(plot, (width) => {
    const height = 150;
    const axisBand = 22;
    const left = 30;
    const max = Math.max(...values, 0);
    const ticks = niceTicks(Math.max(max, 4));
    const top = ticks[ticks.length - 1];
    const slot = (width - left) / days.length;
    const columnWidth = Math.max(2, Math.min(24, slot - 2));
    const y = (value) => 8 + (height - 8) * (1 - value / top);
    geometry = {
      slot,
      x: (index) => left + index * slot,
      top: (index) => y(values[index]),
    };

    const chart = svg("svg", { width, height: height + axisBand, viewBox: `0 0 ${width} ${height + axisBand}`, "aria-hidden": "true" });
    for (const tick of ticks) {
      chart.append(svg("line", { class: "grid", x1: left, x2: width, y1: y(tick), y2: y(tick) }));
      const label = svg("text", { class: "axis", x: left - 8, y: y(tick) + 4, "text-anchor": "end" });
      label.textContent = format(tick);
      chart.append(label);
    }
    columns = values.map((value, index) => {
      const x = left + index * slot + (slot - columnWidth) / 2;
      const group = svg("g", { class: "column" });
      group.append(svg("rect", { class: "column-hit", x: left + index * slot, y: 0, width: slot, height }));
      if (value > 0) {
        const barTop = y(value);
        const radius = Math.min(4, columnWidth / 2, height - barTop);
        group.append(svg("path", {
          class: "column-bar",
          d: `M${x},${height}V${barTop + radius}Q${x},${barTop} ${x + radius},${barTop}H${x + columnWidth - radius}Q${x + columnWidth},${barTop} ${x + columnWidth},${barTop + radius}V${height}Z`,
        }));
      }
      chart.append(group);
      return group;
    });
    chart.append(svg("line", { class: "baseline", x1: left, x2: width, y1: height, y2: height }));
    const labelEvery = width < 420 ? 14 : 7;
    days.forEach((day, index) => {
      if ((days.length - 1 - index) % labelEvery) return;
      const label = svg("text", { class: "axis", x: left + index * slot + slot / 2, y: height + 16, "text-anchor": index === days.length - 1 ? "end" : "middle" });
      if (index === days.length - 1) label.setAttribute("x", width);
      label.textContent = index === days.length - 1 ? "Today" : shortDate.format(day.date);
      chart.append(label);
    });
    plot.replaceChildren(chart);
  });

  plot.addEventListener("pointermove", (event) => {
    if (!geometry) return;
    const rect = plot.getBoundingClientRect();
    const index = Math.max(0, Math.min(days.length - 1, Math.floor((event.clientX - rect.left - (geometry.x(0))) / geometry.slot)));
    show(index);
  });
  plot.addEventListener("pointerleave", hide);
  keyboardPoints(plot, days.length, show, hide, describe);
  return wrap;
}

function lineChart(days, series) {
  const wrap = el("div", "chart");
  const plot = el("div", "chart-plot");
  plot.tabIndex = 0;
  plot.setAttribute("role", "img");
  const latest = series[series.length - 1] ?? 0;
  plot.setAttribute("aria-label", "Cards in the green box over the last " + days.length + " days, " + format(latest) + " today. Use the arrow keys to read each day.");
  wrap.append(plot);
  const tip = tooltipFor(wrap);
  const first = series.findIndex((value) => value !== null);
  const describe = (index) => longDate.format(days[index].date) + ": " + (series[index] === null ? "no data" : plural(series[index], "card") + " in Green");
  let geometry = null;
  let cursor = null;
  let marker = null;

  const show = (index) => {
    if (!geometry) return;
    const value = series[index];
    const x = geometry.x(index);
    cursor.setAttribute("x1", x);
    cursor.setAttribute("x2", x);
    cursor.style.opacity = 1;
    if (value !== null) {
      marker.setAttribute("cx", x);
      marker.setAttribute("cy", geometry.y(value));
      marker.style.opacity = 1;
    } else {
      marker.style.opacity = 0;
    }
    tip.show([[value === null ? "No data" : plural(value, "card"), ""], ["", longDate.format(days[index].date)]], x, value === null ? 30 : geometry.y(value));
  };
  const hide = () => {
    if (cursor) cursor.style.opacity = 0;
    if (marker) marker.style.opacity = 0;
    tip.hide();
  };

  responsive(plot, (width) => {
    const height = 150;
    const axisBand = 22;
    const left = 30;
    const right = 10;
    const values = series.filter((value) => value !== null);
    const ticks = niceTicks(Math.max(...values, 4));
    const top = ticks[ticks.length - 1];
    const step = (width - left - right) / Math.max(1, days.length - 1);
    const x = (index) => left + index * step;
    const y = (value) => 8 + (height - 8) * (1 - value / top);
    geometry = { x, y };

    const chart = svg("svg", { width, height: height + axisBand, viewBox: `0 0 ${width} ${height + axisBand}`, "aria-hidden": "true" });
    for (const tick of ticks) {
      chart.append(svg("line", { class: "grid", x1: left, x2: width, y1: y(tick), y2: y(tick) }));
      const label = svg("text", { class: "axis", x: left - 8, y: y(tick) + 4, "text-anchor": "end" });
      label.textContent = format(tick);
      chart.append(label);
    }
    chart.append(svg("line", { class: "baseline", x1: left, x2: width, y1: height, y2: height }));
    if (first !== -1) {
      const points = series.map((value, index) => (value === null ? null : [x(index), y(value)])).filter(Boolean);
      const line = points.map(([px, py], index) => (index ? "L" : "M") + px.toFixed(1) + "," + py.toFixed(1)).join("");
      chart.append(svg("path", { class: "area", d: `${line}L${points[points.length - 1][0]},${height}L${points[0][0]},${height}Z` }));
      chart.append(svg("path", { class: "line", d: line }));
      const [endX, endY] = points[points.length - 1];
      chart.append(svg("circle", { class: "end-dot", cx: endX, cy: endY, r: 4 }));
      const endLabel = svg("text", { class: "end-label", x: endX - 8, y: endY - 10, "text-anchor": "end" });
      endLabel.textContent = format(series[series.length - 1]);
      chart.append(endLabel);
    }
    cursor = svg("line", { class: "cursor", y1: 0, y2: height });
    marker = svg("circle", { class: "end-dot hover-dot", r: 4 });
    chart.append(cursor, marker);
    const labelEvery = width < 420 ? 14 : 7;
    days.forEach((day, index) => {
      if ((days.length - 1 - index) % labelEvery) return;
      const label = svg("text", { class: "axis", x: x(index), y: height + 16, "text-anchor": index === days.length - 1 ? "end" : "middle" });
      label.textContent = index === days.length - 1 ? "Today" : shortDate.format(day.date);
      chart.append(label);
    });
    plot.replaceChildren(chart);
    hide();
  });

  plot.addEventListener("pointermove", (event) => {
    if (!geometry) return;
    const rect = plot.getBoundingClientRect();
    const step = days.length > 1 ? geometry.x(1) - geometry.x(0) : 1;
    show(Math.max(0, Math.min(days.length - 1, Math.round((event.clientX - rect.left - geometry.x(0)) / step))));
  });
  plot.addEventListener("pointerleave", hide);
  keyboardPoints(plot, days.length, show, hide, describe);
  return wrap;
}

/* ---------- Page ---------- */

export function renderDashboard(root, { cards, topics, progress, activity, now = Date.now(), onPractise }) {
  const counts = boxCounts(cards, progress, now);
  const streak = studyStreak(activity, now);
  const week = weekTotals(activity, now);
  const days = lastDays(30, now);
  const answered = days.map(({ key }) => activity.get(key)?.n ?? 0);
  const rights = days.map(({ key }) => activity.get(key)?.right ?? 0);
  const greens = greenSeries(activity, days, counts.green);
  const sections = [];

  // Headline figures
  const hero = el("section", "dash-hero");
  const heroFigure = el("div", "hero-figure");
  heroFigure.append(el("p", "hero-value", percent(counts.green, counts.total) + "%"), el("p", "hero-label", "of cards in Green"));
  hero.append(heroFigure);
  const tiles = el("div", "stat-tiles");
  tiles.append(
    statTile("Due now", format(counts.due), counts.due ? "Ready to review" : "Nothing waiting"),
    statTile("Day streak", format(streak), streak === 1 ? "day" : "days"),
    statTile("Last 7 days", format(week.n), week.n ? percent(week.right, week.n) + "% right first time" : "cards answered"),
  );
  hero.append(tiles);
  sections.push(hero);

  // Box split
  const split = chartCard("Your boxes", plural(counts.total, "card") + " across every group");
  split.body.append(boxBar(counts, { tall: true }), boxLegend(counts, { fresh: counts.fresh }));
  split.card.classList.add("dash-boxes");
  sections.push(split.card);

  // Activity
  const activityTable = dataTable("Cards answered per day", ["Day", "Answered", "Right first time"],
    days.slice().reverse().map((day, index) => {
      const i = days.length - 1 - index;
      return [longDate.format(day.date), format(answered[i]), format(rights[i])];
    }));
  const activityCard = chartCard("Cards answered", "Last 30 days", { table: activityTable });
  activityCard.card.classList.add("dash-activity");
  activityCard.body.prepend(columnChart(days, answered, rights));
  sections.push(activityCard.card);

  // Green over time
  const greenTable = dataTable("Cards in Green per day", ["Day", "In Green"],
    days.slice().reverse().map((day, index) => {
      const value = greens[days.length - 1 - index];
      return [longDate.format(day.date), value === null ? "No data" : format(value)];
    }));
  const greenCard = chartCard("Cards in Green", counts.green ? "Last 30 days" : "Last 30 days. A card reaches Green when you get it right again once it’s due, a day after it went Amber.", { table: greenTable });
  greenCard.card.classList.add("dash-green");
  greenCard.body.prepend(lineChart(days, greens));
  sections.push(greenCard.card);

  // Groups, then each group's topics
  const groups = chartCard("By group", "Red, amber and green cards in each group");
  groups.card.classList.add("dash-groups");
  const legend = boxLegend({ red: 0, amber: 0, green: 0 });
  legend.classList.add("compact");
  for (const count of legend.querySelectorAll(".legend-count")) count.remove();
  groups.body.append(legend);
  const list = el("div", "meter-list");
  const byCollection = new Map();
  for (const topic of topics.values()) {
    if (!byCollection.has(topic.collection)) byCollection.set(topic.collection, []);
    byCollection.get(topic.collection).push(topic);
  }
  for (const [collection, collectionTopics] of byCollection) {
    const groupCards = cards.filter((card) => topics.get(card.topic)?.collection === collection);
    const groupCounts = boxCounts(groupCards, progress, now);
    const details = el("details", "meter-group");
    const summary = el("summary", "meter-row");
    summary.append(
      el("span", "meter-name", collectionNames[collection] ?? collection),
      boxBar(groupCounts),
      el("span", "meter-figure", format(groupCounts.green) + " of " + format(groupCounts.total) + " green"),
    );
    details.append(summary);
    const topicList = el("div", "meter-topics");
    for (const topic of collectionTopics) {
      const topicCards = groupCards.filter((card) => card.topic === topic.id);
      if (!topicCards.length) continue;
      const topicCounts = boxCounts(topicCards, progress, now);
      const row = el("div", "meter-row topic-row");
      row.append(
        el("span", "meter-name", topic.title),
        boxBar(topicCounts),
        el("span", "meter-figure", format(topicCounts.green) + " of " + format(topicCounts.total)),
      );
      topicList.append(row);
    }
    details.append(topicList);
    list.append(details);
  }
  groups.body.append(list);
  sections.push(groups.card);

  // Topics with the most missed cards, ready to practise
  const missedBy = new Map();
  for (const card of cards) {
    const record = progress.get(card.id);
    if (record?.rating === "review") missedBy.set(card.topic, (missedBy.get(card.topic) ?? 0) + 1);
  }
  const weakest = [...missedBy].sort((a, b) => b[1] - a[1]).slice(0, 3);
  const focus = chartCard("Needs work", weakest.length ? "Topics with the most cards in Red that you’ve missed" : "");
  focus.card.classList.add("dash-focus");
  if (weakest.length) {
    const focusList = el("ul", "focus-list");
    for (const [topicId, missed] of weakest) {
      const item = el("li", "focus-item");
      const text = el("div", "focus-text");
      text.append(el("p", "focus-name", topics.get(topicId)?.title ?? topicId), el("p", "focus-detail", plural(missed, "missed card")));
      const practise = el("button", "focus-button", "Practise");
      practise.type = "button";
      practise.addEventListener("click", () => onPractise?.(topicId));
      item.append(text, practise);
      focusList.append(item);
    }
    focus.body.append(focusList);
  } else {
    focus.body.append(el("p", "dash-empty", "Nothing here yet. Cards you get wrong will show up here so you can go straight back to them."));
  }
  sections.push(focus.card);

  root.replaceChildren(...sections);
}
