const storeKey = "maths-flashcards.question-reports.v1";

export function readReports(accountId) {
  try {
    const rows = JSON.parse(localStorage.getItem(reportKey(accountId))) ?? [];
    return new Map(rows.filter(([id, row]) => typeof id === "string" &&
      typeof row?.reported === "boolean" && Number.isSafeInteger(row.at) && row.at >= 0));
  } catch {
    return new Map();
  }
}

export function reportKey(accountId) {
  return accountId ? storeKey + "." + accountId : storeKey;
}

export function saveReports(reports, accountId) {
  try {
    localStorage.setItem(reportKey(accountId), JSON.stringify([...reports]));
    return true;
  } catch {
    return false;
  }
}

export function mergeReports(reports, incoming, preferServer = false) {
  let changed = false;
  for (const [id, row] of incoming) {
    const previous = reports.get(id);
    if (!previous || row.at > previous.at || (preferServer && row.at === previous.at && row.reported !== previous.reported)) {
      reports.set(id, row);
      changed = true;
    }
  }
  return changed;
}
