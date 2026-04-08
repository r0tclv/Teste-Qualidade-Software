from app import app, init_db
import tempfile
import os


def before_all(context):
    context.app = app
    context.app.config['TESTING'] = True


def before_scenario(context, scenario):
    context.test_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    context.test_db.close()
    context.app.config['DATABASE'] = context.test_db.name
    app.config['DATABASE'] = context.test_db.name
    init_db()
    context.client = context.app.test_client()


def after_scenario(context, scenario):
    if hasattr(context, 'test_db') and os.path.exists(context.test_db.name):
        os.remove(context.test_db.name)
