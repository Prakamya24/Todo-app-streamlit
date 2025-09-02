import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import tempfile

# Use a writable temp directory for Streamlit Cloud
DATA_FILE = Path(tempfile.gettempdir()) / "todos.json"

# Load todos from file
def load_todos():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except:
            return []
    return []

# Save todos to file
def save_todos(todos):
    DATA_FILE.write_text(json.dumps(todos, indent=2))

st.set_page_config(page_title="Simple To‑Do List", page_icon="✅", layout="centered")
st.title("✅ Simple To‑Do List (Streamlit + Python)")

# Initialize session state
if "todos" not in st.session_state:
    st.session_state.todos = load_todos()

todos = st.session_state.todos

# Add new todo
with st.form("Add task"):
    new_task = st.text_input("New task", "")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    submit = st.form_submit_button("Add")
    if submit and new_task.strip():
        todos.append({
            "id": int(datetime.now().timestamp()*1000),
            "task": new_task.strip(),
            "priority": priority,
            "done": False,
            "created_at": datetime.now().isoformat()
        })
        save_todos(todos)
        st.success("Task added!")
        st.experimental_rerun()

st.markdown("---")
if not todos:
    st.info("No tasks yet — add one above!")
else:
    # Sort by done then priority then created_at
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    todos.sort(key=lambda t: (t["done"], priority_order.get(t.get("priority","Low")), t.get("created_at","")))

    for t in todos:
        cols = st.columns([0.05, 0.65, 0.15, 0.15])
        done = cols[0].checkbox("", value=t["done"], key=f"done_{t['id']}")
        if done != t["done"]:
            t["done"] = done
            save_todos(todos)
            st.experimental_rerun()
        task_label = t["task"] + (f"  — *{t['priority']}*" if t.get("priority") else "")
        if t["done"]:
            cols[1].markdown(f"~~{task_label}~~")
        else:
            cols[1].markdown(task_label)
        if cols[2].button("Edit", key=f"edit_{t['id']}"):
            with st.form(f"edit_form_{t['id']}", clear_on_submit=False):
                new_text = st.text_input("Task text", value=t["task"])
                new_pr = st.selectbox("Priority", ["Low","Medium","High"], index=["Low","Medium","High"].index(t.get("priority","Low")))
                saved = st.form_submit_button("Save")
                if saved:
                    t["task"] = new_text.strip()
                    t["priority"] = new_pr
                    save_todos(todos)
                    st.experimental_rerun()
        if cols[3].button("Delete", key=f"del_{t['id']}"):
            todos[:] = [x for x in todos if x["id"] != t["id"]]
            save_todos(todos)
            st.experimental_rerun()

st.markdown("---")
if st.button("Clear completed tasks"):
    todos[:] = [x for x in todos if not x["done"]]
    save_todos(todos)
    st.experimental_rerun()
