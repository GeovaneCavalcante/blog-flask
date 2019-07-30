import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
db = SQLAlchemy(app)

class Posting(db.Model):

   __tablename__ = 'Postings'

   id = db.Column('id', db.Integer, primary_key = True, autoincrement=True)
   author = db.Column(db.String(20))
   title = db.Column(db.String(40))  
   description = db.Column(db.String(100))
   text = db.Column(db.Text(5000))
   created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

   def __init__(self, author, title, description, text):
       self.author = author
       self.title = title
       self.description = description
       self.text = text

db.create_all()

@app.route('/')
def index():
     
    postings = Posting.query.all()

    return render_template('posting.html', postings=postings)


@app.route('/new', methods=['GET', 'POST'])
def new_posting():

    if request.method == 'POST':
        data = {
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'text': request.form.get('text'),
        }
       
        posting = Posting(**data)
        db.session.add(posting)
        db.session.commit()

        return redirect('/')
       


    return render_template('form_post.html')

@app.route('/postings/<int:post_id>')
def detail_posting(post_id):
    posting = Posting.query.filter_by(id=post_id).first()

    return render_template('detail_post.html', posting=posting)
