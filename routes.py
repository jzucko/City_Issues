print("ROUTES FILE LOADED")

from flask import render_template, request, redirect
from app import app, db, Issue
#from models import db

#from models import Issue

#INDEX
@app.route('/')
def index():
      print("INDEX ROUTE HIT")  # debug
      issues = Issue.query.all()
      return render_template('index.html', issues=issues)


#CREATE
@app.route('/create', methods= ['GET', 'POST'])
def create():
     print("CREATE ROUTE HIT")  # debug
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