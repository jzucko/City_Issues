print("ROUTES FILE LOADED")

from app import app
from models import db
from flask import render_template, request, redirect
from models import Issue

#HOME
@app.route('/')
def index():
      issues = Issue.query.all()
      return render_template('index.html', issues=issues)


#CREATE
@app.route('/create', methods= ['GET', 'POST'])
def create():
     if request.method == 'POST':
          title = request.form['title']
          description = request.form['description'] #issue.user_id = current_user.id

          issue = Issue(title = title, 
                        description = description
               )
          db.session.add(issue)
          db.session.commit()

          return redirect('/')
     return render_template('create.html')