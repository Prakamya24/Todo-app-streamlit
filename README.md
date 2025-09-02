
# Simple To-Do List (Streamlit + Python)

This is a small Streamlit app that implements a persistent to-do list stored in a local JSON file (`todos.json`).

## Run locally

1. Create a virtual environment (recommended) and activate it.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. The app will open in your browser at `http://localhost:8501`.

## Deploy

- Deploy to Streamlit Cloud: push this repo to GitHub and connect the repo on [Streamlit Cloud](https://streamlit.io/cloud).
- Or use Render, Railway, or other Python app hosts by following their deployment guides.

## Files
- `app.py` — Streamlit application.
- `todos.json` — created at runtime to store tasks.
- `requirements.txt` — Python dependencies.

