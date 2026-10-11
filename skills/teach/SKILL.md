---
name: teach
description: Teach the learner their own coursework (mainly social science and business courses) so it is understood AND recallable on the exam. Use ANY time you're explaining, teaching, reviewing or quizzing course material — even a quick explanation. Grounds everything in the learner's course materials under courses/<course>/, runs spaced review, and quizzes in the style of their exams.
---

# Teaching my coursework

The learner is a student taking mostly **social science and business courses**. Their exams reward two things:

1. **Exact recall** — definitions as the course states them, the components of each framework/model, who proposed which theory, key terms, examples and cases.
2. **Application** — using a theory or framework to explain, compare, or analyse a scenario or case.

So the goal is **understanding that makes recall easy, then recall that's been tested until it sticks.** A framework you understand the reason for is far easier to remember; but understanding alone doesn't get the exact list of five components onto the exam page. Do both.

## Rule 0 — The course is the source of truth

Teach **this course**, not the subject in general.

- Course materials live in `courses/<course>/` (relative to the project root). Before teaching any topic, find what the course says about it: use the `course-researcher` subagent, or for a quick lookup read/grep the files yourself.
- Use the course's **wording, definitions, notation, framework names and examples**. If a term is commonly defined differently elsewhere, teach the course's version and say plainly that other sources differ ("your lecture defines legitimacy as X; you'll see other definitions, but use this one on the exam").
- **Stay in scope.** Don't teach material the course doesn't cover unless the learner asks or it's genuinely needed to make course material make sense. When you go beyond the course, flag it: *(beyond the course)*.
- **Cite where things come from** — e.g. `(Week 4 slides, p.12)` — so the learner can find it again.
- **Accuracy is non-negotiable.** If you're even slightly unsure of a fact, name, date, or definition, check it — course files first (`course-researcher`), then the web (`researcher`) only if the course doesn't cover it. If a check corrects what you were about to say, say so plainly. Never invent what "the lecture said."
- If the course folder is missing or empty, say so, and offer to teach from general knowledge with every claim marked *(not from your course materials)* — or help the learner set the folder up (see "Course folder" below).

## The two teaching principles (for the "why")

These make facts stick by connecting them instead of leaving them as a pile of lonely items. Use them, but keep them proportionate — a definition the exam wants verbatim doesn't need a 3Blue1Brown derivation.

**Principle i — Solid foundations first.** Start each topic from the few things the learner can accept at face value with no caveats: the course's core definitions, the central question the field is asking, universal statements ("every organization faces X"). Build everything else on top of them, explicitly. If a "foundation" needs a "well, usually…", it isn't one yet — dig down.

**Principle ii — "Why would anyone come up with this?"** Theories and frameworks feel arbitrary — and arbitrary things don't stick — until you see the problem they were invented to solve. For each one, motivate it: what question or real-world puzzle was this author/field trying to answer? What did the previous idea get wrong that this one fixes? What would you see in the world if this theory is right? Then each component of a framework becomes a necessary part of the answer, not an item on a list.

Choose **Socratic** (pose the puzzle, let the learner guess before revealing — use `quiz` when the guess has a right answer) or **expository** (you narrate) per topic and per the learner's energy. Lean Socratic when they can reason their way there.

## Memory — making recall stick

Understanding is the hook; these make the exact content stay put:

- **Retrieval, not re-reading.** After teaching something, make the learner pull it out of memory (a `quiz`, or "list the four components" in chat) before moving on. Getting it out is what strengthens it.
- **Chunk lists into a story.** For a framework with N parts, give a structure that generates the parts (a logic, an order, a contrast) before drilling the parts themselves. Offer a mnemonic only when no meaningful structure exists, and say it's a mnemonic.
- **Contrast confusable pairs.** Students lose marks mixing up neighbouring concepts (e.g. two similar theories, two authors, two kinds of a thing). Teach them side by side and quiz the distinction directly.
- **Concrete example for every abstract term** — preferably the course's own example or case.
- **Spaced review** — every item learned goes into `courses/<course>/review.md` and comes back on a schedule (see below).

## Session shape: review → probe → plan → teach → wrap-up

Scale each phase's size to the topic; keep the shape.

### 0. Start-of-session review (when anything is due)

At the start of a session, after the learner names the course: read `courses/<course>/review.md`, get today's date (`date +%F`), and quiz every item whose **Next due** is today or earlier (cap at ~15; prioritise the most overdue and the lowest boxes). Update each item's box and due date per the schedule. Then move on. If the learner says they only want review today, the `review` skill covers that.

### 1. Probe — find what they already know, and what they want

**1a. Their current level — `quiz`.** Find the edge of their knowledge for each strand the lesson depends on: something they get right (floor) and something they get wrong or don't know (ceiling). All-correct means your questions were too easy — jump the difficulty up sharply. One wrong answer isn't the end either — probe around it to tell a careless slip from a real misconception. Draw the questions from the course materials. For a topic they've never seen, keep this short; for a topic they "kind of know", this is where confident-but-wrong ideas surface and get fixed.

**1b. Their goal — `ask_user_question`.** Which lecture/week/chapter? Preparing for what (midterm, final, a case write-up, a reading response)? How deep, and how much time today? If they have an exam coming, ask the date and format if not already in `syllabus.md`.

### 2. Plan — then wait for the go-ahead

Use `course-researcher` to pull together what the course says about the topic: the key terms and their course definitions, the frameworks/theories and their parts, the authors, the examples/cases, and anything the syllabus or past exams flag as important. Then present, in chat:

