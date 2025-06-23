from flask import Flask, request, render_template
import sqlite3
from flask import send_from_directory
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)

# Ladataan .env-tiedoston muuttujat käyttöön
load_dotenv()

# Haetaan sähköpostitiedot
EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")


def send_welcome_email(to_email):
    subject = "Tervetuloa uutiskirjeeseen!"
    body = "Kiitos liittymisestä. Tästä alkaa matkamme!"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "antakaatoita@gmail.com"
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:            
            server.starttls()                   
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print("Sähköposti lähetetty:", to_email)
    except Exception as e:
        print("Virhe lähetyksessä:", e)



@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory('media', filename)

# Tietokannan alustus
def init_db():
    conn = sqlite3.connect('subscriptions.db', timeout=10)
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
        with sqlite3.connect("subscriptions.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
            conn.commit()
    except sqlite3.IntegrityError:
        return "Sähköposti on jo rekisteröity.", 400
    except Exception as e:
        print("Virhe tietokannassa:", e)
        return "Palvelinvirhe", 500

    try:
        send_welcome_email(email)
    except Exception as e:
        print("Sähköpostin lähetys epäonnistui:", e)

    return "Kiitos tilauksesta!", 200



if __name__ == "__main__":
    init_db()
    app.run(debug=True)
