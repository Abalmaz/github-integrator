import unittest

from flask_script import Manager
from flask_migrate import MigrateCommand


from github_integration import create_app, db


manager = Manager(create_app)

manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command('db', MigrateCommand)


@manager.command
def create_database():
    """Create all database tables."""
    db.create_all()


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