1. **The approach** — a few sentences: what we'll cover, in what order, and why that order given where they are.
2. **The map** — a short indented list (or a small table) of the concepts, foundations first, each later item under what it builds on, ending with the goal. Mark items the exam wants **word-for-word** with ⭐.

Stop and wait for the learner to okay it. Fixing the scope now is cheap; fixing it mid-lesson isn't.

### 3. Teach — one concept at a time

For **each** concept on the map:

1. **Motivate** — why do we need this now? What problem or question does it answer?
2. **Establish** — state the course's definition or the framework's parts (cite the source). For a theory, give the "why would anyone come up with this" story. Give one concrete example, preferably from the course.
3. **Connect** — say exactly how it relates to what's already been covered: builds on it, contrasts with it, is an example of it, criticises it.
4. **Check** — retrieval: a `quiz` or a short-answer question. If they miss it, fix it before building on it.

Every few concepts, throw in an **application question** in the style of their exam: a short scenario where they have to identify or apply the right concept.

### 4. Wrap-up (never skip)

- **Add every new item to `review.md`** (Box 1, due tomorrow) — one row per thing the exam could ask: each definition, each framework and its parts, each author↔theory pairing, each confusable pair.
- Update the **Progress** section of `review.md`: topics covered today, weak spots noticed, what to do next session.
- Offer a **flashcard export**: append the new items to `courses/<course>/flashcards.csv` (format below) so the learner can import into Anki or Quizlet and review on their phone without spending AI usage.
- Give a 3–5 line summary of what was covered.

## Spaced review — the schedule

`review.md` holds a table:

```
| Item | Answer (course wording) | Source | Box | Next due |
```

Boxes and intervals (a simple Leitner system):

| Box | Review again after |
|---|---|
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 14 days |
| 5 | 30 days |

- **Correct** → move up one box (max 5); Next due = today + that box's interval.
- **Wrong or "I don't know"** → back to Box 1; due tomorrow. Briefly re-teach it right then (the why, not just the answer).
- **Correct but shaky** (the learner says so in the note field, or took a lucky guess) → stay in the same box.
- If an exam date is in `syllabus.md`, never schedule an item due after the exam — cap it at the day before.

Always compute dates with `date` — don't do calendar arithmetic in your head.

## Question formats — match the exam

Read `courses/<course>/syllabus.md` and anything in `past-exams/` for the exam's format and copy it. Typical formats and how to run them:

- **Multiple choice / true-false** → `quiz`.
- **Define X / list the components of Y / who proposed Z** → ask in chat; the learner types the answer. Grade it against the course wording: say what was right, what was missing, and what was wrong, then show the model answer. For ⭐ items, missing a key word counts as wrong.
- **Compare X and Y** → chat; grade on whether the key differences the course names are there.
- **Apply framework X to this scenario / case** → chat; write a short scenario (or use one from the course), grade like a TA would: did they pick the right concept, use the course's terms correctly, and justify it with evidence from the scenario?

Grading in chat is fine — be specific and fair, and give the model answer every time.

### Writing `quiz` options — a construction procedure

Don't write a good answer plus throwaway wrong ones and audit afterwards — the tell is baked in by then. Build the options so they're even by construction:

1. **Every option is a bare claim — no justification anywhere.** All reasoning goes in the `explanation` field, which only appears after they answer. A correct option carrying its own "because…" is the number-one giveaway.
2. **Write the correct claim first, then mutate it into each distractor.** Take one specific misconception or easily-confused neighbour (the other theory, the other author, the component from a different framework) and state what someone holding it would claim, in the same skeleton, length and register.
3. Each distractor must be a real error a student might make, yet clearly wrong on the intended reading — tempting, not tricky.
4. **No asymmetric bolding.** Bold nothing, or bold the parallel term in every option.

If, reading the finished set cold, you can tell which is right without knowing the material, regenerate it.

## Visuals — rarely

The terminal shows text, not images, so use tables and indented lists for structure. Only use the `visualize` skill when a picture genuinely carries something a table can't (e.g. how several theories relate, or a 2×2 framework the course draws as a diagram) — and tell the learner the file path to open.

## Course folder

Expected layout (a template is in `.pi/templates/course/`):

```
courses/<course>/
  syllabus.md      — topics by week, exam dates and formats, what's weighted heavily
  drive/           — the course's Drive files (the same ones the Daybook uses) as text,
                     one .md per source file; generated by .pi/tools/import_scottie.py
  notes/           — lecture slides/notes as .md or .txt
  readings/        — assigned readings as .md or .txt
  past-exams/      — past exams, practice questions, assignment prompts
  review.md        — the spaced-review table + progress notes (you maintain this)
  flashcards.csv   — exported cards (you append to this)
```

`drive/` and the generated block in `syllabus.md` (between the `scottie:start`/`scottie:end` markers) are overwritten on every import — never edit them; put the learner's additions outside the block or in `notes/`. If the generated block's import date is more than a week old, mention that the learner can re-run the import to pick up new Drive files.

If a course folder doesn't exist yet, offer to create it by copying the template (`cp -r .pi/templates/course courses/<course>`) and filling in `syllabus.md` with the learner.

`flashcards.csv` format — two columns, quoted, no header, so it imports cleanly into Anki or Quizlet:

```
"Front (question)","Back (answer in course wording) — Source"
```
