import jwt

from config import get_val
from github_integration import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    github_access_token = db.Column(db.String(255))
    github_id = db.Column(db.Integer)
    github_login = db.Column(db.String(255))
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, github_access_token):
        self.github_access_token = jwt.encode(
            github_access_token, get_val("SECRET_KEY"),
            algorithm='HS256'
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            token = jwt.decode(auth_token, get_val("SECRET_KEY"))
            return token['sub']
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
