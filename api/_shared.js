// What both endpoints share: which sites may call them, the sign-in check, and a rate limit.

// The flashcards are served from GitHub Pages, so they call these functions cross-origin.
const ORIGINS = new Set([
  "https://jcooksh.github.io",
  "http://127.0.0.1:8000",
  "http://localhost:8000",
]);

// The same Supabase project the site signs in against. Both values are public by design:
// the publishable key is already in the browser.
const SUPABASE_URL = "https://mosmevfnxnnxxmmktfcb.supabase.co";
const SUPABASE_KEY = "sb_publishable_B2CkIOCAUSm_uEg7nN7rAQ_MPAI7XU4";

// Answers the CORS preflight and sets the headers for allowed sites.
// Returns true when the request has been fully handled.
function cors(req, res, methods) {
  const origin = req.headers.origin ?? "";
  if (ORIGINS.has(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", methods);
    res.setHeader("Access-Control-Allow-Headers", "Authorization, Content-Type");
    res.setHeader("Access-Control-Max-Age", "600");
  }
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Content-Type-Options", "nosniff");
  if (req.method === "OPTIONS") {
    res.status(ORIGINS.has(origin) ? 204 : 403).end();
    return true;
  }
  return false;
}

function allowedOrigin(req) {
  return ORIGINS.has(req.headers.origin ?? "");
}

// The providers' free quotas are shared by everyone using the site, so the AI is for signed-in
// users only. Supabase is asked whether the caller's access token is real; the token can't be
// checked here without the project's JWT secret, which must not live in this repo.
async function signedInUser(req) {
  const token = (req.headers.authorization ?? "").replace(/^Bearer\s+/i, "").trim();
  if (!token || token.length > 4000) return null;
  try {
    const response = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
      headers: { Authorization: `Bearer ${token}`, apikey: SUPABASE_KEY },
      signal: AbortSignal.timeout(8000),
    });
    if (!response.ok) return null;
    const user = await response.json();
    return typeof user?.id === "string" ? user.id : null;
  } catch {
    return null;
  }
}

// Per user and per minute. Serverless instances come and go, so this is a floor rather than a
// guarantee; the providers' own quotas are the real ceiling.
const hits = new Map();
function tooMany(key, limit) {
  const now = Date.now();
  const recent = (hits.get(key) ?? []).filter((time) => now - time < 60_000);
  recent.push(now);
  hits.set(key, recent);
  if (hits.size > 5000) hits.clear();
  return recent.length > limit;
}

function jsonBody(req) {
  let body = req.body;
  if (typeof body === "string") {
    try {
      body = JSON.parse(body);
    } catch {
      body = null;
    }
  }
  return body && typeof body === "object" ? body : null;
}

module.exports = { cors, allowedOrigin, signedInUser, tooMany, jsonBody };
