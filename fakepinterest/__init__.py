
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
#Variável que define o endereço do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
#Variável que define a criptografia secreta
app.config["SECRET_KEY"] = "af78cfa9a6d28478f96e74181f86fa3"
#Variável que define o endereço das fotos postadas
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fakepinterest import routes