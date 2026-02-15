# UEEEL0012 — Practice exam for TAFE NSW Electrotechnology Cert III

**Install low voltage wiring, appliances, switchgear and associated accessories.**

If you remember all these questions and answers you will be perfectly fine in the exam and it will help with capstone. *(Capstone quiz coming soon.)*

---

## Visit the quiz online

**→ [Open the quiz](https://jaydenmedifocal.github.io/UEEEL0012-Install-low-voltage-wiring-appliances-switchgear-and-associated-accessories/)**

181 questions · single choice, multiple choice, true/false, ranking, matching · 1 mark per question · instant feedback, previous/next, print summary.

*If the link doesn’t load:* In this repo go to **Settings → Pages → Source: Deploy from a branch** → Branch: `main`, Folder: `/ (root)` → Save. The site will appear at the URL above after a minute or two.

---

## What it covers

- **AS/NZS 3000:2018**, Building Code of Australia, NCC
- **Units:** 50 questions per section (1–50, 51–100, 101–150, 151–181) or **All** for the full set
- For **TAFE NSW Electrotechnology Certificate III**, unit **UEEEL0012**

---

## Run locally

```bash
git clone https://github.com/jaydenmedifocal/UEEEL0012-Install-low-voltage-wiring-appliances-switchgear-and-associated-accessories.git
cd UEEEL0012-Install-low-voltage-wiring-appliances-switchgear-and-associated-accessories
python3 -m http.server 8000
```

Open **http://localhost:8000**. Use **Shuffle questions** for a random order.

---

## Printable exam and answer key

```bash
python3 build_exam.py
```

Then open **exam-paper.html** and **answer-key.html** in your browser and use **File → Print**.

---

## Terminal and AI (Gemini) use

- **Terminal:** `python3 run_quiz.py` or `python3 run_quiz.py --shuffle`
- **Gemini:** `python3 run_quiz.py --gemini-prompt` → copy output → paste into Gemini and ask it to quiz you.

---

## Disclaimer

For **study only**. Based on AS/NZS 3000:2018 and related standards. Not a substitute for the actual standards or formal training. Always confirm against current published standards.

---

## Licence

MIT — use, change and share for study. See [LICENSE](LICENSE).
