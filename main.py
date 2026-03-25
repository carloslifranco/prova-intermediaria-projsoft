from flask import Flask, request, jsonify
from models import Pagamento 
from pymongo import MongoClient
from bson import ObjectId
import requests
import os


app = Flask(__name__)

mongo_host = os.getenv("MONGO_URL", "localhost")
users_host = os.getenv("USERS_API_URL", "localhost")

MONGO_URL = f"mongodb://{mongo_host}:27017"
USERS_API_URL = f"http://{users_host}/users/"

db = MongoClient(MONGO_URL)['pagamentos'] #nome do banco de dados


@app.route('/pagamento', methods=['POST'])
def create_pagamento():
    data = request.json
    usuario_id = data.get('usuario_id')
    
    if not usuario_id:
        return jsonify({"erro": "ID do usuário é obrigatório"}), 400

    try:
        response = requests.get(f"{USERS_API_URL}{usuario_id}")
        
        # Se a API de usuários retornar 404, o usuário não existe
        if response.status_code == 404:
            return jsonify({"erro": "Usuário inexistente. Pagamento rejeitado."}), 404
        
        user_data = response.json()
        usuario_email = user_data.get("email") 

    except requests.exceptions.RequestException:
        return jsonify({"erro": "Serviço de validação indisponível"}), 503


    valor_pagamento = float(data.get("valor_pagamento", 0))
    num_parcelas = int(data.get("parcelas", 1))
    valor_parcela = valor_pagamento / num_parcelas if num_parcelas > 0 else valor_pagamento


    novo_pagamento = Pagamento (
        usuario_id=usuario_id,
        usuario_email=usuario_email, 
        codigo=data.get('codigo'),
        valor_pagamento=valor_pagamento,
        tipo_pagamento=data.get('tipo_pagamento'),
        parcelas=num_parcelas,
        valor_parcela=valor_parcela,
        data_pagamento=data.get('data_pagamento')
    )

    #Salvando no Mongo
    resultado = db.pagamentos.insert_one(novo_pagamento.to_dict())
    
    return jsonify({"mensagem": "Pagamento criado!", "id": str(resultado.inserted_id)}), 201


@app.route('/pagamento', methods=['GET'])
def get_pagamento():
    cliente_id = request.args.get('usuario_id')
    
    filtro = {}
    if cliente_id:
        filtro = {"usuario_id": cliente_id}

    pagamentos = list(db.pagamentos.find(filtro))
    
    # Tratamento para transformar o ObjectId do Mongo em String
    for p in pagamentos:
        p['_id'] = str(p['_id'])

    return jsonify(pagamentos), 200

@app.route('/pagamento/<id>', methods=['DELETE'])
def delete_pagamento(id):
    try:
        resultado = db.pagamentos.delete_one({"_id": ObjectId(id)})
        if resultado.deleted_count == 0:
            return jsonify({"erro": "Pagamento não encontrado"}), 404
        return jsonify({"mensagem": "Pagamento removido"}), 200
    except:
        return jsonify({"erro": "ID inválido"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)