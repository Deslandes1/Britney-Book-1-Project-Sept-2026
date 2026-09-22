
## 4. How to Deploy — Step by Step

**Step 1 — Create the GitHub repository**
- Go to https://github.com/new
- Name it `britneys-kids-in-wonderland`
- Make it Public
- Click **Create repository**

**Step 2 — Upload the three files**
- Click **Add file** → **Upload files**
- Drag in `app.py`, `requirements.txt`, and `README.md`
- Click **Commit changes**

**Step 3 — Deploy on Streamlit Cloud**
- Go to https://share.streamlit.io
- Sign in with your GitHub account
- Click **New app**
- Repository: `your-username/britneys-kids-in-wonderland`
- Branch: `main`
- Main file path: `app.py`
- Click **Deploy**

**Step 4 — Wait 2–3 minutes**
Streamlit will install `streamlit` and `gtts` and launch your app. You'll get a public URL like:

`https://gesnerdeslandes-britneys-kids-in-wonderland-app.streamlit.app`

## Notes on the AI Voice

- The app uses **Google Text-to-Speech (gTTS)** with `lang="en"` and `tld="com"`, which produces a **female-sounding American English voice** — close to a child-friendly narrator.
- gTTS is free, requires no API key, and works on Streamlit Cloud.
- If you want a **true child voice**, the best option is to switch to **OpenAI TTS** with the `nova` or `shimmer` voice (available via `streamlit-TTS`), but that requires an OpenAI API key and a small usage cost.
- Every time you click **▶ Read This Page Aloud**, the app generates a fresh MP3 and autoplays it.

## What You Can Extend

- Add more pages by appending to the `PAGES` list — the app automatically detects the list length.
- Change `tld="com"` to `tld="co.uk"` for a British voice, or `tld="ca"` for a Canadian voice.
- Add illustrations by placing an `st.image()` call inside the book card.
- Add a "read all pages automatically" loop using `st.session_state` and `time.sleep()`.

Once deployed, the app will show your big golden header **BE LIKE BRIT / BRITNEY'S KIDS IN WONDERLAND BOOK 1**, your name and contact info, and a working AI voice that reads every page aloud.
