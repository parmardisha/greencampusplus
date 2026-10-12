import math

from flask import Flask, jsonify, render_template, request

from database import add_activity, delete_activity, get_activities, get_summary, init_db
from sustainability import CATEGORIES, calculate_emissions

app = Flask(__name__)
init_db()


@app.get("/")
def index():
    return render_template("index.html", categories=CATEGORIES)


@app.get("/api/dashboard")
def dashboard():
    return jsonify(
        summary=get_summary(),
        activities=get_activities(),
        categories=CATEGORIES,
    )


@app.post("/api/activities")
def create_activity():
    data = request.get_json(silent=True) or {}
    category = data.get("category")
    description = str(data.get("description", "")).strip()

    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify(error="Enter a valid amount."), 400

    if category not in CATEGORIES:
        return jsonify(error="Choose a supported activity."), 400
    if not description:
        return jsonify(error="Enter a description."), 400
    if len(description) > 120:
        return jsonify(error="Description must be 120 characters or fewer."), 400
    if not math.isfinite(amount) or amount <= 0:
        return jsonify(error="Amount must be a finite number greater than zero."), 400

    emissions = calculate_emissions(category, amount)
    activity = add_activity(description, category, amount, emissions)
    return jsonify(activity), 201


@app.delete("/api/activities/<int:activity_id>")
def remove_activity(activity_id):
    if not delete_activity(activity_id):
        return jsonify(error="Activity not found."), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
