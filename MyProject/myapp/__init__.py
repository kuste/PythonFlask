from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '7f27d8f7dd9fed2abd01e03f27fe15d8a1bd4c9c33ed8dfd05cdeec2b9abbc0f'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
babel = Babel(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from myapp import routes
