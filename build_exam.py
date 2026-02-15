#!/usr/bin/env python3
"""
Generate printable exam paper and answer key from quiz_data.json.
Run: python3 build_exam.py
Output: exam-paper.html (exam only), answer-key.html (answers only).
"""

import json
from pathlib import Path

QUIZ_PATH = Path(__file__).resolve().parent / "quiz_data.json"
PAPER_PATH = Path(__file__).resolve().parent / "exam-paper.html"
KEY_PATH = Path(__file__).resolve().parent / "answer-key.html"

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def escape(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def format_answer(q):
    """Return correct answer as short text for answer key."""
    t = q.get("type", "")
    if t == "single":
        idx = q.get("correct_index", 0)
        return LETTERS[idx] if idx < 26 else str(idx + 1)
    if t == "multiple":
        idxs = sorted(q.get("correct_indices", []))
        return ",".join(LETTERS[i] if i < 26 else str(i + 1) for i in idxs)
    if t == "true_false":
        ans = q.get("correct_answers", [])
        return " ".join("T" if a else "F" for a in ans)
    if t == "ranking":
        order = q.get("correct_order", [])
        return ", ".join(str(x) for x in order)
    if t == "match":
        matches = q.get("correct_matches", [])
        return ", ".join(str(m) for m in matches)
    return "—"


def build_paper(data):
    lines = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>Electrical Installation — Practice Exam</title>",
        "<style>",
        "body { font-family: Georgia, 'Times New Roman', serif; font-size: 11pt; line-height: 1.4; max-width: 800px; margin: 1in auto; padding: 0 1em; color: #111; background: #fff; }",
        "h1 { font-size: 1.4em; margin-bottom: 0.2em; }",
        ".header { margin-bottom: 1.5em; padding-bottom: 0.75em; border-bottom: 2px solid #333; }",
        ".header p { margin: 0.25em 0; }",
        ".meta { display: flex; gap: 2em; flex-wrap: wrap; margin-top: 0.5em; }",
        ".meta span { display: inline-block; min-width: 120px; border-bottom: 1px solid #333; }",
        ".instructions { font-size: 0.95em; color: #333; margin-bottom: 1.5em; }",
        ".q { margin-bottom: 1.25em; page-break-inside: avoid; }",
        ".q-num { font-weight: bold; margin-bottom: 0.25em; }",
        ".q-text { margin-bottom: 0.5em; }",
        ".opts { list-style: none; padding-left: 0; margin: 0.25em 0; }",
        ".opts li { margin-bottom: 0.2em; }",
        ".opts li::before { content: attr(data-letter) '. '; font-weight: bold; }",
        ".tf-statement { margin: 0.35em 0 0.15em 0; padding-left: 0.5em; }",
        ".tf-line { margin-bottom: 0.4em; }",
        ".tf-answer { display: inline-block; width: 2em; border-bottom: 1px solid #333; margin-left: 0.5em; }",
        ".rank-item { margin: 0.2em 0; }",
        ".match-item { margin: 0.25em 0; }",
        ".match-answer { display: inline-block; width: 2em; border-bottom: 1px solid #333; margin-left: 0.5em; }",
        ".answer-line { margin-top: 0.35em; }",
        ".answer-line .blank { display: inline-block; min-width: 80px; border-bottom: 1px solid #333; margin-left: 0.25em; }",
        "@media print { body { margin: 0.5in; } .q { page-break-inside: avoid; } }",
        "</style>",
        "</head>",
        "<body>",
        "<div class='header'>",
        f"<h1>{escape(data.get('title', 'Electrical Installation Quiz'))}</h1>",
        f"<p>{escape(data.get('source', ''))}</p>",
        "<div class='meta'>",
        "<span>Name: </span>",
        "<span>Date: </span>",
        f"<span>Total questions: {len(data['questions'])}</span>",
        "</div>",
        "</div>",
        "<p class='instructions'><strong>Instructions:</strong> Answer each question in the space provided. "
        "Single choice: write the letter (A, B, C, or D). Multiple choice: write all correct letters. "
        "True/False: write T or F for each part. Ranking: write the step order (e.g. 2, 1, 3, 4). "
        "Match: write the matching letter for each item.</p>",
    ]

    for i, q in enumerate(data["questions"], 1):
        t = q.get("type", "single")
        lines.append(f"<div class='q'>")
        lines.append(f"<div class='q-num'>Question {i}</div>")
        lines.append(f"<div class='q-text'>{escape(q.get('text', ''))}</div>")

        if t == "single":
            lines.append("<ul class='opts'>")
            for j, opt in enumerate(q.get("options", [])):
                lines.append(f"<li data-letter='{LETTERS[j]}'>{escape(opt)}</li>")
            lines.append("</ul>")
            lines.append("<div class='answer-line'>Answer: <span class='blank'></span></div>")

        elif t == "multiple":
            lines.append("<p><em>Select all that apply.</em></p>")
            lines.append("<ul class='opts'>")
            for j, opt in enumerate(q.get("options", [])):
                lines.append(f"<li data-letter='{LETTERS[j]}'>{escape(opt)}</li>")
            lines.append("</ul>")
            lines.append("<div class='answer-line'>Answer: <span class='blank'></span></div>")

        elif t == "true_false":
            for stmt in q.get("statements", []):
                lines.append(f"<div class='tf-line'><span class='tf-statement'>{escape(stmt)}</span> Answer: <span class='tf-answer'></span></div>")
            if not q.get("statements"):
                lines.append("<div class='answer-line'>Answer: <span class='blank'></span></div>")

        elif t == "ranking":
            for j, item in enumerate(q.get("items", []), 1):
                lines.append(f"<div class='rank-item'>{j}. {escape(item)}</div>")
            lines.append("<div class='answer-line'>Order (step numbers): <span class='blank'></span></div>")

        elif t == "match":
            left = q.get("left_items", [])
            right = q.get("right_options", [])
            opts_str = "  ".join(f"{ro.get('letter', '')}. {escape(ro.get('text', ''))}" for ro in right)
            lines.append(f"<p><strong>Options:</strong> {opts_str}</p>")
            for item in left:
                lines.append(f"<div class='match-item'>{escape(item)} &rarr; <span class='match-answer'></span></div>")
            lines.append("<div class='answer-line'>Answer: <span class='blank'></span></div>")

        else:
            lines.append("<div class='answer-line'>Answer: <span class='blank'></span></div>")

        lines.append("</div>")

    lines.extend(["</body>", "</html>"])
    return "\n".join(lines)


