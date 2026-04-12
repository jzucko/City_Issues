from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///issues.db"
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy()
db.init_app(app)

#MODELS
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

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





with app.app_context():
        db.create_all()
        #print("Tables created!")

if __name__ == '__main__':
    app.run(debug=True)

