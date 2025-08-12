from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from helpers.database import db

from resources.InstituicaoResource import InstituicaoResource

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost:5432/censoescolar"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)
    db.init_app(app)

    api = Api(app)

    # Registra os endpoints
    api.add_resource(InstituicaoResource, "/instituicoes")

    return app
