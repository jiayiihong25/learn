---
name: review
description: Run a spaced-review session for one of the learner's courses — quiz every item that's due in courses/<course>/review.md, update the schedule, and re-teach anything missed. Use when the learner says "review", "quiz me", "what's due", or wants to practise before an exam without learning new material.
---

# Review session

A focused session of retrieval practice — no new material. Follow the `teach` skill's rules for accuracy, question formats, quiz-option construction, and the box schedule; this skill only sets the session shape.

1. **Pick the course.** If the learner didn't say which, list the folders in `courses/` and ask with `ask_user_question`.
2. **Load the queue.** Read `courses/<course>/review.md` and run `date +%F`. Due = every item whose **Next due** is today or earlier. Order: most overdue first, then lowest box first.
   - Nothing due? Say so, and offer: review the lowest-box items early, do exam-style practice (below), or start a new topic with `teach`.
3. **Quiz each due item** in the format the exam would use (see `teach` → "Question formats"). Mix it up — don't ask every item the same way, and ask for the term from the definition as well as the definition from the term. Default cap: ~20 items; ask the learner if they want to keep going.
   - A ⚑ row (Answer *"to fill in from the course material…"*) is a spot the learner flagged on their Daybook: teach it first, then rewrite it into real items, keeping `Daybook flag <id>` in their Source (see `teach` → "Spaced review").
4. **After each answer:** update the row's Box and Next due per the schedule. If they missed it, re-teach briefly — the *why* behind it, a contrast with whatever they confused it with — then move on. Re-ask every missed item once more at the end of the session.
5. **Exam-style practice (optional, when an exam is near).** Write 1–3 application questions in the style of `past-exams/` that combine several recently reviewed concepts, and grade them like a TA.
6. **Wrap up:** save `review.md`, add a line to its Progress section (date, how many reviewed, % correct, recurring weak spots), and give a 2–3 line summary of what to focus on next. Remind the learner to run `python .pi/tools/sync_daybook.py` so the Daybook's Review panel is up to date tomorrow.
