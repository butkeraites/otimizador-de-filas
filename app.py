import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from otimizador_filas import otimizar_filas, otimizar_distancia

app = Flask(__name__)
api = Api(app)

def maximizar_alunos(posted_data):
    if  ('largura_sala' in posted_data) and \
        ('comprimento_sala' in posted_data) and \
        ('largura_cadeira' in posted_data) and \
        ('comprimento_cadeira' in posted_data) and \
        ('num_carteiras' in posted_data) and \
        ('largura_corredores' in posted_data) and \
        ('distancia_minima' in posted_data):
        
        largura_sala = posted_data['largura_sala']
        comprimento_sala = posted_data['comprimento_sala']
        largura_cadeira = posted_data['largura_cadeira']
        comprimento_cadeira = posted_data['comprimento_cadeira']
        num_carteiras = posted_data['num_carteiras']
        largura_corredores = posted_data['largura_corredores']
        distancia_minima = posted_data['distancia_minima']

        return jsonify(otimizar_filas(largura_sala,
                                    comprimento_sala,
                                    largura_cadeira,
                                    comprimento_cadeira,
                                    num_carteiras,
                                    largura_corredores,
                                    distancia_minima))
    else:
        return jsonify({'erro' : 'Chave nao encontrada'})

def maximizar_distancia(posted_data):
    if  ('largura_sala' in posted_data) and \
        ('comprimento_sala' in posted_data) and \
        ('largura_cadeira' in posted_data) and \
        ('comprimento_cadeira' in posted_data) and \
        ('num_carteiras' in posted_data) and \
        ('largura_corredores' in posted_data) and \
        ('numero_de_alunos' in posted_data):
        
        largura_sala = posted_data['largura_sala']
        comprimento_sala = posted_data['comprimento_sala']
        largura_cadeira = posted_data['largura_cadeira']
        comprimento_cadeira = posted_data['comprimento_cadeira']
        num_carteiras = posted_data['num_carteiras']
        largura_corredores = posted_data['largura_corredores']
        numero_de_alunos = posted_data['numero_de_alunos']

        return jsonify(otimizar_distancia(largura_sala,
                                    comprimento_sala,
                                    largura_cadeira,
                                    comprimento_cadeira,
                                    num_carteiras,
                                    largura_corredores,
                                    numero_de_alunos))
    else:
        return jsonify({'erro' : 'Chave nao encontrada'})
class OtimizarFilas(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
        if posted_data:
            if ('modelo' in posted_data):
                if (posted_data['modelo'] == 'max_alunos'):
                    return maximizar_alunos(posted_data)
                else:
                    return maximizar_distancia(posted_data)
        else:
            return jsonify({'erro' : 'Mensagem vazia'})

api.add_resource(OtimizarFilas, '/otimizar-filas')

if __name__ == '__main__':
    app.run(debug=True)