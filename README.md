# Maths flashcards

Quick recall of methods and formulas for Edexcel A level Pure Mathematics (9MA0). Click the card to reveal the answer, or use Space. Arrow keys move between cards.

## Red, amber and green boxes

Every card sits in one of three boxes (a Leitner system). All cards start in **Red**. A right answer moves a card up a box: Red to Amber, then Amber to Green. A wrong answer sends it straight back to Red.

Cards come back on a schedule. Red cards are always due. Amber cards come back a day later. Green cards come back after 3, 7, 14, 30 and then 60 days. A right answer before a card is due keeps it in its box, so cramming can't promote it. It only moves up once it's due again.

## Home, sessions and progress

The home page shows your boxes and lets you choose what to study. Untick a group (Revision, Trig rules, Past papers) to leave it out, or open its topic list to pick individual topics. The choice is remembered on that browser.

**Start** begins an open-ended session:
- Missed (red) cards come first, then amber and green cards that are due, then cards you haven't seen yet, mixed together.
- A missed card comes back a few cards later in the same session.
- Every answer is saved straight away, so you can stop whenever you like with the close button or the back button.
- When nothing is left, you can practise cards early. They won't move up until they're due.

The progress page (`?view=progress`) has:
- the share of cards in Green
- how many cards are due
- your day streak
- how many cards you answered in the last 7 days
- the box split
- cards answered per day
- cards in Green over time
- a breakdown by group and topic
- the topics with the most missed cards, each with a button to practise it

Every chart has a table view and works with the keyboard.

Questions mode sets each card out like the exam paper: the question number, each part on its own line with its marks on the right, and the question's total. Instead of picking from choices, you answer in your own words, so you practise working it out rather than recognising the answer:

- **Say your answer.** It's recorded, written down by Whisper and put in the answer box. Check the transcription and correct it before marking.
- **Or type it.** Write the maths however is easiest, like `x^2` or `root 3`.
- **Mark my answer.** An AI examiner marks each part against the worked solution, as an Edexcel examiner would, and says what to fix. A right answer moves the card up a box; anything else sends it back to Red. Each question counts once towards your boxes.

Speaking and AI marking need you to be signed in. Signed out, or if the examiner can't be reached, you compare your answer with the worked solution and mark it yourself. Show answer gives up on a question, which counts as Red. The Question, Your answer and Marking tabs move between the views. Open Questions directly with `?mode=questions`. The sidebar (or the menu on a phone) also lets you browse any topic card by card.

On a phone every screen fits without scrolling. Anything too long for the screen, such as a long worked solution, is split into pages: tap the arrows or swipe up and down. Formulas too wide for a line are shrunk to fit. The progress page has Overview, Activity and Topics tabs.

### AI marking

Marking runs on [CS Revise's Vercel project](https://github.com/jcooksh/csrevise#maths-flashcards-marking), which holds the model providers' API keys: `api/maths-mark.js` and `api/maths-transcribe.js` there. The site calls them with the signed-in user's Supabase token, and they check it against this project's Supabase before using any quota. The examiner tries Groq (gpt-oss-120b) first, then Google Gemini, Cohere and NVIDIA, and Whisper on Groq writes down spoken answers. No key is ever in the browser. If CS Revise's Vercel project goes, the site falls back to marking answers yourself.

## Trigonometry deck

The trig rules cover every identity and formula in the 9MA0 trigonometry content, in both directions. You expand an identity and also recognise it in reverse. The topics are:

- reciprocal and Pythagorean identities
- compound angles, double and half angles, and the factor formulae
- the R cos(x ± α) form
- exact values and symmetries, and inverse trig
- small angle approximations
- triangles, arcs and sectors
- trig equations
- trig calculus

Cards marked “In the formula booklet” are printed in Pearson’s booklet: compound angles, factor formulae, small angle approximations, and the tan, sec, cot and cosec derivatives and integrals. Cards marked “Recall for the exam” are not printed and must be learned. These include the Pythagorean identities, double angle formulae, sine and cosine rules, arc length and sector area, and the sin and cos derivatives and integrals.

## Past papers

The Past papers section has a card for every question in the Edexcel 9MA0 Pure papers (Papers 1 and 2). Each question is reworded with different numbers, so you won't be doing the same questions when you sit the real papers. The front shows the question. The back gives the method:

- **Spot**: what in the question tells you which technique to use
- **Use**: the formulas or identities you need
- the working for each part, and the answer

In Questions mode, the same reworked questions use a paper-style layout with the question number, part labels, marks and total.

The cards are built from `tools/past-papers/`, with one file per exam series. `python3 tools/past-papers/build.py` recomputes every answer with sympy, checks that all the maths renders, and writes `papers.json`. It also puts each part on its own line and adds the marks for each part and the question's total from `tools/past-papers/marks.json`, which was read from the question papers. Where a card leaves out a part of the paper's question, such as one that needs a diagram, that part's marks are left out too.

## Controls

- Flashcards: click or tap the card (or Space) to flip. Swipe right or press 2 for “Got it”, swipe left or press 1 for “Not yet”. The card shows its box, and the swipe stamp shows where it will go. In a session, Skip moves a card to the back of the queue.
- Questions: press Enter to start typing, Ctrl+Enter or Command+Enter to mark, then Enter for the next question.
- The moon/sun button switches between light and dark mode. It follows the system setting until you choose one.
- Animations are reduced when the system “reduce motion” setting is on.

## Accounts

Ratings are stored in the current browser, so no account is needed. Signing in syncs them across devices. The first sign-in on a browser also includes existing ratings from that browser.

Sign-in uses Supabase Auth with email and password, or Google. The “Continue with Google” button appears automatically once the Google provider is switched on for the project:
1. In Google Cloud, create an OAuth client ID of type *Web application*, with `https://mosmevfnxnnxxmmktfcb.supabase.co/auth/v1/callback` as an authorised redirect URI.
2. Paste its client ID and secret into Supabase under Authentication, then Providers, then Google.
3. Make sure the site URL is in the project's redirect URLs.

Accounts are created by the `create-account` Edge Function, which makes an already-confirmed account so sign-up never waits on an email. Password reset still sends an email; the link returns to the page it was requested from, so add the site URL to the project's Auth redirect URLs. Supabase's built-in email service is heavily rate limited and only delivers to the project's team members, so set up custom SMTP if other people need password resets.

Progress is stored per account by the migrations in `supabase/migrations/`. Daily totals for the charts are kept per browser and uploaded under a device id, so a phone and a laptop add up without counting anything twice. The browser uses the project's publishable API key. Supabase JS 2.119.1 is served locally with its licence in `assets/supabase/`.

## Run locally

Run `python3 -m http.server 8000 --bind 127.0.0.1` from this folder and open `http://127.0.0.1:8000/`.

## Add a flashcard

Edit `cards.json`. Each card has a unique `id`, an existing `topic` ID, a question in `front`, and one or more answer lines in `back`. Use `$…$` around LaTeX. To put a formula on its own line, make it a separate entry in `back`. An optional `reference` of `recall` or `booklet` marks its exam status. Use it only when supported by Pearson's materials.

Write the answer and any essential workings in `back`. Questions mode uses it as the worked solution and the reference for marking.

Cards can be opened directly with `?card=<id>` on the site URL. GitHub Pages publishes changes to the main branch.

KaTeX 0.19.1 and the two variable fonts (Inter and Bricolage Grotesque) are served locally with their licences in `assets/`. Pearson’s specification, content guidance and formula booklet are linked from the site.
