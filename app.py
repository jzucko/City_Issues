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
    if 'user_id' not in session:
         return redirect('/login')
    
    issues = Issue.query.filter_by(user_id = session['user_id']).all()
    return render_template("index.html", issues=issues)


#CREATE
@app.route("/create", methods=["GET", "POST"])
def create():
    if 'user_id' not in session:
         return redirect('/login')
    
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        issue = Issue(
             title=title, 
             description=description,
             user_id=session['user_id']
             )

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

        #check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
             return 'Username already exists.'

        hashed_password = generate_password_hash(password)

        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")



#LOGIN
@app.route("/login", methods=['GET', 'POST'] )
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
             session['user_id'] = user.id
             session['username'] = username

             return redirect("/")
    
        return 'Invalid credentials.'

    return render_template("login.html")



with app.app_context():
        db.create_all()
        users = User.query.all()
        print('USERS:', users)
        for u in users:
             print(u.username, u.password)
        
        

if __name__ == '__main__':
    app.run(debug=True)

