from flask import Flask, render_template, request, redirect, url_for
from models import db, Issue, User
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session



app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///issues.db"
app.config['SECRET_KEY'] = 'secret'

db.init_app(app)


#INDEX    
@app.route("/")
def index():
    
    issues = Issue.query.all()
    return render_template("index.html", issues=issues)


#CREATE
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        issue = Issue(title=title, description=description)

        db.session.add(issue)
        db.session.commit()

        return redirect("/")

    return render_template("create.html")


#REGISTER
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")



#LOGIN
@app.route("/login", )
def login():
    """if request.method == "DELETE":
        title = request.form["title"]
        description = request.form["description"]

        issue = Issue(title=title, description=description)

        db.session.add(issue)
        db.session.commit()

        return redirect("/login")"""

    return render_template("login.html")



with app.app_context():
        db.create_all()
        users = User.query.all()
        print('USERS:', users)
        for u in users:
             print(u.username, u.password)
        
        

if __name__ == '__main__':
    app.run(debug=True)

