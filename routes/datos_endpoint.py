from flask import Blueprint, jsonify
from queries.datos_queries import obtener_datos

datos_bp = Blueprint('datos', __name__)

@datos_bp.route('/api/datos-json', methods=['GET'])
def datos():
    data = obtener_datos()
    return jsonify(data), 200