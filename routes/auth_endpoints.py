import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, jsonify, request

from queries.auth_queries import crear_usuario, obtener_clientes


auth_bp = Blueprint("auth", __name__)


def _get_bearer_token() -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header.replace("Bearer ", "", 1).strip() or None


def _verificar_jwt() -> tuple[bool, dict | None]:
    token = _get_bearer_token()
    if not token:
        return False, None

    secret = os.getenv("JWT_SECRET", "dev-secret")
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return True, payload
    except Exception:
        return False, None


@auth_bp.route("/admin/create-user", methods=["POST"])
def admin_create_user():
    if request.headers.get("Authorization") != "Bearer ADMIN_SECRET":
        return jsonify({"error": "No autorizado"}), 401

    data = request.get_json(silent=True) or {}
    email = data.get("email")
    passwd = data.get("passwd")

    if not email or not passwd:
        return jsonify({"error": "Faltan campos: email y passwd"}), 400

    result = crear_usuario(email=email, passwd=passwd)
    
    if not result.get("ok"):
        return jsonify({"error": result.get("error", "No se pudo crear el usuario")}), 500

    secret = os.getenv("JWT_SECRET", "dev-secret")
    exp_minutes = int(os.getenv("JWT_EXPIRES_MINUTES", "10080"))
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(result.get("usuario_id")),
        "email": email,
        "rol_id": 3,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=exp_minutes)).timestamp()),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")

    return jsonify({
        "message": "Usuario creado",
        "token": token,
        "usuario_id": result.get("usuario_id")
    }), 201
    
@auth_bp.route("/admin/clientes", methods=["GET"])
def obtener_clientes_endpoint():

    if request.headers.get("Authorization") != "Bearer ADMIN_SECRET":
        return jsonify({"error": "No autorizado"}), 401

    clientes = obtener_clientes()

    return jsonify(clientes), 200