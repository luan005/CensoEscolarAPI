from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from helpers.database import db
from resources.InstituicaoResource import InstituicoesResource, InstituicaoResource

from models.UF import UF
from models.Mesorregiao import Mesorregiao
from models.Microrregiao import Microrregiao
from models.Municipio import Municipio
from models.Instituicao import Instituicao


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost:5432/censoescolar"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

api = Api(app)

# Corrigido:
api.add_resource(InstituicoesResource, "/instituicoes")
api.add_resource(InstituicaoResource, "/instituicoes/<string:id>")

if __name__ == "__main__":
    app.run(debug=True)
