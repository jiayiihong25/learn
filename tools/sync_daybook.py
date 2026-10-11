"""Two-way sync between the study tutor and the Daybook, through Drive.

    python .pi/tools/sync_daybook.py [--scottie ../scottie] [--no-pull] [--no-push]

Run it from the learning project root (the folder that contains .pi/), with
scottie's Python environment, after a study session or whenever you've added
course files to Drive. It:

1. pulls the "JiaYi Courses" Drive folder into the scottie checkout and
   extracts the text (`python -m drive_sync pull && python -m ingest`: no
   model calls, doesn't move the Daybook's reading pace);
2. refreshes courses/<course>/ for every course with files in Drive
   (import_scottie.py);
3. adds the Daybook's open "to relearn" flags (relearn.json, exported by the
   morning Routine) to that course's review.md as Box 1 items due today, once
   each;
4. writes every course's review items to tutor_status.json and pushes it to
   Drive (`python -m drive_sync push --tutor-only`), so tomorrow morning's
   Daybook shows what's due in its Review panel.

Contract for both files: scottie-display/docs/tutor-sync.md.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from import_scottie import import_courses  # noqa: E402

SCHEMA_VERSION = 1
BOXES = 5
FLAG_SOURCE = "Daybook flag "
ITEM_COLUMNS = ("item", "answer", "source", "box", "next due")
DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


class ReviewFileError(ValueError):
    pass


def run(cmd: list[str], cwd: Path) -> None:
    print(f"$ {' '.join(cmd)}  (in {cwd})")
    if subprocess.run(cmd, cwd=cwd).returncode != 0:
        sys.exit(f"Failed: {' '.join(cmd)}. Nothing was pushed.")


# --- review.md --------------------------------------------------------------

def _cells(line: str) -> list[str]:
    """Split a markdown table row on unescaped pipes."""
    inner = line.strip()
    inner = inner[1:] if inner.startswith("|") else inner
    inner = inner[:-1] if inner.endswith("|") and not inner.endswith("\\|") else inner
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", inner)]


def _section(text: str, heading: str) -> list[str]:
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower() == heading
            continue
        if inside:
            lines.append(line)
    return lines


def read_items(review_md: Path) -> list[dict]:
    """The Items table of review.md. Raises ReviewFileError on a row the tutor wrote badly."""
    rows = [l for l in _section(review_md.read_text(encoding="utf-8"), "items") if l.strip().startswith("|")]
    if not rows:
        return []
    header = [h.lower() for h in _cells(rows[0])]
    # "Answer (course wording)" counts as "answer".
    col = {name: next((i for i, h in enumerate(header) if h == name or h.startswith(name + " ")), None) for name in ITEM_COLUMNS}
    missing = [name for name, i in col.items() if i is None]
    if missing:
        raise ReviewFileError(f"{review_md}: Items table is missing column(s) {', '.join(missing)}")
    items = []
    for n, row in enumerate(rows[1:], start=2):
        cells = _cells(row)
        if all(set(c) <= set("-: ") for c in cells):
            continue  # the |---|---| separator
        if len(cells) < len(header):
            raise ReviewFileError(f"{review_md}: Items row {n} has {len(cells)} cells, expected {len(header)}")
        item, source = cells[col["item"]], cells[col["source"]]
        try:
            box = int(cells[col["box"]])
            next_due = date.fromisoformat(cells[col["next due"]])
        except ValueError:
            raise ReviewFileError(f"{review_md}: Items row {n} ({item!r}) needs a Box 1-5 and a YYYY-MM-DD Next due") from None
        if not item or not 1 <= box <= BOXES:
            raise ReviewFileError(f"{review_md}: Items row {n} needs an Item and a Box from 1 to {BOXES}")
        flag = source[source.index(FLAG_SOURCE) + len(FLAG_SOURCE):].split()[0] if FLAG_SOURCE in source else None
        items.append({"item": item, "box": box, "next_due": next_due.isoformat(), "flag_id": flag})
    return items


def last_session(review_md: Path) -> str | None:
    dates = DATE.findall("\n".join(_section(review_md.read_text(encoding="utf-8"), "progress")))
    return max(dates) if dates else None


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def add_flags(review_md: Path, flags: list[dict], today: date) -> int:
    """Appends each flag not already in review.md as a Box 1 row due today. Returns how many."""
    known = {i["flag_id"] for i in read_items(review_md) if i["flag_id"]}
    new = [f for f in flags if f["id"] not in known]
    if not new:
        return 0
    rows = []
    for f in new:
        note = f"what didn't stick: {_cell(f['note'])}; " if f.get("note") else ""
        flagged = f" {f['flagged_on']}" if f.get("flagged_on") else ""
        rows.append(
            f"| ⚑ {_cell(f['where'])} | (to fill in from the course material; {note}flagged on the Daybook{flagged}) "
            f"| {FLAG_SOURCE}{f['id']} | 1 | {today.isoformat()} |"
        )
    lines = review_md.read_text(encoding="utf-8").splitlines()
    # Insert after the Items table's last row (or its separator, if empty).
    start = next(i for i, l in enumerate(lines) if l.strip().lower() == "## items")
    end = start + 1
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            break
        if lines[i].strip().startswith("|"):
            end = i + 1
    lines[end:end] = rows
    review_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(new)


# --- the sync -----------------------------------------------------------------

def load_flags(path: Path) -> list[dict]:
    if not path.exists():
        return []
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc == {}:
        return []  # the Drive placeholder: the Routine hasn't exported yet
    if doc.get("schema_version") != SCHEMA_VERSION or not isinstance(doc.get("flags"), list):
        sys.exit(f"{path}: unexpected relearn.json (schema_version {doc.get('schema_version')!r}); see scottie-display/docs/tutor-sync.md")
    return [f for f in doc["flags"] if isinstance(f, dict) and f.get("id") and f.get("course") and f.get("where")]


def status(folders: dict[str, Path]) -> dict:
    courses = []
    for course, folder in sorted(folders.items()):
        review_md = folder / "review.md"
        courses.append({
            "course": course,
            "last_session": last_session(review_md),
            "items": read_items(review_md),
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "synced_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "courses": courses,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scottie", type=Path, default=Path("../scottie"), help="path to the scottie checkout")
    parser.add_argument("--out", type=Path, default=Path("courses"), help="the tutor's courses folder")
    parser.add_argument("--no-pull", action="store_true", help="use the scottie checkout's data/ as it is")
    parser.add_argument("--no-push", action="store_true", help="write tutor_status.json but don't push it to Drive")
    args = parser.parse_args()
    scottie = args.scottie.resolve()

    if not args.no_pull:
        run([sys.executable, "-m", "drive_sync", "pull"], scottie)
        run([sys.executable, "-m", "ingest"], scottie)

    folders = import_courses(scottie, args.out)

    today = date.today()
    flags = load_flags(scottie / "data" / "relearn.json")
    waiting = sorted({f["course"] for f in flags if f["course"] not in folders})
    try:
        for course, folder in folders.items():
            n = add_flags(folder / "review.md", [f for f in flags if f["course"] == course], today)
            if n:
                print(f"⚑ {course}: {n} relearn flag{'s' if n != 1 else ''} from the Daybook added to review.md")
        if waiting:
            print(f"⚑ flags waiting for course files in Drive: {', '.join(waiting)}")
        doc = status(folders)
    except ReviewFileError as exc:
        sys.exit(f"{exc}\nFix that row (or ask the tutor to), then sync again. Nothing was pushed.")
    out = scottie / "data" / "tutor_status.json"
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    due = sum(1 for c in doc["courses"] for i in c["items"] if i["next_due"] <= today.isoformat())
    print(f"Wrote {out}: {sum(len(c['items']) for c in doc['courses'])} items, {due} due today")

    if not args.no_push:
        run([sys.executable, "-m", "drive_sync", "push", "--tutor-only"], scottie)
        print("Pushed. The Daybook's Review panel picks it up at the next morning build.")


if __name__ == "__main__":
    main()
