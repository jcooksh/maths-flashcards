// Marks a typed or spoken answer to a maths question.
//
// The browser posts the question, its parts and marks, the worked solution and the student's
// answer. The examiner (see _examiner.js) calls the model providers directly; their keys live in
// this Vercel project's environment variables and never reach the browser:
//
//   GROQ_API_KEY     first in line, and the one that also transcribes speech
//   GOOGLE_API_KEY   independent quota, so it covers a Groq rate limit
//   COHERE_API_KEY   slower, later in line
//   NVIDIA_API_KEY   last resort
//
// With none set this returns 503, and the site lets the student mark themselves instead.

const examiner = require("./_examiner.js");
const { cors, allowedOrigin, signedInUser, tooMany, jsonBody } = require("./_shared.js");

const LIMITS = { line: 1500, lines: 40, answer: 6000, parts: 12, marks: 20 };

function validate(body) {
  if (!body) return "bad body";
  const lines = (value) => Array.isArray(value) && value.length > 0 && value.length <= LIMITS.lines &&
    value.every((line) => typeof line === "string" && line.length <= LIMITS.line);
  if (!lines(body.question)) return "bad question";
  if (!lines(body.solution)) return "bad solution";
  if (typeof body.answer !== "string" || !body.answer.trim()) return "bad answer";
  if (body.answer.length > LIMITS.answer) return "answer too long";
  if (!Array.isArray(body.parts) || !body.parts.length || body.parts.length > LIMITS.parts) return "bad parts";
  for (const part of body.parts) {
    if (!part || typeof part.label !== "string" || part.label.length > 20) return "bad part";
    if (part.marks !== null && (!Number.isInteger(part.marks) || part.marks < 1 || part.marks > LIMITS.marks)) return "bad marks";
  }
  return null;
}

module.exports = async (req, res) => {
  if (cors(req, res, "GET, POST, OPTIONS")) return;

  // The site asks whether marking is available before offering it.
  if (req.method === "GET") {
    res.status(200).json({ ok: examiner.examinerConfigured() });
    return;
  }
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
  if (!examiner.examinerConfigured()) {
    res.status(503).json({ error: "examiner unavailable" });
    return;
  }
  if (tooMany("mark:" + user, 12)) {
    res.setHeader("Retry-After", "20");
    res.status(429).json({ error: "slow down" });
    return;
  }

  const body = jsonBody(req);
  const problem = validate(body);
  if (problem) {
    res.status(400).json({ error: problem });
    return;
  }

  const trace = [];
  const started = Date.now();
  try {
    const result = await examiner.mark({
      question: body.question,
      parts: body.parts.map((part) => ({ label: part.label, marks: part.marks })),
      solution: body.solution,
      answer: body.answer.trim(),
      spoken: body.spoken === true,
    }, trace);
    console.log(`[mark] ${result.score}/${result.outOf} in ${((Date.now() - started) / 1000).toFixed(1)}s via ${describe(trace)}`);
    res.status(200).json(result);
  } catch (error) {
    console.error(`[mark] failed after ${((Date.now() - started) / 1000).toFixed(1)}s: ${error.message}`);
    res.status(503).json({ error: "examiner unavailable" });
  }
};

// Which providers served the request, for the logs. No student content.
function describe(trace) {
  return trace.map((step) => `${step.route}${step.ok ? "" : " (declined)"} ${step.ms}ms`).join(" → ") || "no calls";
}
