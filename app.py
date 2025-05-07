from flask import Flask, request, jsonify
import sqlite3

from models.InstituicaoEnsino import InstituicaoEnsino

app = Flask(__name__)


@app.route("/")
def index():
    versao = {"versao": "0.0.1"}
    return jsonify(versao), 200


@app.get("/instituicoes")
def instituicoesResource():
    print("Get - Instituições")
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    offset = (page - 1) * per_page

    try:
        instituicoesEnsino = []

        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_instituicao LIMIT  ? OFFSET ?', (per_page, offset))
        resultSet = cursor.fetchall()

        for row in resultSet:
            id = row[0]
            no_regiao = row[1]
            sg_uf = row[2]
            no_municipio = row[3]
            no_mesorregiao = row[4]
            no_microrregiao = row[5]
            co_entidade = row[6]
            qt_mat_bas = row[7]
            co_regiao = row[8]
            co_uf = row[9]
            co_municipio = row[10]
            co_microrregiao = row[11]
            co_mesorregiao = row[12]

            instituicaoEnsino = InstituicaoEnsino(
                id, no_regiao, sg_uf, no_municipio, no_mesorregiao, no_microrregiao,
                co_entidade, qt_mat_bas, co_regiao, co_uf, co_municipio, co_microrregiao, co_mesorregiao
            )
            instituicoesEnsino.append(instituicaoEnsino.toDict())

    except sqlite3.Error:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

    return jsonify(instituicoesEnsino), 200


def validarInstituicao(content):
    isValido = True
    if (len(content['no_municipio']) < 3 or content['no_municipio'].isdigit()):
        isValido = False
    if (not str(content['co_entidade']).isdigit()):
        isValido = False
    if (not str(content['qt_mat_bas']).isdigit()):
        isValido = False
    return isValido


@app.post("/instituicoes")
def instituicaoInsercaoResource():
    print("Post - Instituição")
    instituicaoJson = request.get_json()

    isValido = validarInstituicao(instituicaoJson)
    if isValido:
        values = (
            instituicaoJson['no_regiao'], instituicaoJson['sg_uf'], instituicaoJson['no_municipio'],
            instituicaoJson['no_mesorregiao'], instituicaoJson['no_microrregiao'], instituicaoJson['co_entidade'],
            instituicaoJson['qt_mat_bas'], instituicaoJson['co_regiao'], instituicaoJson['co_uf'],
            instituicaoJson['co_municipio'], instituicaoJson['co_microrregiao'], instituicaoJson['co_mesorregiao']
        )

        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO tb_instituicao (
                no_regiao, sg_uf, no_municipio, no_mesorregiao, no_microrregiao, 
                co_entidade, qt_mat_bas, co_regiao, co_uf, co_municipio, co_microrregiao, co_mesorregiao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            values
        )
        conn.commit()

        id = cursor.lastrowid
        instituicaoEnsino = InstituicaoEnsino(id, *values)
        conn.close()

        return jsonify(instituicaoEnsino.toDict()), 200

    return jsonify({"mensagem": "Não cadastrado"}), 406


@app.route("/instituicoes/<int:id>", methods=["DELETE"])
def instituicaoRemocaoResource(id):
    try:
        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tb_instituicao WHERE id = ?', (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        return jsonify({"mensagem": "Instituição removida com sucesso."}), 200

    except sqlite3.Error:
        return jsonify({"mensagem": "Erro ao acessar o banco de dados."}), 500
    finally:
        conn.close()


@app.route("/instituicoes/<int:id>", methods=["PUT"])
def instituicaoAtualizacaoResource(id):
    print("Put - Instituição")
    instituicaoJson = request.get_json()

    if not validarInstituicao(instituicaoJson):
        return jsonify({"mensagem": "Dados inválidos."}), 400

    try:
        values = (
            instituicaoJson['no_regiao'], instituicaoJson['sg_uf'], instituicaoJson['no_municipio'],
            instituicaoJson['no_mesorregiao'], instituicaoJson['no_microrregiao'], instituicaoJson['co_entidade'],
            instituicaoJson['qt_mat_bas'], instituicaoJson['co_regiao'], instituicaoJson['co_uf'],
            instituicaoJson['co_municipio'], instituicaoJson['co_microrregiao'], instituicaoJson['co_mesorregiao'], id
        )

        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tb_instituicao SET 
                no_regiao = ?, sg_uf = ?, no_municipio = ?, no_mesorregiao = ?, no_microrregiao = ?, 
                co_entidade = ?, qt_mat_bas = ?, co_regiao = ?, co_uf = ?, co_municipio = ?, 
                co_microrregiao = ?, co_mesorregiao = ?
            WHERE id = ?
        ''', values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoEnsino = InstituicaoEnsino(id, *values[:-1])
        return jsonify(instituicaoEnsino.toDict()), 200

    except sqlite3.Error:
        return jsonify({"mensagem": "Erro ao atualizar instituição."}), 500
    finally:
        conn.close()


@app.route("/instituicoes/<int:id>", methods=["GET"])
def instituicoesByIdResource(id):
    try:
        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_instituicao WHERE id = ?', (id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        instituicaoEnsino = InstituicaoEnsino(*row)
        return jsonify(instituicaoEnsino.toDict()), 200

    except sqlite3.Error:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
