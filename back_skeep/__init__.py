import os

from flask import Flask, Blueprint
from flask_restful import Api

from back_skeep.auth import Auth
from back_skeep.keeps import KeepList, Keep
from back_skeep.users import UserList, User


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from back_skeep.store import db
    db.init_app(app)

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    api.add_resource(UserList, '/users')
    api.add_resource(User, '/users/<user_id>')

    api.add_resource(KeepList, '/keeps')
    api.add_resource(Keep, '/keeps/<keep_id>')

    api.add_resource(Auth, '/auth')

    app.register_blueprint(api_bp)

    return app
