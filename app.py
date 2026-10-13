
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from src.predict import predict_with_confidence

app = Flask(__name__)
app.secret_key = "phishing_detection_secret_key_2026"

users = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/index")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return redirect(url_for("detect"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            return render_template(
                "register.html",
                error="Please enter username, email and password."
            )

        if username in users:
            return render_template(
                "register.html",
                error="Username already exists. Please login."
            )

        for user in users.values():
            if user["email"].lower() == email.lower():
                return render_template(
                    "register.html",
                    error="Email already registered. Please login."
                )

        users[username] = {
            "email": email,
            "password": generate_password_hash(password)
        }

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username not in users:
            return render_template(
                "login.html",
                error="Username not found. Please register first."
            )

        if not check_password_hash(users[username]["password"], password):
            return render_template(
                "login.html",
                error="Incorrect password. Please try again."
            )

        session["logged_in"] = True
        session["username"] = username
        session["email"] = users[username]["email"]

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        email=session.get("email")
    )


@app.route("/detect", methods=["GET", "POST"])
def detect():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    result = None
    confidence = None
    url = ""

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url:
            return render_template(
                "index.html",
                error="Please enter a website URL.",
                url=url
            )

        try:
            result, confidence = predict_with_confidence(url)

        except Exception:
            return render_template(
                "index.html",
                error="Unable to predict this URL. Please check your model and URL features.",
                url=url
            )

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        url=url
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
