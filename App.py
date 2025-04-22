import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Caminho do JSON
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'dados_pb_pe_rn.json') 

with open(json_path, 'r', encoding='utf-8') as f:
    instituicoes = json.load(f)

@app.route('/instituicoesensino', methods=['GET'])
def listar_instituicoes():
    return jsonify(instituicoes), 200

@app.route('/instituicoesensino/<co_entidade>', methods=['GET'])
def obter_instituicao(co_entidade):
    for inst in instituicoes:
        if str(inst.get('CO_ENTIDADE')) == str(co_entidade):
            return jsonify(inst), 200
    return jsonify({'erro': 'Instituição não encontrada'}), 404

@app.route('/instituicoesensino/<co_entidade>', methods=['DELETE'])
def deletar_instituicao(co_entidade):
    global instituicoes
    tamanho_antes = len(instituicoes)
    instituicoes = [i for i in instituicoes if str(i.get('CO_ENTIDADE')) != str(co_entidade)]
    if len(instituicoes) == tamanho_antes:
        return jsonify({'erro': 'Instituição não encontrada'}), 404
    return jsonify({'mensagem': 'Instituição removida com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)

