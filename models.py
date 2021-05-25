from flask_login import UserMixin
from create_app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    login = db.Column(db.String(100))
    pwd = db.Column(db.String(100))
    mail = db.Column(db.String(100), unique=True)
    id_profil = db.Column(db.Integer)
    id_region = db.Column(db.Integer)
    id_magasin = db.Column(db.Integer)




