from flask_restful import Resource, fields, marshal_with, reqparse, abort
from models.Microrregiao import Microrregiao
from models.Mesorregiao import Mesorregiao
from models.UF import UF
from helpers.database import db

microrregiao_fields = {
    "id": fields.Integer,
    "nome": fields.String,
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
post_put_parser.add_argument('mesorregiao_id', type=int, required=True, help='Mesorregião ID é obrigatório')
post_put_parser.add_argument('uf_id', type=int, required=True, help='UF ID é obrigatório')


class MicrorregiaoResource(Resource):
    @marshal_with(microrregiao_fields)
    def get(self, id=None):
        if id is not None:
            micro = Microrregiao.query.get(id)
            if not micro:
                abort(404, message="Microrregião não encontrada")
            return micro

        args = pagination_parser.parse_args()
        page = args['page']
        per_page = args['per_page']

        query = Microrregiao.query.paginate(page=page, per_page=per_page, error_out=False)
        return query.items

    @marshal_with(microrregiao_fields)
    def post(self):
        args = post_put_parser.parse_args()

        meso = Mesorregiao.query.get(args['mesorregiao_id'])
        uf = UF.query.get(args['uf_id'])
        if not meso or not uf:
            abort(400, message="Mesorregião ou UF não encontrada")

        micro = Microrregiao(
            nome=args['nome'],
            mesorregiao_id=meso.id,
            mesorregiao_nome=meso.nome,
            uf_id=uf.id,
            uf_nome=uf.nome,
            uf_sigla=uf.sigla,
            regiao_id=uf.regiao_id,
            regiao_nome=uf.regiao_nome,
            regiao_sigla=uf.regiao_nome[:1]  # ajustar se sigla real existir
        )
        db.session.add(micro)
        db.session.commit()
        return micro, 201

    @marshal_with(microrregiao_fields)
    def put(self, id):
        args = post_put_parser.parse_args()
        micro = Microrregiao.query.get(id)
        if not micro:
            abort(404, message="Microrregião não encontrada")

        meso = Mesorregiao.query.get(args['mesorregiao_id'])
        uf = UF.query.get(args['uf_id'])
        if not meso or not uf:
            abort(400, message="Mesorregião ou UF não encontrada")

        micro.nome = args['nome']
        micro.mesorregiao_id = meso.id
        micro.mesorregiao_nome = meso.nome
        micro.uf_id = uf.id
        micro.uf_nome = uf.nome
        micro.uf_sigla = uf.sigla
        micro.regiao_id = uf.regiao_id
        micro.regiao_nome = uf.regiao_nome
        micro.regiao_sigla = uf.regiao_nome[:1]  # ajustar se sigla real existir

        db.session.commit()
        return micro, 200

    def delete(self, id):
        micro = Microrregiao.query.get(id)
        if not micro:
            abort(404, message="Microrregião não encontrada")

        db.session.delete(micro)
        db.session.commit()
        return '', 204
