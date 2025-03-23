
from flask import Flask
from flasgger import Swagger

from modules.main.route import main_bp
from modules.site.route import site_bp
from modules.access.route import access_bp


def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(main_bp, url_prefix='/')
        app.register_blueprint(site_bp, url_prefix='/site/')
        app.register_blueprint(access_bp, url_prefix='/access/')

# def initialize_db(app: Flask):
#     with app.app_context():
#         db.init_app(app)
#         db.create_all()


def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger
