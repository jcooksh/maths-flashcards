// Renders every maths segment in a deck file with KaTeX and fails on any error.
const path = require("path");
const katex = require(path.join(__dirname, "..", "..", "assets", "katex", "katex.min.js"));
const data = require(path.resolve(process.argv[2]));

const options = { macros: { "\\cosec": "\\operatorname{cosec}" }, throwOnError: true, strict: "ignore" };
let count = 0;
let problems = 0;
for (const card of data.cards) {
  const front = Array.isArray(card.front) ? card.front : [card.front];
  for (const text of [...front, ...card.back, ...(card.choices || [])]) {
    for (const segment of text.split(/(\$[^$]+\$)/g)) {
      if (!segment.startsWith("$")) continue;
      count++;
      try {
        katex.renderToString(segment.slice(1, -1), options);
      } catch (error) {
        problems++;
        console.log(card.id, segment, error.message);
      }
    }
  }
}
console.log(`KaTeX: ${count} maths segments, ${problems} problems`);
process.exit(problems ? 1 : 0);
