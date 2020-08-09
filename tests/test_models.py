import unittest

from github_integration import db
from github_integration.models import User
from tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_decode_personal_token(self):
        user = User(
            github_access_token='test_personal_token'
        )
        db.session.add(user)
        db.session.commit()
        personal_token = User.decode_personal_token(user.github_access_token)
        self.assertEqual(personal_token, 'test_personal_token')


if __name__ == '__main__':
    unittest.main()
