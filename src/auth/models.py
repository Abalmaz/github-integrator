from src import db
from src.auth.utils import encrypt_personal_token


class GitHubUser(db.Model):
    """
        The user table.
        Attributes:
            id (int): User unique identifier
            github_access_users (str): The GitHub personal
                                       access token(encrypted).
            github_id (int): The GitHub user's id.
            github_login (str): The GitHub user's login.
            admin (bool): User's role. If user is admin set it True
        """
    __tablename__ = 'github_users'

    id = db.Column(db.Integer, primary_key=True)
    github_access_token = db.Column(db.String(300))
    github_id = db.Column(db.Integer)
    github_login = db.Column(db.String(255))
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self,
                 github_access_token: str,
                 github_id: int = None,
                 github_login: str = None) -> None:
        self.github_access_token = encrypt_personal_token(
            github_access_token
        )
        self.github_id = github_id
        self.github_login = github_login

    def save(self):
        db.session.add(self)
        db.session.commit()
