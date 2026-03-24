from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "skillify_secret"

# ---------------- DATABASE ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anushka333",
    database="skillify"
)

cursor = db.cursor(dictionary=True)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
            (username, email, password, role)
        )
        db.commit()

        return redirect("/login")

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session["user"] = user["email"]
            session["role"] = user["role"]

            if user["role"] == "student":
                return redirect("/dashboard_student")
            else:
                return redirect("/dashboard_mentor")

        return "Invalid Login"

    return render_template("login.html")

# ---------------- STUDENT DASHBOARD ----------------
@app.route("/dashboard_student")
def dashboard_student():
    if "user" in session:
        return render_template("dashboard_student.html")
    return redirect("/login")

# ---------------- MENTOR DASHBOARD ----------------
@app.route("/dashboard_mentor")
def dashboard_mentor():
    if "user" in session:
        return render_template("dashboard_mentor.html")
    return redirect("/login")

# ---------------- ADD SKILL ----------------
@app.route("/add_skill", methods=["POST"])
def add_skill():
    skill = request.form["skill"]
    user = session["user"]

    cursor.execute(
        "INSERT INTO skills (user_email, skill_name) VALUES (%s,%s)",
        (user, skill)
    )
    db.commit()

    return redirect("/dashboard_mentor")

# ---------------- SHOW SKILLS ----------------
@app.route("/browse_skills")
def browse_skills():
    cursor.execute("SELECT * FROM skills")
    skills = cursor.fetchall()

    return render_template("browse_skills.html", skills=skills)

# ---------------- REQUEST SKILL ----------------
@app.route("/request_skill", methods=["POST"])
def request_skill():
    learner = session["user"]
    mentor = request.form["mentor"]
    skill = request.form["skill"]

    cursor.execute(
        "INSERT INTO requests (learner_email, mentor_email, skill_name, status) VALUES (%s,%s,%s,%s)",
        (learner, mentor, skill, "pending")
    )
    db.commit()

    return redirect("/browse_skills")

# ---------------- MENTOR REQUESTS ----------------
@app.route("/mentor_requests")
def mentor_requests():
    user = session["user"]

    cursor.execute(
        "SELECT * FROM requests WHERE mentor_email=%s",
        (user,)
    )
    data = cursor.fetchall()

    return render_template("mentor_requests.html", data=data)

# ---------------- ACCEPT REQUEST ----------------
@app.route("/accept_request", methods=["POST"])
def accept_request():
    id = request.form["id"]

    cursor.execute(
        "UPDATE requests SET status='accepted' WHERE id=%s",
        (id,)
    )
    db.commit()

    return redirect("/mentor_requests")

# ---------------- PROFILE ----------------
@app.route("/profile", methods=["GET", "POST"])
def profile():
    user = session["user"]

    if request.method == "POST":
        bio = request.form["bio"]
        github = request.form["github"]

        cursor.execute(
            "INSERT INTO profile (email, bio, github) VALUES (%s,%s,%s)",
            (user, bio, github)
        )
        db.commit()

    cursor.execute("SELECT * FROM profile WHERE email=%s", (user,))
    data = cursor.fetchone()

    return render_template("profile.html", data=data)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)