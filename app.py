from flask import Flask, request, render_template
import sqlite3
from flask import send_from_directory




app = Flask(__name__)

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory('media', filename)

# Tietokannan alustus
def init_db():
    conn = sqlite3.connect('subscriptions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return "Sähköposti puuttuu", 400

    try:
        conn = sqlite3.connect("subscriptions.db")
        c = conn.cursor()
        c.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        conn.commit()
        return "Kiitos tilauksesta!", 200
    except sqlite3.IntegrityError:
        return "Sähköposti on jo rekisteröity.", 400
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
