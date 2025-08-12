# resources/UfResource.py

from flask_restful import Resource, fields, marshal_with, reqparse, abort
from models.UF import UF  # <- Correto agora
from helpers.database import db

uf_fields = {
    "id": fields.Integer,
    "sigla": fields.String,
    "nome": fields.String,
    "regiao_id": fields.String,
    "regiao_nome": fields.String,
}

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, default=1, location='args')
pagination_parser.add_argument('per_page', type=int, default=10, location='args')

post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument('sigla', type=str, required=True, help='Sigla é obrigatória')
post_put_parser.add_argument('nome', type=str, required=True, help='Nome é obrigatório')
post_put_parser.add_argument('regiao_id', type=str, required=True, help='ID da região é obrigatório')
post_put_parser.add_argument('regiao_nome', type=str, required=True, help='Nome da região é obrigatório')


class UFResource(Resource):
    @marshal_with(uf_fields)
    def get(self, id=None):
        if id is not None:
            uf = UF.query.get(id)
            if not uf:
                abort(404, message="UF não encontrada")
            return uf

        args = pagination_parser.parse_args()
        page = args['page']
        per_page = args['per_page']

        query = UF.query.paginate(page=page, per_page=per_page, error_out=False)
        return query.items

    @marshal_with(uf_fields)
    def post(self):
        args = post_put_parser.parse_args()
        uf = UF(
            sigla=args['sigla'],
            nome=args['nome'],
            regiao_id=args['regiao_id'],
            regiao_nome=args['regiao_nome']
        )
        db.session.add(uf)
        db.session.commit()
        return uf, 201

    @marshal_with(uf_fields)
    def put(self, id):
        args = post_put_parser.parse_args()
        uf = UF.query.get(id)
        if not uf:
            abort(404, message="UF não encontrada")

        uf.sigla = args['sigla']
        uf.nome = args['nome']
        uf.regiao_id = args['regiao_id']
        uf.regiao_nome = args['regiao_nome']
        db.session.commit()
        return uf, 200

    def delete(self, id):
        uf = UF.query.get(id)
        if not uf:
            abort(404, message="UF não encontrada")

        db.session.delete(uf)
        db.session.commit()
        return '', 204
