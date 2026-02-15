# Electrical Installation & Standards Quiz

A free, open study quiz for **AS/NZS 3000:2018**, the **Building Code of Australia**, and **NCC** (National Construction Code). **181 questions** covering electrical installation and related standards—single choice, multiple choice, true/false, ranking, and matching.

Use it in the browser (including on GitHub Pages), in the terminal, or print an exam paper and answer key.

---

## Try it online

If this repo is enabled for **GitHub Pages**, the quiz runs in your browser at:

**https://\<your-username\>.github.io/\<repo-name\>/**

To enable: **Settings → Pages → Source: Deploy from a branch** → choose `main` (or `master`) and `/ (root)`.

---

## Run locally in the browser

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
python3 -m http.server 8000
```

Open **http://localhost:8000**. Optionally tick **Shuffle questions** for a random order.

---

## What’s in the quiz

- **Sections:** 50 questions per section (1–50, 51–100, 101–150, 151–181), or **All** for the full set.
- **Question types:** Single choice, multiple choice, true/false (multi-part), ranking, and matching.
- **Scoring:** 1 mark per question. At the end you see your score, a **question breakdown** (each question and 1/0), and a **Print summary** option.

You can move **Previous** / **Next** and your answers and feedback are kept when you go back.

---

## Printable exam and answer key

Generate a print-friendly exam (questions only) and answer key:

```bash
python3 build_exam.py
```

Then open **exam-paper.html** and **answer-key.html** in your browser and use **File → Print**. Print the exam first; use the answer key when marking.

---

## Run in the terminal

```bash
python3 run_quiz.py
```

Optional: `python3 run_quiz.py --shuffle` to randomise order.

---

## Use with Gemini (or other AI)

1. Generate a prompt containing the full quiz:
   ```bash
   python3 run_quiz.py --gemini-prompt
   ```
2. Copy the output and paste it into Gemini (or another AI).
3. Ask the AI to quiz you one question at a time and tell you if each answer is correct.

---

## Adding or editing questions

Edit **quiz_data.json** and add or change objects in the `"questions"` array:

- **Single choice:** `"type": "single"`, `"options": [...]`, `"correct_index": 0` (0-based).
- **Multiple choice:** `"type": "multiple"`, `"options": [...]`, `"correct_indices": [1, 3]`.
- **True/False:** `"type": "true_false"`, `"statements": [...]`, `"correct_answers": [true, false, ...]`.
- **Ranking:** `"type": "ranking"`, `"items": [...]`, `"correct_order": [2, 1, 3, 4, 6, 5]`.
- **Match:** `"type": "match"`, `"left_items": [...]`, `"right_options": [{"letter": "A", "text": "..."}, ...]`, `"correct_matches": ["D", "A", ...]`.

After changing **quiz_data.json**, run `python3 build_exam.py` if you use the printable exam.

---

## Standards and disclaimer

Questions are based on **AS/NZS 3000:2018** (Wiring Rules), **Building Code of Australia**, **NCC**, and related standards. This project is for **study only**; it is not a substitute for the actual standards or formal training. Always confirm answers against the current published standards.

---

## Licence

MIT — see [LICENSE](LICENSE). You can use, modify, and share this for study and learning.
