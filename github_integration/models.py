from github_integration import db
from itsdangerous import encoding


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    github_access_token = db.Column(db.String(255))
    github_id = db.Column(db.Integer)
    github_login = db.Column(db.String(255))
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, github_access_token, github_id, github_login):
        self.github_access_token = encoding.base64_encode(
            github_access_token
        ),
        self.github_id = github_id,
        self.github_login = github_login

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def decode_auth_token(auth_token):
        return encoding.base64_encode(auth_token)
