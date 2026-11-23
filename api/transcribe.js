// Turns a spoken answer into text with Whisper on Groq, so the examiner can mark it.
//
// The browser records the answer and posts it here as base64. Nothing is stored: the audio goes
// to Groq and the text comes back. Needs GROQ_API_KEY.

const { cors, allowedOrigin, signedInUser, tooMany, jsonBody } = require("./_shared.js");

const TYPES = { "audio/webm": "webm", "audio/mp4": "m4a", "audio/mpeg": "mp3", "audio/ogg": "ogg", "audio/wav": "wav", "audio/x-m4a": "m4a", "audio/aac": "m4a" };
const MAX_BYTES = 3 * 1024 * 1024;

// Spelling hints. Whisper leans towards these words, so maths comes out as maths.
const HINT = "An A level maths student explains their answer out loud: x squared, cubed, square root, " +
  "over, sine, cosine, tangent, cosec, sec, cot, theta, alpha, beta, pi, e to the power, ln, log, " +
  "dy by dx, differentiate, integrate, equals, plus, minus, times, brackets, part a, part b, part c.";

module.exports = async (req, res) => {
  if (cors(req, res, "POST, OPTIONS")) return;
  if (req.method !== "POST") {
    res.status(405).json({ error: "method not allowed" });
    return;
  }
  if (!allowedOrigin(req)) {
    res.status(403).json({ error: "forbidden" });
    return;
  }
  const user = await signedInUser(req);
  if (!user) {
    res.status(401).json({ error: "sign in required" });
    return;
  }
  const key = (process.env.GROQ_API_KEY || "").trim();
  if (!key) {
    res.status(503).json({ error: "transcription unavailable" });
    return;
  }
  if (tooMany("speech:" + user, 15)) {
    res.setHeader("Retry-After", "20");
    res.status(429).json({ error: "slow down" });
    return;
  }

  const body = jsonBody(req);
  const type = String(body?.type ?? "").split(";")[0].trim().toLowerCase();
  if (!body || typeof body.audio !== "string" || !TYPES[type]) {
    res.status(400).json({ error: "bad audio" });
    return;
  }
  const audio = Buffer.from(body.audio, "base64");
  if (!audio.length || audio.length > MAX_BYTES) {
    res.status(400).json({ error: "audio too long" });
    return;
  }

  const form = new FormData();
  form.append("file", new Blob([audio], { type }), "answer." + TYPES[type]);
  form.append("model", "whisper-large-v3-turbo");
  form.append("language", "en");
  form.append("temperature", "0");
  form.append("response_format", "json");
  form.append("prompt", HINT);
  const started = Date.now();
  try {
    const response = await fetch("https://api.groq.com/openai/v1/audio/transcriptions", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}` },
      body: form,
      signal: AbortSignal.timeout(25_000),
    });
    if (!response.ok) throw new Error(`${response.status} ${(await response.text()).replace(/\s+/g, " ").slice(0, 160)}`);
    const data = await response.json();
    const text = String(data.text ?? "").trim();
    console.log(`[speech] ${audio.length} bytes in ${Date.now() - started}ms`);
    res.status(200).json({ text });
  } catch (error) {
    console.error(`[speech] failed after ${Date.now() - started}ms: ${error.message}`);
    res.status(503).json({ error: "transcription unavailable" });
  }
};
