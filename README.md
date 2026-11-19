# Maths flashcards

Quick recall of methods and formulas for Edexcel A level Pure Mathematics (9MA0). Click the card to reveal the answer, or use Space. Arrow keys move between cards.

Study next starts with missed cards and then cards due for review. When those are done, it offers up to ten new cards. Each correct review increases the time before the next one. A missed card is due straight away.

Maths questions presents four shuffled answer choices for each supported flashcard. The first answer updates the same progress as flashcard practice. Revealing an answer also puts that card in review. You can open Maths questions directly with `?mode=questions`.

Ratings are stored in the current browser and sync across devices when signed in. The first sign-in on a browser also includes existing ratings from that browser. The GitHub Pages site uses Supabase Auth and the account-scoped progress migration in `supabase/migrations/`. The browser uses the project's publishable API key. Supabase JS 2.119.1 is served locally with its licence in `assets/supabase/`.

The site has a single personal sign-in. Initial setup uses a Supabase Auth invitation for the account in `account.js`, and the user chooses their own password. The one-time invitation token is passed in the URL fragment and exchanged on form submission.

## Run locally

Run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder and open `http://127.0.0.1:8000/`.

## Add a flashcard

Edit `cards.json`. Each card has a unique `id`, an existing `topic` ID, a question in `front`, and one or more answer lines in `back`. Use `$…$` around LaTeX. To put a formula on its own line, make it a separate entry in `back`. An optional `reference` of `recall` or `booklet` marks its exam status. Use it only when supported by Pearson's materials.

Include a `choices` array with the correct answer first and three distinct wrong answers to include the card in Maths questions. Match their notation and give each question a single correct choice. The site displays `back` as the explanation.

Cards can be opened directly with `?card=<id>` on the site URL. GitHub Pages publishes changes to the main branch.

KaTeX 0.19.1 and the two variable fonts (Inter and Bricolage Grotesque) are served locally with their licences in `assets/`. Pearson’s specification, content guidance and formula booklet are linked from the site.
