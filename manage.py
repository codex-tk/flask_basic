import os, unittest

from flask import url_for
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import create_app, db
from app.main.model import user
from app.main.model import blacklist

from app import blueprint
from app.main.controller.sample_view_controller import sample_view_controller

# this boilerplate code are from https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/

app = create_app(os.getenv('FLASK_BASIC_ENV') or 'dev')
app.register_blueprint(blueprint)
app.register_blueprint(sample_view_controller)
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

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@manager.command
def list_routes():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    for line in sorted(links):
        print(line)

# python manage.py db init
# Each time the database model changes, repeat the migrate and upgrade commands
# python manage.py db migrate --message 'initial database migration'
# python manage.py db upgrade
if __name__ == '__main__':
    manager.run()
