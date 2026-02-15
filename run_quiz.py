#!/usr/bin/env python3
"""
Electrical Installation & Standards Quiz (181 questions).
Run in terminal: python run_quiz.py
To use with Gemini: python run_quiz.py --gemini-prompt — copy output into Gemini and ask it to quiz you.
"""

import json
import sys
from pathlib import Path

QUIZ_PATH = Path(__file__).resolve().parent / "quiz_data.json"


def load_quiz():
    with open(QUIZ_PATH, encoding="utf-8") as f:
        return json.load(f)


def run_single(question, q_num):
    print(f"\n--- Question {q_num} ---")
    print(question["text"])
    for i, opt in enumerate(question["options"], 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            raw = input("Your answer (number): ").strip()
            if not raw:
                continue
            choice = int(raw)
            if 1 <= choice <= len(question["options"]):
                break
        except ValueError:
            pass
        print("Enter a valid option number.")
    correct = question["correct_index"] + 1
    ok = choice == correct
    print("Correct!" if ok else f"Incorrect. Correct answer: {correct}. {question['options'][question['correct_index']]}")
    return ok


def run_multiple(question, q_num):
    print(f"\n--- Question {q_num} ---")
    print(question["text"])
    for i, opt in enumerate(question["options"], 1):
        print(f"  {i}. {opt}")
    print("Enter numbers separated by spaces (e.g. 2 4)")
    while True:
        try:
            raw = input("Your answers: ").strip()
            if not raw:
                continue
            chosen = sorted(set(int(x) for x in raw.split()))
            if all(1 <= c <= len(question["options"]) for c in chosen):
                break
        except ValueError:
            pass
        print("Enter valid option numbers separated by spaces.")
    # 1-based indices chosen; correct are 1-based
    correct_set = sorted(i + 1 for i in question["correct_indices"])
    ok = chosen == correct_set
    print("Correct!" if ok else f"Incorrect. Correct: {correct_set} — " + ", ".join(question["options"][i] for i in question["correct_indices"]))
    return ok


def run_true_false(question, q_num):
    print(f"\n--- Question {q_num} ---")
    print(question.get("text", ""))
    statements = question["statements"]
    correct = question["correct_answers"]
    score = 0
    for i, (stmt, ans) in enumerate(zip(statements, correct), 1):
        print(f"  {i}. {stmt}")
        expected = "True" if ans else "False"
        while True:
            raw = input(f"    True or False? ").strip().lower()
            if raw in ("true", "t", "1"):
                user = True
                break
            if raw in ("false", "f", "0"):
                user = False
                break
            print("    Enter True or False.")
        if user == ans:
            score += 1
            print("    Correct!")
        else:
            print(f"    Incorrect. Answer: {expected}")
    return score == len(statements)


def run_ranking(question, q_num):
    print(f"\n--- Question {q_num} ---")
    print(question["text"])
    items = question["items"]
    correct_order = question["correct_order"]  # step numbers 1..n for each item in order
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    n = len(items)
    print(f"Enter the step order as {n} numbers (1-{n}) for items 1-{n} respectively, e.g. 2 1 3 4" + (" 6 5" if n == 6 else ""))
    while True:
        try:
            raw = input("Your order: ").strip().split()
            if len(raw) != len(items):
                print(f"Enter exactly {len(items)} numbers.")
                continue
            user = [int(x) for x in raw]
            if set(user) != set(range(1, len(items) + 1)):
                print(f"Use each step number 1 to {len(items)} exactly once.")
                continue
            break
        except (ValueError, IndexError):
            print("Enter numbers separated by spaces.")
    ok = user == correct_order
    if ok:
        print("Correct!")
    else:
        print("Incorrect. Correct order (step for each item):", correct_order)
    return ok


def run_match(question, q_num):
    print(f"\n--- Question {q_num} ---")
    print(question["text"])
    left = question["left_items"]
    right = question["right_options"]
    correct = question["correct_matches"]
    print("Right options:")
    for ro in right:
        print(f"  {ro['letter']}. {ro['text']}")
    print("Enter the letter for each left item (in order), e.g. D A E H C B F G")
    for i, item in enumerate(left, 1):
        print(f"  {i}. {item}")
    while True:
        try:
            raw = input("Your matches (letters separated by spaces): ").strip().upper().split()
            if len(raw) != len(left):
                print(f"Enter exactly {len(left)} letters.")
                continue
            if all(r in [ro["letter"] for ro in right] for r in raw):
                break
            print("Use only letters A–H (or the option letters shown).")
        except (ValueError, IndexError):
            pass
    ok = raw == correct
    if ok:
        print("Correct!")
    else:
        print("Incorrect. Correct:", " ".join(correct))
    return ok


def run_quiz(shuffle=False):
    data = load_quiz()
    questions = data["questions"]
    if shuffle:
        import random
        random.shuffle(questions)
    total = len(questions)
    correct = 0
    print(f"\n{data['title']} — Batch {data.get('batch', 1)}")
    print(f"Questions: {total}. Source: {data.get('source', 'N/A')}\n")

    for i, q in enumerate(questions, 1):
        t = q["type"]
        if t == "single":
            correct += run_single(q, i)
        elif t == "multiple":
            correct += run_multiple(q, i)
        elif t == "true_false":
            correct += run_true_false(q, i)
        elif t == "ranking":
            correct += run_ranking(q, i)
        elif t == "match":
            correct += run_match(q, i)
        else:
            print(f"Unknown type: {t}")

    print(f"\n--- Result: {correct}/{total} ({100 * correct / total:.1f}%) ---")


def build_gemini_prompt():
    """Build a single text prompt you can paste into Gemini so it can quiz you."""
    data = load_quiz()
    lines = [
        "You are a quiz master. Quiz me one question at a time from the following list.",
        "After I answer, tell me if I was right or wrong and show the correct answer, then ask the next question.",
        "Do not reveal the correct answers until I have answered. At the end, give my score.",
        "",
        "--- QUIZ DATA (JSON) ---",
        json.dumps({"title": data["title"], "batch": data.get("batch"), "questions": data["questions"]}, indent=2),
    ]
    return "\n".join(lines)


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--gemini-prompt", "-g"):
        print(build_gemini_prompt())
        return
    shuffle = "--shuffle" in sys.argv or "-s" in sys.argv
    run_quiz(shuffle=shuffle)


if __name__ == "__main__":
    main()
