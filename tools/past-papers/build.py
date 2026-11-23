"""Build papers.json from the series files after checking every answer.

Run from the repository root:  python3 tools/past-papers/build.py
Needs sympy (pip install sympy) and node, for the KaTeX check.
A series whose file (and common.py) hasn't changed since its last passing
check is skipped. Pass --force to check every series again.
"""
import hashlib
import importlib
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

# Newest first, so the sidebar lists the most recent papers at the top.
SERIES_MODULES = sorted((p.stem for p in HERE.glob("series_*.py")), reverse=True)
CACHE = HERE / ".checked.json"
LABELS = ("Spot:", "Use:", "Method:", "Answer:", "Answers:", "Watch out:", "Check:", "Key idea:", "Tip:")

# Marks for every part of every question, read from the question papers' "(n)" and
# "(Total for Question n is m marks)" labels: {series: {"p1": {q: [total, [[part, sub, marks], ...]]}}}.
# A part is None where the text layer lost its "(a)" label.
MARKS = json.loads((HERE / "marks.json").read_text())
# Cards whose parts are lettered differently from the paper's. June 2023 P1 Q15 leaves out
# the staircase diagram, the paper's (c), so the paper's (d) and (e) are the card's (c) and (d).
OVERRIDES = {"2023-06-p1-q15": [12, [["a", None, 5], ["b", None, 2], ["c", None, 3], ["d", None, 2]]]}
PART_LABEL = re.compile(r"^\(([a-h])\)")
SUB_LABEL = re.compile(r"(?:^|(?<=[\s)]))\((i|ii|iii|iv|v|vi)\)")


LABEL = re.compile(r"\((?:[a-h]|i{1,3}|iv|v|vi)\)")
# Words that make a label a reference to another part ("using your answer to (a)").
REFERENCE = re.compile(r"\b(?:to|parts?|in|of|from|using|and|or|with|on|see|by|answer|Question)\s+$", re.I)


def split_parts(front):
    """Puts every part on its own line, as the paper does.

    A label starts a new line when it follows the end of a sentence, so "Find $fg(4)$.
    (b) Find $g^{-1}$." becomes two lines, while "using your answer to (a)" stays put.
    Nothing inside $...$ is ever split.
    """
    lines = []
    for text in front:
        start = 0
        in_math = False
        for i, ch in enumerate(text):
            if ch == "$":
                in_math = not in_math
            elif ch == "(" and not in_math and i > start and LABEL.match(text, i) and re.search(r"\s$", text[start:i]) \
                    and not REFERENCE.search(text[start:i]):
                lines.append(text[start:i].rstrip())
                start = i
        lines.append(text[start:])
    return lines


def line_labels(front):
    """The part each front line answers, and its sub-part numerals (None for the stem).

    A question whose parts are numbered (i), (ii) with no letters uses the numerals as parts.
    """
    labels = []
    part = None
    for text in front:
        match = PART_LABEL.match(text)
        sub = SUB_LABEL.match(text)
        if match:
            part = match.group(1)
            labels.append((part, set(SUB_LABEL.findall(text))))
        elif sub and part:
            labels.append((part, set(SUB_LABEL.findall(text))))
        elif sub:
            labels.append((sub.group(1), set()))
        else:
            labels.append((None, set()))
    return labels


def part_marks(front, total, entries, where, notes):
    """Marks to print at the end of each front line, as the paper does, and checks they add up."""
    labels = line_labels(front)
    letters = []
    for part, _ in labels:
        if part and part not in letters:
            letters.append(part)
    marks = [0] * len(front)
    # One mark for the whole question sits at the end of its last line.
    if not letters or (len(entries) == 1 and entries[0][0] is None):
        marks[-1] = total
        return marks, total
    pointer = 0
    for part, sub, value in entries:
        if part is None:
            part = letters[min(pointer, len(letters) - 1)]
            notes.append(f"{where}: unlabelled ({value}) taken as ({part})")
        if part not in letters:
            notes.append(f"{where}: the card leaves out ({part}), so its {value} marks are dropped")
            total -= value
            continue
        pointer = letters.index(part) + 1
        lines = [i for i, (p, _) in enumerate(labels) if p == part]
        exact = [i for i in lines if sub and sub in labels[i][1]]
        marks[(exact or lines)[-1]] += value
    for i, (part, _) in enumerate(labels):
        if part and not any(marks[j] for j, (p, _) in enumerate(labels) if p == part):
            notes.append(f"{where}: the card's ({part}) got no marks")
    assert sum(marks) == total, (where, marks, total)
    return marks, total


def validate(card, where):
    assert card["paper"] in (1, 2), where
    assert isinstance(card["front"], list) and card["front"], where
    assert isinstance(card["back"], list) and len(card["back"]) >= 2, where
    assert card["back"][0].startswith("Spot:"), (where, "the method should open with Spot:")
    choices = card["choices"]
    assert len(choices) == 4 and len(set(choices)) == 4, (where, "needs four different choices")
    for text in card["front"] + card["back"] + choices:
        assert text.count("$") % 2 == 0, (where, "unpaired $", text)
        assert not re.search(r"\s{2,}", text), (where, "double space", text)


def digest(name):
    data = (HERE / f"{name}.py").read_bytes() + (HERE / "common.py").read_bytes()
    return hashlib.sha256(data).hexdigest()


def main():
    force = "--force" in sys.argv
    try:
        cache = {} if force else json.loads(CACHE.read_text())
    except (OSError, ValueError):
        cache = {}
    topics, cards = [], []
    notes = []
    for name in SERIES_MODULES:
        module = importlib.import_module(name)
        series = module.SERIES
        if cache.get(name) == digest(name):
            print(f'{series["title"]}: unchanged, check skipped')
        else:
            module.check()
            cache[name] = digest(name)
            CACHE.write_text(json.dumps(cache, indent=1) + "\n")
        topics.append({"id": series["id"], "title": series["title"], "collection": "papers", "hue": series["hue"]})
        seen = set()
        for c in sorted(module.CARDS, key=lambda c: (c["paper"], c["q"])):
            where = f'{series["title"]} P{c["paper"]} Q{c["q"]}'
            assert (c["paper"], c["q"]) not in seen, (where, "duplicate question")
            seen.add((c["paper"], c["q"]))
            validate(c, where)
            front = split_parts(c["front"])
            out = {
                "id": f'{series["id"].removeprefix("paper-")}-p{c["paper"]}-q{c["q"]:02d}',
                "topic": series["id"],
                "source": f'{series["title"]} · Paper {c["paper"]} · Q{c["q"]}',
                "front": front,
                "back": c["back"],
                "choices": c["choices"],
            }
            if "ask" in c:
                out["ask"] = c["ask"]
            card_id = f'{series["id"].removeprefix("paper-")}-p{c["paper"]}-q{c["q"]:02d}'
            total, entries = OVERRIDES.get(card_id) or MARKS[series["id"]][f'p{c["paper"]}'][str(c["q"])]
            out["marks"], out["total"] = part_marks(front, total, entries, where, notes)
            cards.append(out)
        print(f'{series["title"]}: {len(seen)} questions')

    for note in notes:
        print("note:", note)
    data = {"topics": topics, "cards": cards}
    path = ROOT / "papers.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = subprocess.run(["node", str(HERE / "check_katex.js"), str(path)], capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode:
        print(result.stderr)
        sys.exit("KaTeX check failed")
    print(f"Wrote {len(cards)} cards to {path.name}")


if __name__ == "__main__":
    main()
