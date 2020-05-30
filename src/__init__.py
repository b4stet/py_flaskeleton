import os
import yaml
from flask import Flask, Blueprint, g

from src.include.services import services
from src.include.clis import clis
from src.include.routing import routing


def bootstrap_core(config_file, env):
    app = Flask(
        __name__,
        instance_path=os.path.dirname(os.path.dirname(__file__)),
    )

    # set config
    config = config_from_yaml(config_file, env)
    app.config.update(config)
    app.debug = app.config['app']['debug']
    return app


def bootstrap_web(config_file, env):
    app = bootstrap_core(config_file, env)
    app.config['mode'] = 'web'

    # register components and return app
    with app.app_context():
        register_services(app)
        register_routes(app, g.di_container)
        return app


def bootstrap_cli(config_file, env):
    app = bootstrap_core(config_file, env)
    app.config['mode'] = 'cli'

    # register components and return app
    with app.app_context():
        register_services(app)
        register_commands(app, g.di_container)
        return app


def config_from_yaml(config_file, env):
    with open(config_file, mode='r') as f:
        config = yaml.safe_load(f)
    app_config = config.get(env, config)
    app_config['env'] = env
    return app_config


def register_services(app):
    for service in services:
        service().init_app(app)


def register_routes(app, di_container):
    for bp_name, actions in routing.items():
        blueprint = Blueprint(name=bp_name, import_name=__name__)

        for middleware in actions['middlewares']:
            blueprint.before_request(di_container[middleware])

        for route in actions['routes']:
            blueprint.add_url_rule(route['uri'], view_func=di_container[route['action']], methods=route['methods'])

        app.register_blueprint(blueprint)


def register_commands(app, di_container):
    for cli in clis:
        di_container[cli].init_app(app)
