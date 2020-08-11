import unittest

from src import db
from src.auth.models import GitHubUser
from src.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_decode_personal_token(self):
        user = GitHubUser(
            github_access_token='test_personal_token'
        )
        db.session.add(user)
        db.session.commit()
        personal_token = GitHubUser.decode_personal_token(
            user.github_access_token)
        self.assertEqual(personal_token, 'test_personal_token')


if __name__ == '__main__':
    unittest.main()
