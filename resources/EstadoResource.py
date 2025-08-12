# resources/EstadoResource.py
from flask_restful import Resource
from flask import jsonify
from helpers.database import getConnection

class EstadoResource(Resource):
    def get(self, sigla):
        conn = getConnection()
        cursor = conn.cursor()
        query = """
            SELECT id, nome, sigla, regiao_id, regiao_nome
            FROM tb_uf
            WHERE sigla = %s
        """
        cursor.execute(query, (sigla.upper(),))
        row = cursor.fetchone()
        conn.close()

        if row:
            estado = {
                "id": row[0],
                "nome": row[1],
                "sigla": row[2],
                "regiao_id": row[3],
                "regiao_nome": row[4]
            }
            return jsonify(estado)
        return {"error": "Estado não encontrado"}, 404
