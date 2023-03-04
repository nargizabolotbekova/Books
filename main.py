from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(300), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(300), nullable=False)
    cover = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    available = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
     return f'{self.id} - {self.title}'
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    posts = Books.query.order_by(Books.date.desc()).all()
    return render_template('posts.html', books=posts)


@app.route('/create', methods=['POST', 'GET'])
def create_books():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        books = Books(title=title, intro=intro, text=text)
        db.session.add(books)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('create_post.html')
    
@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
def update_books(id):
    post = Books.query.get(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.intro = request.form['intro']
        post.text = request.form['text']

        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('update.html', article=post)



@app.route('/post/<int:id>')
def hello(id):
    post = Books.query.get(id)
    return render_template('post_detail.html', books=post)

@app.route('/post/<int:id>/delete')
def delete(id):
    post = Books.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Error while deleting'
    
    
if __name__ == '__main__':
    app.run(debug=True)