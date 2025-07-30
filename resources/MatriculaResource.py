from flask_restful import Resource
from flask import jsonify, request
from helpers.database import getConnection

class MatriculasPorEstadoResource(Resource):
    def get(self):
        ano = request.args.get("ano", default="2023")

        conn = getConnection()
        cursor = conn.cursor()

        if ano == "all":
            query = """
                SELECT sg_uf, SUM(CAST(qt_mat_bas AS NUMERIC)) AS total_matriculas
                FROM tb_instituicao
                GROUP BY sg_uf
                ORDER BY sg_uf;
            """
            cursor.execute(query)
        else:
            query = """
                SELECT sg_uf, SUM(CAST(qt_mat_bas AS NUMERIC)) AS total_matriculas
                FROM tb_instituicao
                WHERE nu_ano_censo = %s
                GROUP BY sg_uf
                ORDER BY sg_uf;
            """
            cursor.execute(query, (ano,))

        rows = cursor.fetchall()
        conn.close()

        resultado = {row[0]: float(row[1]) for row in rows}
        return jsonify(resultado)
