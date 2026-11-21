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
            out = {
                "id": f'{series["id"].removeprefix("paper-")}-p{c["paper"]}-q{c["q"]:02d}',
                "topic": series["id"],
                "source": f'{series["title"]} · Paper {c["paper"]} · Q{c["q"]}',
                "front": c["front"],
                "back": c["back"],
                "choices": c["choices"],
            }
            if "ask" in c:
                out["ask"] = c["ask"]
            cards.append(out)
        print(f'{series["title"]}: {len(seen)} questions')

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
