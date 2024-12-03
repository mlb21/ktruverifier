from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_shelf_items(shelf_label):
    try:
        conn = sqlite3.connect('albums.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM album WHERE shelf_label = ?", (shelf_label,))
        items = [row[0] for row in cursor.fetchall()]
        return items
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}
    finally:
        conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", year="2024")

@app.route("/api/shelves/<shelf_label>", methods=["GET"])
def fetch_shelf_items(shelf_label):
    if not shelf_label:
        return jsonify({"error": "Shelf label is required."}), 400

    shelf_items = get_shelf_items(shelf_label)
    if isinstance(shelf_items, dict) and "error" in shelf_items:
        return jsonify(shelf_items), 500

    # Return the items under the 'barcodes' key to match the client-side expectation
    return jsonify({"barcodes": shelf_items}), 200

if __name__ == "__main__":
    app.run(debug=True)
