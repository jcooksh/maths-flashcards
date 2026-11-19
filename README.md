# Maths flashcards

Quick recall of methods and formulas for Edexcel A level Pure Mathematics (9MA0). Click the card to reveal the answer, or use Space. Arrow keys move between cards.

Study next starts with missed cards and then cards due for review. When those are done, it offers up to ten new cards. Each correct review increases the time before the next one. A missed card is due straight away.

Questions mode presents four shuffled answer choices for each supported flashcard. The first answer updates the same progress as flashcard practice. Revealing an answer also puts that card in review. You can open Questions directly with `?mode=questions`.

## Controls

- Flashcards: click or tap the card (or Space) to flip. Swipe right or press 2 for “Got it”, swipe left or press 1 for “Not yet”. Arrow keys move between cards.
- Questions: press 1–4 or A–D to answer, Enter for the next question.
- The moon/sun button switches between light and dark mode. It follows the system setting until you choose one.
- Animations are reduced when the system “reduce motion” setting is on.

## Accounts

Ratings are stored in the current browser, so no account is needed. Signing in syncs them across devices. The first sign-in on a browser also includes existing ratings from that browser.

Sign-in uses Supabase Auth with email and password. Accounts are created by the `create-account` Edge Function, which makes an already-confirmed account so sign-up never waits on an email. Password reset still sends an email; the link returns to the page it was requested from, so add the site URL to the project's Auth redirect URLs. Supabase's built-in email service is heavily rate limited and only delivers to the project's team members, so set up custom SMTP if other people need password resets.

Progress is stored per account by the migration in `supabase/migrations/`. The browser uses the project's publishable API key. Supabase JS 2.119.1 is served locally with its licence in `assets/supabase/`.

## Run locally

Run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder and open `http://127.0.0.1:8000/`.

## Add a flashcard

Edit `cards.json`. Each card has a unique `id`, an existing `topic` ID, a question in `front`, and one or more answer lines in `back`. Use `$…$` around LaTeX. To put a formula on its own line, make it a separate entry in `back`. An optional `reference` of `recall` or `booklet` marks its exam status. Use it only when supported by Pearson's materials.

Include a `choices` array with the correct answer first and three distinct wrong answers to include the card in Maths questions. Match their notation and give each question a single correct choice. The site displays `back` as the explanation.

Cards can be opened directly with `?card=<id>` on the site URL. GitHub Pages publishes changes to the main branch.

KaTeX 0.19.1 and the two variable fonts (Inter and Bricolage Grotesque) are served locally with their licences in `assets/`. Pearson’s specification, content guidance and formula booklet are linked from the site.
