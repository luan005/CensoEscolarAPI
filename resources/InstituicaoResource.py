from flask import request
from flask_restful import Resource, fields, marshal
from sqlalchemy.exc import SQLAlchemyError
from helpers.database import db
from helpers.logging import logger
from models.Instituicao import Instituicao

instituicao_fields = {
    'id': fields.Integer,
    'nu_ano_censo': fields.Integer,
    'no_regiao': fields.String,
    'sg_uf': fields.String,
    'no_municipio': fields.String,
    'no_mesorregiao': fields.String,
    'no_microrregiao': fields.String,
    'co_entidade': fields.String,
    'qt_mat_bas': fields.String,
    'co_regiao': fields.String,
    'co_uf': fields.String,
    'co_municipio': fields.Integer,
    'co_microrregiao': fields.String,
    'co_mesorregiao': fields.String
}

class InstituicoesResource(Resource):
    def get(self):
        logger.info("GET - Lista de Instituições com paginação")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))

        try:
            pagination = db.session.query(Instituicao).paginate(page=page, per_page=per_page, error_out=False)
            return {
                "total": pagination.total,
                "page": page,
                "per_page": per_page,
                "data": marshal(pagination.items, instituicao_fields)
            }, 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao consultar instituições: {e}")
            return {"mensagem": "Erro ao consultar instituições."}, 500

    def post(self):
        logger.info("POST - Criar nova Instituição")
        content = request.get_json()

        campos = [
            'nu_ano_censo', 'no_regiao', 'sg_uf', 'no_municipio',
            'no_mesorregiao', 'no_microrregiao', 'co_entidade',
            'qt_mat_bas', 'co_regiao', 'co_uf', 'co_municipio',
            'co_microrregiao', 'co_mesorregiao'
        ]

        if not all(field in content for field in campos):
            logger.warning("POST - Campos ausentes")
            return {"mensagem": "Campos obrigatórios ausentes."}, 400

        try:
            nova = Instituicao(**{k: content[k] for k in campos})
            db.session.add(nova)
            db.session.commit()
            return marshal(nova, instituicao_fields), 201
        except SQLAlchemyError as e:
            logger.error(f"Erro ao inserir instituição: {e}")
            db.session.rollback()
            return {"mensagem": "Erro ao inserir instituição."}, 500


class InstituicaoResource(Resource):
    def get(self, id):
        logger.info(f"GET - Instituição {id}")
        try:
            instituicao = db.session.query(Instituicao).filter_by(co_entidade=id).first()
            if not instituicao:
                return {"mensagem": "Instituição não encontrada."}, 404
            return marshal(instituicao, instituicao_fields), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar instituição: {e}")
            return {"mensagem": "Erro ao buscar instituição."}, 500

    def put(self, id):
        logger.info(f"PUT - Atualizar Instituição {id}")
        content = request.get_json()

        campos = [
            'nu_ano_censo', 'no_regiao', 'sg_uf', 'no_municipio',
            'no_mesorregiao', 'no_microrregiao', 'co_entidade',
            'qt_mat_bas', 'co_regiao', 'co_uf', 'co_municipio',
            'co_microrregiao', 'co_mesorregiao'
        ]

        if not all(field in content for field in campos):
            logger.warning("PUT - Campos ausentes")
            return {"mensagem": "Campos obrigatórios ausentes."}, 400

        try:
            instituicao = db.session.query(Instituicao).filter_by(co_entidade=id).first()
            if not instituicao:
                return {"mensagem": "Instituição não encontrada."}, 404

            for campo in campos:
                setattr(instituicao, campo, content[campo])

            db.session.commit()
            return marshal(instituicao, instituicao_fields), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar instituição: {e}")
            db.session.rollback()
            return {"mensagem": "Erro ao atualizar instituição."}, 500

    def delete(self, id):
        logger.info(f"DELETE - Remover Instituição {id}")
        try:
            instituicao = db.session.query(Instituicao).filter_by(co_entidade=id).first()
            if not instituicao:
                return {"mensagem": "Instituição não encontrada."}, 404

            db.session.delete(instituicao)
            db.session.commit()
            return {"mensagem": "Instituição removida com sucesso."}, 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao remover instituição: {e}")
            db.session.rollback()
            return {"mensagem": "Erro ao remover instituição."}, 500
