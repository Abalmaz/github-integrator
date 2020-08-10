from github_integration import db
from github_integration.utils import encrypt_personal_token


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    github_access_token = db.Column(db.String(255))
    github_id = db.Column(db.Integer)
    github_login = db.Column(db.String(255))
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, github_access_token,
                 github_id=None,
                 github_login=None):
        self.github_access_token = encrypt_personal_token(
            github_access_token)
        self.github_id = github_id
        self.github_login = github_login

    def save(self):
        db.session.add(self)
        db.session.commit()
