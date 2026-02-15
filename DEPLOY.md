# Deploy to GitHub (one-time setup)

Your quiz is ready to push. Do this once:

## 1. Create the repo on GitHub

1. Go to **https://github.com/new**
2. Sign in if needed.
3. **Repository name:** e.g. `electrical-quiz` or `Study`
4. **Public**, no need to add a README (you already have one).
5. Click **Create repository**.

## 2. Push from your Mac

In Terminal, from this folder (`Study`), run (replace `YOUR_USERNAME` and `REPO_NAME` with yours):

```bash
cd /Users/jaydenbarnett/Study
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

If GitHub asks for a password, use a **Personal Access Token** (Settings → Developer settings → Personal access tokens). Or use GitHub Desktop / SSH if you prefer.

## 3. Turn on GitHub Pages

1. On the repo page: **Settings** → **Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `main` → `/ (root)` → **Save**
4. After a minute, the quiz is live at:

   **https://YOUR_USERNAME.github.io/REPO_NAME/**

Done. Share that link so others can use the quiz.
