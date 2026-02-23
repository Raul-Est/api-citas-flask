from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config

_swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda model: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "uiversion": 3,
    "oauth_config": {},
}

_swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Clínica",
        "description": "Documentación de la API para agendar citas",
        "version": "0.0.1",
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Añade 'Bearer <tu_token>' para autenticación. Ejemplo: 'Bearer eye...'",
        }
    },
    "security": [{"Bearer": []}],
}


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app)
    JWTManager(app)
    Swagger(app, template=_swagger_template, config=_swagger_config)

    from app.blueprints.auth import auth_bp
    from app.blueprints.centros import centros_bp
    from app.blueprints.citas import citas_bp
    from app.blueprints.usuarios import usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(centros_bp)
    app.register_blueprint(citas_bp)
    app.register_blueprint(usuarios_bp)

    return app
