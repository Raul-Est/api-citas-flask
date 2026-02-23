from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.utils.db import get_db

from . import usuarios_bp


@usuarios_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """
    Obtiene el perfil del usuario autenticado
    ---
    tags:
      - Usuarios
    security:
      - Bearer: []
    summary: Obtiene el perfil del usuario actual
    description: Devuelve la información del perfil del usuario autenticado.
    responses:
      200:
        description: Perfil del usuario
        schema:
          type: object
          properties:
            username:
              type: string
              description: Nombre de usuario
            name:
              type: string
              description: Nombre del usuario
            lastname:
              type: string
              description: Apellido del usuario
            email:
              type: string
              description: Correo electrónico del usuario
            phone:
              type: string
              description: Teléfono del usuario
            date:
              type: string
              description: Fecha de nacimiento en formato DD/MM/YYYY
              example: "25/12/1990"
      404:
        description: Usuario no encontrado
    """
    current_user = get_jwt_identity()
    db = get_db()
    user = db["usuarios"].find_one({"username": current_user}, {"_id": 0, "password": 0})

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(user), 200
