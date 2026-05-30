#!/usr/bin/env python3
"""
app.py -- Flask backend for the Word Slot Machine.

Routes:
  GET /                      -> the slot-machine page
  GET /api/categories        -> the category tree (with live word counts)
  GET /api/spin              -> N random words from a chosen category
                                params: category=<slug|all>, count=<1..3>

The word data lives in the normalized SQLite database built by build_data.py.
Run `python3 build_data.py` once before starting the server.
"""

import os
import sqlite3

from flask import Flask, g, jsonify, render_template, request

from scoring import score_word

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "words.db")

app = Flask(__name__)


def get_db():
    if "db" not in g:
        if not os.path.exists(DB_PATH):
            raise RuntimeError(
                "words.db not found. Run `python3 build_data.py` first."
            )
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/categories")
def categories():
    """Return the full category tree, each with its live word count."""
    db = get_db()
    rows = db.execute(
        """
        SELECT c.id, c.name, c.display_name, c.parent_id,
               c.description, c.sort_order,
               COUNT(wc.word_id) AS word_count
        FROM categories c
        LEFT JOIN word_categories wc ON wc.category_id = c.id
        GROUP BY c.id
        ORDER BY c.sort_order
        """
    ).fetchall()

    total = db.execute("SELECT COUNT(*) AS n FROM words").fetchone()["n"]

    return jsonify({
        "total_words": total,
        "categories": [dict(r) for r in rows],
    })


@app.route("/api/spin")
def spin():
    """Return random words from one category, or one category per slot."""
    categories = request.args.getlist("category")
    if not categories:
        categories = [request.args.get("category", "all")]

    try:
        count = int(request.args.get("count", 3))
    except (TypeError, ValueError):
        count = 3
    count = max(1, min(3, count))

    db = get_db()
    multi_category_spin = len(categories) > 1

    def random_word_rows(category, limit, excluded_ids=()):
        exclude_sql = ""
        exclude_params = []
        if excluded_ids:
            placeholders = ",".join("?" for _ in excluded_ids)
            exclude_sql = f" AND w.id NOT IN ({placeholders})"
            exclude_params = list(excluded_ids)

        if category == "all":
            return db.execute(
                f"""
                SELECT w.id, w.text, w.display_text, w.points
                FROM words w
                WHERE 1=1{exclude_sql}
                ORDER BY RANDOM() LIMIT ?
                """,
                (*exclude_params, limit),
            ).fetchall()

        cat = db.execute(
            "SELECT id FROM categories WHERE name = ?", (category,)
        ).fetchone()
        if cat is None:
            raise ValueError(category)
        return db.execute(
            f"""
            SELECT w.id, w.text, w.display_text, w.points
            FROM words w
            JOIN word_categories wc ON wc.word_id = w.id
            WHERE wc.category_id = ?{exclude_sql}
            ORDER BY RANDOM() LIMIT ?
            """,
            (cat["id"], *exclude_params, limit),
        ).fetchall()

    try:
        if multi_category_spin:
            rows = []
            selected_ids = set()
            for category in categories[:3]:
                picked = random_word_rows(category, 1, selected_ids)
                if not picked:
                    picked = random_word_rows(category, 1)
                if picked:
                    row = picked[0]
                    rows.append(row)
                    selected_ids.add(row["id"])
            category = "multiple"
            count = len(rows)
        else:
            category = categories[0]
            rows = random_word_rows(category, count)
    except ValueError as exc:
        return jsonify({"error": f"unknown category '{exc.args[0]}'"}), 400

    words = []
    for r in rows:
        labels = db.execute(
            """
            SELECT c.display_name
            FROM word_categories wc
            JOIN categories c ON c.id = wc.category_id
            WHERE wc.word_id = ?
            ORDER BY c.sort_order
            """,
            (r["id"],),
        ).fetchall()
        scoring = score_word(r["display_text"])
        words.append({
            "id": r["id"],
            "text": r["display_text"],
            "points": scoring["total"],
            "scoring": scoring,
            "categories": [x["display_name"] for x in labels],
        })

    return jsonify({"category": category, "count": count, "words": words})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
