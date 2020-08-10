from github_integration import db, encryption_type


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
        self.github_access_token = encryption_type.encrypt(
            github_access_token.encode('ascii')).decode('ascii')
        self.github_id = github_id
        self.github_login = github_login

    def save(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def decode_personal_token(access_token):
        return encryption_type.decrypt(
            access_token.encode('ascii')
        ).decode('ascii')
