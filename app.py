from flask import *
from database import init_db, db_session
from models import *
from civpol import * 

civpol = CivPol()
civpol.run()

app = Flask(__name__)

app.secret_key = "alH6Ez6WF48O+MDUWQ=="

@app.route("/", methods=("GET", "POST"))
def login():
    if "username" not in session:
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            code = civpol.loginUser(username, password)

            if code == 0:
                session["username"] = username
                return redirect(url_for("issues"))
            elif code == 1:
                flash("The username or password are incorrect.", "info")
                return render_template("login.html")
            elif code == 2:
                flash("Insufficient amount of information entered.", "info")
                return render_template("login.html")
    else:
        return redirect(url_for("issues"))

@app.route("/signup", methods=("GET", "POST"))
def signup():
    if "username" not in session:
        if request.method == "GET":
            return render_template("signup.html")
        elif request.method == "POST":
            displayName = request.form["displayName"]
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            confirmPassword = request.form["confirmPassword"]

            if password == confirmPassword:
                code = civpol.registerUser(username, email, displayName, password)
                if code == 0:
                    session["username"] = username
                    return redirect(url_for("issues"))
                elif code == 1:
                    flash("The username is already taken", "info")
                    return render_template("signup.html")
                elif code == 2:
                    flash("Insufficient amount of information entered.", "info")
                    return render_template("signup.html")
            else:
                flash("The passwords do not match, try again.", "info")
                return render_template("signup.html")
    else:
        return redirect(url_for("login"))

@app.route("/issues", methods=("GET", "POST"))
def issues():
    if "username" in session:
        if request.method == "GET":
            return render_template("issues.html", issueList=civpol.issueFeed())
        elif request.method == "POST":
            if "issueNum" in request.form:
                revIssue = request.form["issueNum"]
                revIssueNum = int(revIssue)
                civpol.setIssue(revIssueNum)
                return redirect(url_for("policies"))
            elif "title" in request.form and "content" in request.form:
                postTitle = request.form["title"]
                postContent = request.form["content"]
                civpol.createIssue(postTitle, postContent)

                return render_template("issues.html", issueList=civpol.issueFeed())

    else:
        return redirect(url_for("login"))

@app.route("/policies", methods=("GET", "POST"))
def policies():
    if "username" in session:
        if request.method == "GET":
            return render_template("policies.html", policyList=civpol.policyFeed())
        elif request.method == "POST":
            postTitle = request.form["title"]
            postContent = request.form["content"]
            civpol.createPolicy(postTitle, postContent)
            return render_template("policies.html", policyList=civpol.policyFeed())

    else:
        return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "username" in session:
        print(civpol.issuesNum)
        return render_template("profile.html", user=civpol.currentUser, dateOfCreation=civpol.dateOfCreation(), issues=civpol.issuesNum(), policies=civpol.policiesNum())
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
