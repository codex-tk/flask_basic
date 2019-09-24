import os, unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import create_app, db
from app.main.model import user
from app import blueprint

# this boilerplate code are from https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/

app = create_app(os.getenv('FLASK_BASIC_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


# python manage.py run
@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests"""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


# python manage.py db init
# Each time the database model changes, repeat the migrate and upgrade commands
# python manage.py db migrate --message 'initial database migration'
# python manage.py db upgrade
if __name__ == '__main__':
    manager.run()
