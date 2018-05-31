from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

#Model for Users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    books = db.relationship('Book', backref='poster', lazy='dynamic')

    #How to print objects of this class
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


#Model for Posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # #user_id is a foreign key. user refers to the table and .id refers to the column
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True, unique=False)
    author = db.Column(db.String(256), index=True, unique=False)
    genre = db.Column(db.String(64))
    format = db.Column(db.String(64))
    time_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    on_shelf = db.Column(db.Boolean, index=True, unique=False)

    def __repr__(self):
        return '<Book {}>'.format(self.title)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def load_book(id):
    return Book.query.get(int(id))
