from flask_testing import TestCase

from app import app
from github_integration import db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
