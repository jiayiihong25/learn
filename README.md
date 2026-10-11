# learn

[![video](assets/thumbnail.png)](https://www.youtube.com/watch?v=kzcI5F4tGiU)

My AI learning system from this video: [How I Use AI to Learn Things](https://www.youtube.com/watch?v=kzcI5F4tGiU).

This is a personal system I built for myself, shared as-is. Built as a pi configuration: the teaching philosophy encoded in a skill, a few small extensions, and agent definitions.

> **This fork** is adapted to teach **my own coursework** (mostly social science and business courses that reward exact recall + applying frameworks), running on a **ChatGPT Plus (Codex) subscription** instead of an API key, with **no Obsidian** required. See [My setup](#my-setup) below.

## My setup

### 1. Install pi and log in with ChatGPT

```bash
npm install -g @mariozechner/pi-coding-agent
```

Make a learning project and put this repo in it as `.pi`:

```bash
mkdir ~/learning && cd ~/learning
git clone -b claude/zealous-carson-7a48q3 https://github.com/jiayiihong25/learn .pi
pi
```

Inside pi, run `/login` and choose **ChatGPT Plus/Pro (Codex)**. Then `/model` to pick a model. The agents in `agents/` don't pin a model, so subagents use whatever you're logged into. To save usage, you can add a `model:` line to an agent's frontmatter pointing at a smaller model from the `/model` list.

### 2. Add a course

```bash
cp -r .pi/templates/course courses/<course-code>
```

Then fill it in:

- `syllabus.md` — exam dates, formats and weights, weekly topics, anything flagged "important". The exam format matters most: the tutor copies it when quizzing.
- `notes/`, `readings/` — lecture slides/notes and readings **as text** (`.md` or `.txt`). The tutor can't search PDFs or slides directly; convert them first, e.g. with [markitdown](https://github.com/microsoft/markitdown):
  ```bash
  pip install 'markitdown[all]'
  markitdown week04-slides.pptx -o courses/<course-code>/notes/week04.md
  markitdown chapter3.pdf -o courses/<course-code>/readings/chapter3.md
  ```
- `past-exams/` — past exams, practice questions, assignment prompts (also as text).
- `review.md` and `flashcards.csv` — leave as they are; the tutor fills them in.

Resulting layout:

```
~/learning/
  .pi/                 ← this repo
  courses/
    <course-code>/
      syllabus.md
      notes/  readings/  past-exams/
      review.md        ← spaced-review schedule + progress (tutor-maintained)
      flashcards.csv   ← import into Anki / Quizlet
```

### 2b. Or import your courses from the Daybook (scottie)

If you have a local checkout of [scottie](https://github.com/jiayiihong25/scottie) with its Drive service-account `.env` set up, you don't need to fill in course folders by hand. The importer reuses what scottie already pulls from the "JiaYi Courses" Drive folder for the Daybook:

```bash
# in the scottie checkout: download from Drive and extract text (no model calls, doesn't advance pacing)
python -m drive_sync pull && python -m ingest

# in ~/learning, with scottie's Python environment
python .pi/tools/import_scottie.py --scottie ../scottie
```

Per course, this writes:

- `syllabus.md`: exam dates from `courses.yaml` and the weekly schedule from `schedule.yaml`, inside a generated block. Anything you add outside that block (exam formats, grading notes) is kept on the next import.
- `drive/*.md`: every PDF, slide deck and notes file in that course's Drive folder, already converted to text, so you can skip markitdown.

Re-run both commands whenever you add files to Drive or change exam dates. Your progress (`review.md`, `flashcards.csv`) is never touched.

### 3. Study

Open `pi` in `~/learning` and say what you want, e.g.:

- "Teach me week 4 of BUS201 — institutional theory. Midterm is in two weeks."
- "Review BUS201" — quizzes whatever is due in `review.md`.
- "Give me a practice case question for SOC101 like the ones on the past exams."

What the tutor does:

- **Teaches from your course materials** (via the `course-researcher` subagent): the course's definitions, frameworks, examples, and citations back to the file. The web `researcher` is only a fallback.
- **Explains the "why"** behind each theory/framework so it sticks, then **drills the exact wording** the exam wants.
- **Quizzes in your exam's format**: multiple choice via popups; define / compare / apply-to-a-case questions in chat, graded against the course wording.
- **Spaced review**: every item learned goes into `review.md` (a 5-box Leitner schedule) and comes back when it's due.
- **Flashcard export** to `flashcards.csv` so you can review on your phone without using AI.

### What's optional

- **Subagents** need [pi-interactive-subagents](https://github.com/amosblomqvist/pi-interactive-subagents) (requires tmux). Without it, the main session reads your course files itself, which works fine, just with more context used per session.
- **The web `researcher`** uses `web_search` / `web_fetch` / `safe_bash` tools that come from other pi extensions, not this repo. It's only a fallback for things your course doesn't cover.
- **Diagrams** (`visualize`, `mermaid-maker`, `svg-maker`) are rarely used for these courses, and the renderer looks for Chrome at macOS paths. Tables and lists in chat cover most needs.
- **`/md-log`** still works if you want a markdown copy of a session, viewable in any markdown previewer (VS Code, Obsidian, etc.). Not needed.

---

*The rest of this README is the original author's.*

## What's in it

- `skills/teach/` — the philosophy and the process (rewritten in this fork for coursework, recall and spaced review)
- `skills/review/` — *(this fork)* a review-only session over what's due
- `agents/course-researcher.md` — *(this fork)* finds what your course materials say about a topic
- `templates/course/` — *(this fork)* starter folder for a course
- `tools/import_scottie.py` — *(this fork)* builds course folders from the Daybook's data (scottie)
- `skills/visualize/` — adds a correct, minimal diagram to a lesson when an idea is clearer as a picture
- `extensions/ask-user-question/` — the agent asks you questions through a UI popup
- `extensions/quiz/` — graded questions with instant feedback (✓/✗, correct answer, explanation)
- `extensions/md-log/` — link a markdown file to the session
- `extensions/visual-tools/` — tools for visualization subagents
- `agents/` — `researcher`, `svg-maker`, `mermaid-maker`: the subagents the system delegates to

## Install

This repo **is** a `.pi` directory. From your learning project's root:

```bash
git clone https://github.com/amosblomqvist/learn .pi
```

Then open pi in that directory. (Or copy the pieces you want into your existing project config.)

## Requirements

- [pi](https://github.com/earendil-works/pi)
- A subagent implementation, so the system can spawn the researcher and the visual makers. Recommended: [pi-interactive-subagents](https://github.com/amosblomqvist/pi-interactive-subagents) (tmux only). With it, everything works out of the box. Any other implementation works too, but expect to adapt the agent definitions, e.g. `agents/researcher.md` lists `safe_bash` in its tools, which is specific to that extension.
- `ask-user-question` — use the copy bundled here. If your setup already has an `ask-user-question` extension, use **this** one in its place. Popups from different extensions serialize through a shared UI lock, which only works when it's the same implementation.

## Notes

You can run the system without subagents. The main session does the teaching. You just lose the researcher (truth verification) and the generated visuals.

The teaching skill is written for one learner (me). Edit the skill to fit how you learn best.
