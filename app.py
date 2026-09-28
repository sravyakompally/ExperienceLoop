from flask import Flask, render_template, request, jsonify
from database.database import init_db, create_experience, get_stats, get_recent
from hindsight.client import HindsightMemory
from uuid import uuid4
from datetime import datetime, timezone

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
init_db()
memory = HindsightMemory()

@app.get("/")
def dashboard():
    return render_template("dashboard.html", stats=get_stats(), recent=get_recent())

@app.get("/capture")
def capture():
    return render_template("capture.html")

@app.post("/api/experiences")
def api_create_experience():
    data = request.get_json(silent=True) or request.form.to_dict()
    required = ["experience_type", "title", "situation", "outcome", "success_or_failure", "lesson_learned"]
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        return jsonify({"ok": False, "error": "Please complete required fields.", "fields": missing}), 400

    exp_id = f"EXP-{datetime.now().year}-{uuid4().hex[:6].upper()}"
    record = {
        "experience_id": exp_id,
        "experience_type": data["experience_type"].strip(),
        "title": data["title"].strip(),
        "situation": data["situation"].strip(),
        "context": data.get("context", "").strip(),
        "action_taken": data.get("action_taken", "").strip(),
        "reason_for_action": data.get("reason_for_action", "").strip(),
        "outcome": data["outcome"].strip(),
        "success_or_failure": data["success_or_failure"].strip(),
        "root_cause": data.get("root_cause", "").strip(),
        "lesson_learned": data["lesson_learned"].strip(),
        "challenges": data.get("challenges", "").strip(),
        "department": data.get("department", "Other").strip(),
        "author": data.get("author", "").strip(),
        "verification_status": data.get("verification_status", "Human-Verified Experience").strip()
    }
    # Save app metadata first; memory failure must not lose the submitted experience.
    create_experience(record)
    memory_result = memory.retain(record)
    return jsonify({
        "ok": True, "experience_id": exp_id, "memory": memory_result,
        "message": "Experience saved locally." if not memory_result["stored"] else "Experience captured and stored in Hindsight."
    }), 201

if __name__ == "__main__":
    app.run(debug=True)
