from flask_restful import Resource, fields, marshal_with, reqparse, abort
from models.Mesorregiao import Mesorregiao
from models.Microrregiao import Microrregiao
from models.Municipio import Municipio
from models.UF import UF
from helpers.database import db

mesorregiao_fields = {
    "id": fields.Integer,
    "nome": fields.String,
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
post_put_parser.add_argument('uf_id', type=int, required=True, help='UF ID é obrigatório')


class MesorregiaoResource(Resource):
    @marshal_with(mesorregiao_fields)
    def get(self, id=None):
        if id is not None:
            meso = Mesorregiao.query.get(id)
            if not meso:
                abort(404, message="Mesorregião não encontrada")
            return meso

        args = pagination_parser.parse_args()
        page = args['page']
        per_page = args['per_page']

        query = Mesorregiao.query.paginate(page=page, per_page=per_page, error_out=False)
        return query.items

    @marshal_with(mesorregiao_fields)
    def post(self):
        args = post_put_parser.parse_args()

        uf = UF.query.get(args['uf_id'])
        if not uf:
            abort(400, message="UF não encontrada")

        meso = Mesorregiao(
            nome=args['nome'],
            uf_id=uf.id,
            uf_nome=uf.nome,
            uf_sigla=uf.sigla,
            regiao_id=uf.regiao_id,
            regiao_nome=uf.regiao_nome,
            regiao_sigla=uf.regiao_nome[:1]  # ajuste se tiver sigla real
        )
        db.session.add(meso)
        db.session.commit()
        return meso, 201

    @marshal_with(mesorregiao_fields)
    def put(self, id):
        args = post_put_parser.parse_args()
        meso = Mesorregiao.query.get(id)
        if not meso:
            abort(404, message="Mesorregião não encontrada")

        uf = UF.query.get(args['uf_id'])
        if not uf:
            abort(400, message="UF não encontrada")

        meso.nome = args['nome']
        meso.uf_id = uf.id
        meso.uf_nome = uf.nome
        meso.uf_sigla = uf.sigla
        meso.regiao_id = uf.regiao_id
        meso.regiao_nome = uf.regiao_nome
        meso.regiao_sigla = uf.regiao_nome[:1]  # ajuste se tiver sigla real

        db.session.commit()
        return meso, 200

    def delete(self, id):
        meso = Mesorregiao.query.get(id)
        if not meso:
            abort(404, message="Mesorregião não encontrada")

        db.session.delete(meso)
        db.session.commit()
        return '', 204
