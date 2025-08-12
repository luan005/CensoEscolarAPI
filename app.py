from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from helpers.database import db, migrate
from models.UF import UF
from models.Mesorregiao import Mesorregiao
from models.Microrregiao import Microrregiao
from models.Municipio import Municipio
from models.Instituicao import Instituicao

from resources.InstituicaoResource import InstituicoesResource, InstituicaoResource
from resources.UFResource import UFResource
from resources.MesorregiaoResource import MesorregiaoResource
from resources.MicrorregiaoResource import MicrorregiaoResource
from resources.MunicipioResource import MunicipioResource
from resources.CensoEscolarResource import CensoEscolarPorEstadoResource

app = Flask(__name__)
CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost:5432/censoescolar"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
migrate.init_app(app, db)

api = Api(app)

# Endpoints
api.add_resource(InstituicoesResource, "/instituicoes")
api.add_resource(InstituicaoResource, "/instituicoes/<string:id>")
api.add_resource(UFResource, "/ufs", "/ufs/<int:id>")
api.add_resource(MesorregiaoResource, "/mesorregioes", "/mesorregioes/<int:id>")
api.add_resource(MicrorregiaoResource, "/microrregioes", "/microrregioes/<int:id>")
api.add_resource(MunicipioResource, "/municipios", "/municipios/<int:id>")
api.add_resource(CensoEscolarPorEstadoResource, "/censoescolar")


if __name__ == "__main__":
    app.run(debug=True)
