import unittest

from src import db
from src.auth.models import GitHubUser
from src.auth.utils import decode_personal_token
from src.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encrypt_personal_token(self):
        user = GitHubUser(
            github_access_token='test_token'
        )
        db.session.add(user)
        db.session.commit()
        self.assertFalse(
            user.github_access_token == 'test_token'
        )

    def test_decode_personal_token(self):
        user = GitHubUser(
            github_access_token='test_token'
        )
        db.session.add(user)
        db.session.commit()
        github_token = user.github_access_token

        self.assertTrue(
            decode_personal_token(github_token) == 'test_token'
        )


if __name__ == '__main__':
    unittest.main()
