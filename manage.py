#!/usr/bin/env/env python
import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app = app, User = User, Role = Role, db = db)

manager.add_command("shell", Shell(make_context = make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def test():
    """run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity = 2).run(tests)


@manager.command
def deploy():
    """Run the deploy tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # upgrade the database
    upgrade()

    # create the user's role (roles table)
    Role.insert_roles()

    # make every users follow himself
    User.add_self_follows()




if __name__ == '__main__':
    manager.run()
