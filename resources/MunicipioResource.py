from flask_restful import Resource, fields, marshal_with, reqparse, abort
from models.Municipio import Municipio
from models.Microrregiao import Microrregiao
from models.Mesorregiao import Mesorregiao
from models.UF import UF
from helpers.database import db

municipio_fields = {
    "id": fields.Integer,
    "nome": fields.String,
    "microrregiao_id": fields.Integer,
    "microrregiao_nome": fields.String,
    "mesorregiao_id": fields.Integer,
    "mesorregiao_nome": fields.String,
    "uf_id": fields.Integer,
    "uf_nome": fields.String,
    "uf_sigla": fields.String,
    "regiao_id": fields.Integer,
    "regiao_nome": fields.String,
    "regiao_sigla": fields.String
}

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, default=1, location='args')
pagination_parser.add_argument('per_page', type=int, default=10, location='args')

post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument('nome', type=str, required=True, help='Nome é obrigatório')
post_put_parser.add_argument('microrregiao_id', type=int, required=True, help='Microrregião ID é obrigatório')
post_put_parser.add_argument('mesorregiao_id', type=int, required=True, help='Mesorregião ID é obrigatório')
post_put_parser.add_argument('uf_id', type=int, required=True, help='UF ID é obrigatório')

class MunicipioResource(Resource):
    @marshal_with(municipio_fields)
    def get(self, id=None):
        if id is not None:
            municipio = Municipio.query.get(id)
            if not municipio:
                abort(404, message="Município não encontrado")
            return municipio

        args = pagination_parser.parse_args()
        page = args['page']
        per_page = args['per_page']

        query = Municipio.query.paginate(page=page, per_page=per_page, error_out=False)
        return query.items

    @marshal_with(municipio_fields)
    def post(self):
        args = post_put_parser.parse_args()

        micro = Microrregiao.query.get(args['microrregiao_id'])
        meso = Mesorregiao.query.get(args['mesorregiao_id'])
        uf = UF.query.get(args['uf_id'])

        if not micro or not meso or not uf:
            abort(400, message="Microrregião, Mesorregião ou UF não encontrada")

        municipio = Municipio(
            nome=args['nome'],
            microrregiao_id=micro.id,
            microrregiao_nome=micro.nome,
            mesorregiao_id=meso.id,
            mesorregiao_nome=meso.nome,
            uf_id=uf.id,
            uf_nome=uf.nome,
            uf_sigla=uf.sigla,
            regiao_id=uf.regiao_id,
            regiao_nome=uf.regiao_nome,
            regiao_sigla=uf.regiao_nome[:1]  # ajustar se tiver sigla
        )
        db.session.add(municipio)
        db.session.commit()
        return municipio, 201

    @marshal_with(municipio_fields)
    def put(self, id):
        args = post_put_parser.parse_args()
        municipio = Municipio.query.get(id)
        if not municipio:
            abort(404, message="Município não encontrado")

        micro = Microrregiao.query.get(args['microrregiao_id'])
        meso = Mesorregiao.query.get(args['mesorregiao_id'])
        uf = UF.query.get(args['uf_id'])

        if not micro or not meso or not uf:
            abort(400, message="Microrregião, Mesorregião ou UF não encontrada")

        municipio.nome = args['nome']
        municipio.microrregiao_id = micro.id
        municipio.microrregiao_nome = micro.nome
        municipio.mesorregiao_id = meso.id
        municipio.mesorregiao_nome = meso.nome
        municipio.uf_id = uf.id
        municipio.uf_nome = uf.nome
        municipio.uf_sigla = uf.sigla
        municipio.regiao_id = uf.regiao_id
        municipio.regiao_nome = uf.regiao_nome
        municipio.regiao_sigla = uf.regiao_nome[:1]  # ajustar se tiver sigla

        db.session.commit()
        return municipio, 200

    def delete(self, id):
        municipio = Municipio.query.get(id)
        if not municipio:
            abort(404, message="Município não encontrado")

        db.session.delete(municipio)
        db.session.commit()
        return '', 204
