from flask import Blueprint, jsonify, request
import jwt
import os
from queries.datos_queries import obtener_datos

datos_bp = Blueprint('datos', __name__)

@datos_bp.route('/api/datos-json', methods=['GET'])
def datos():

    token = request.args.get("token")

    if not token:
        return jsonify({"error": "Token requerido"}), 401

    try:
        jwt.decode(token, os.getenv("JWT_SECRET", "dev-secret"), algorithms=["HS256"])
    except:
        return jsonify({"error": "Token inválido"}), 401

    data = obtener_datos()
    return jsonify(data), 200