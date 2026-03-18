from flask import Blueprint, jsonify
from queries.datos_queries import obtener_datos
from routes.auth_endpoints import _verificar_jwt

datos_bp = Blueprint('datos', __name__)

@datos_bp.route('/api/datos-json', methods=['GET'])
def datos():
    ok, payload = _verificar_jwt()
    
    if not ok:
        return jsonify({'error': 'No autorizado'}), 401
     
    data = obtener_datos()
    return jsonify(data), 200