def build_key(data):
    lines = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<title>Answer Key</title>",
        "<style>",
        "body { font-family: Georgia, serif; font-size: 11pt; max-width: 600px; margin: 1in auto; padding: 0 1em; color: #111; background: #fff; }",
        "h1 { font-size: 1.3em; margin-bottom: 0.5em; }",
        "table { border-collapse: collapse; width: 100%; }",
        "th, td { border: 1px solid #333; padding: 0.25em 0.5em; text-align: left; }",
        "th { background: #f0f0f0; }",
        "td:first-child { font-weight: bold; width: 4em; }",
        "@media print { body { margin: 0.5in; } }",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>{escape(data.get('title', 'Quiz'))} — Answer Key</h1>",
        "<p><strong>Do not print this sheet with the exam if you want to test yourself.</strong></p>",
        "<table>",
        "<tr><th>Q</th><th>Answer</th></tr>",
    ]
    for i, q in enumerate(data["questions"], 1):
        ans = format_answer(q)
        lines.append(f"<tr><td>{i}</td><td>{escape(str(ans))}</td></tr>")
    lines.extend(["</table>", "</body>", "</html>"])
    return "\n".join(lines)


def main():
    with open(QUIZ_PATH, encoding="utf-8") as f:
        data = json.load(f)
    with open(PAPER_PATH, "w", encoding="utf-8") as f:
        f.write(build_paper(data))
    with open(KEY_PATH, "w", encoding="utf-8") as f:
        f.write(build_key(data))
    print(f"Generated {PAPER_PATH.name} and {KEY_PATH.name}")
    print("  Print exam-paper.html for the exam. Print answer-key.html separately to mark.")


if __name__ == "__main__":
    main()
