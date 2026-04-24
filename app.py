from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "skillify_secret"

# DATABASE CONNECTION
db = mysql.connector.connect(
    host="localhost", user="root", password="anushka333", database="skillify"
)
cursor = db.cursor(dictionary=True)


# --- HELPER FUNCTIONS ---

def go_home():
    """Redirects authenticated users to their correct dashboard."""
    if session.get("role") == "mentor":
        return redirect("/dashboard_mentor")
    return redirect("/dashboard_student")

def render_dashboard():
    """Renders the appropriate dashboard template safely based on role."""
    if "email" not in session:
        return redirect("/login")
    
    if session.get("role") == "mentor":
        return render_template("dashboard_mentor.html", name=session.get("name"))
    
    return render_template("dashboard_student.html", name=session.get("name"))


# --- ROUTES ---

# Homepage
@app.route("/")
def home():
    if "email" in session:
        return go_home()
    return redirect("/login")


# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
            (data["username"], data["email"], data["password"], data["role"])
        )
        db.commit()
        return redirect("/login")
    
    return render_template("signup.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" in session:
        return go_home()

    if request.method == "POST":
        data = request.form
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (data["email"], data["password"]))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user.get("id", user.get("user_id", ""))
            session["name"] = user["name"]
            session["email"] = user["email"]
            session["role"] = user["role"]
            return go_home()
            
        return "Invalid Login"

    return render_template("login.html")


# Dashboards (Merged rendering logic for safety)
@app.route("/dashboard_student")
def dashboard_student():
    return render_dashboard()

@app.route("/dashboard_mentor")
def dashboard_mentor():
    return render_dashboard()


# Browse matching mentors
@app.route("/browse")
def browse():
    if "email" not in session:
        return redirect("/login")
    
    cursor.execute("SELECT * FROM users WHERE role='mentor'")
    return render_template("browse.html", mentors=cursor.fetchall())


# Profile settings
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "email" not in session:
        return redirect("/login")
    
    user_email = session["email"]
    
    if request.method == "POST":
        data = request.form
        cursor.execute("INSERT INTO profile (email, bio, github) VALUES (%s,%s,%s)", (user_email, data["bio"], data["github"]))
        db.commit()

    cursor.execute("SELECT * FROM profile WHERE email=%s", (user_email,))
    return render_template("profile.html", data=cursor.fetchone())


# System Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# Initialize App Setup
if __name__ == "__main__":
    app.run(debug=True)