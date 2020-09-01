from sqlalchemy import Column, Integer, String, Boolean

from src.auth.utils import encrypt_personal_token
from src.database import Base, db_session


class GitHubUser(Base):
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

    id = Column(Integer, primary_key=True)
    github_access_token = Column(String(300))
    github_id = Column(Integer)
    github_login = Column(String(255))
    github_email = Column(String(100))
    admin = Column(Boolean, nullable=False, default=False)

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
        db_session.add(self)
        db_session.commit()
