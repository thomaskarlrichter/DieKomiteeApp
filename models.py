from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    erstellt_am = db.Column(db.DateTime, default=datetime.utcnow)

    wortmeldungen = db.relationship(
        'Wortmeldung', backref='autor', lazy='dynamic',
        cascade='all, delete-orphan'
    )
    rueckmeldungen = db.relationship(
        'Rueckmeldung', backref='autor', lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Wortmeldung(db.Model):
    __tablename__ = 'wortmeldungen'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    datum_uhrzeit = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    rueckmeldungen = db.relationship(
        'Rueckmeldung', backref='wortmeldung', lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Wortmeldung {self.id} von User {self.user_id}>'


class Rueckmeldung(db.Model):
    __tablename__ = 'rueckmeldungen'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    datum_uhrzeit = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wortmeldung_id = db.Column(db.Integer, db.ForeignKey('wortmeldungen.id'), nullable=False)

    def __repr__(self):
        return f'<Rueckmeldung {self.id} zu Wortmeldung {self.wortmeldung_id}>'
