from flask_script import Manager
from flask_migrate import MigrateCommand
from github_integration import models


from github_integration import create_app, db


manager = Manager(create_app)

manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command('db', MigrateCommand)


@manager.command
def create_database():
    """Create all database tables."""
    db.create_all()


if __name__ == '__main__':
    manager.run()
