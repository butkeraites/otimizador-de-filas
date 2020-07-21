import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from otimizador_filas import otimizar_filas

app = Flask(__name__)
api = Api(app)

class OtimizarFilas(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
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

api.add_resource(OtimizarFilas, '/otimizar-filas')

if __name__ == '__main__':
    app.run(debug=True)