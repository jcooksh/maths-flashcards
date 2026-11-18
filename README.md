# Maths flashcards

Quick recall of methods and formulas for Edexcel A level Pure Mathematics (9MA0). Click the card to reveal the answer, or use Space. Arrow keys move between cards. The review deck and known count use storage in the current browser.

## Run locally

Run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder and open `http://127.0.0.1:8000/`.

## Add a flashcard

Edit `cards.json`. Each card has a unique `id`, an existing `topic` ID, a question in `front`, and one or more answer lines in `back`. Use `$…$` around LaTeX. To put a formula on its own line, make it a separate entry in `back`. An optional `reference` of `recall` or `booklet` marks its exam status. Use it only when supported by Pearson's materials.

Cards can be opened directly with `?card=<id>` on the site URL. GitHub Pages publishes changes to the main branch.

KaTeX 0.19.1 and the two variable fonts (Inter and Bricolage Grotesque) are served locally with their licences in `assets/`. Pearson’s specification, content guidance and formula booklet are linked from the site.
