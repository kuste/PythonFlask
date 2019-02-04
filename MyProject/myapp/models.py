from datetime import datetime
from myapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    savedMovies = db.relationship('Movies', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Movies(db.Model):
    IMDB_link = db.Column(db.String(100) ,primary_key = True, unique=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Movies('{self.IMDB_link}','{self.user_id}')"
