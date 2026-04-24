from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash # ADDED FOR SECURITY

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
    
    user_email = session.get("email") # FIX: Use email instead of id
    role = session.get("role")
    
    # FETCH REQUESTS BASED ON ROLE
    if role == "mentor":
        # FIX: Database uses 'mentor_email' instead of 'mentor_id'
        cursor.execute("SELECT * FROM requests WHERE mentor_email=%s", (user_email,))
        requests_data = cursor.fetchall()
        return render_template("dashboard_mentor.html", name=session.get("name"), requests=requests_data)
    
    # For student
    # FIX: Database uses 'learner_email' instead of 'student_id'
    cursor.execute("SELECT * FROM requests WHERE learner_email=%s", (user_email,))
    requests_data = cursor.fetchall()
    return render_template("dashboard_student.html", name=session.get("name"), requests=requests_data)


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
        hashed_pw = generate_password_hash(data["password"]) # HASH PASSWORD
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
            (data["username"], data["email"], hashed_pw, data["role"]) # SAVE HASHED
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
        cursor.execute("SELECT * FROM users WHERE email=%s", (data["email"],)) # FETCH BY EMAIL ONLY
        user = cursor.fetchone()

        # VERIFY HASHED PASSWORD
        if user and check_password_hash(user["password"], data["password"]):
            session["user_id"] = user.get("id", user.get("user_id", ""))
            session["name"] = user["name"]
            session["email"] = user["email"]
            session["role"] = user["role"]
            return go_home()
            
        return "Invalid Login"

    return render_template("login.html")


# Forgot Password
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        new_password = request.form["new_password"]
        
        # Check if email exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            hashed_pw = generate_password_hash(new_password) # Hash new password
            cursor.execute("UPDATE users SET password=%s WHERE email=%s", (hashed_pw, email))
            db.commit()
            return redirect("/login")
        return "Email not found"
        
    return render_template("forgot_password.html")


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