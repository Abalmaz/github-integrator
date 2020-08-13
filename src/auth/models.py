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
            github_email (str): The GitHub user's email.
            admin (bool): User's role. If user is admin set it True
        """
    __tablename__ = 'github_users'

    id = db.Column(db.Integer, primary_key=True)
    github_access_token = db.Column(db.String(300))
    github_id = db.Column(db.Integer)
    github_login = db.Column(db.String(255))
    github_email = db.Column(db.String(100))
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self,
                 github_access_token: str,
                 github_email: str,
                 github_id: int = None,
                 github_login: str = None) -> None:
        self.github_access_token = encrypt_personal_token(
            github_access_token
        )
        self.github_id = github_id
        self.github_login = github_login
        self.github_email = github_email

    def save(self):
        db.session.add(self)
        db.session.commit()
