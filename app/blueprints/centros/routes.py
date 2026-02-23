from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app.utils.db import get_db

from . import centros_bp


@centros_bp.route("/centers", methods=["POST"])
@jwt_required()
def create_center():
    """
    Crea un nuevo centro médico
    ---
    tags:
      - Centros
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - address
          properties:
            name:
              type: string
              description: Nombre del centro
              example: "Centro de Salud Madrid Centro"
            address:
              type: string
              description: Dirección del centro
              example: "Calle Gran Vía, 1, Madrid"
            phone:
              type: string
              description: Teléfono del centro (opcional)
              example: "910000000"
    responses:
      201:
        description: Centro creado correctamente
        schema:
          type: object
          properties:
            msg:
              type: string
              example: Centro creado correctamente
      400:
        description: Solicitud incorrecta
      409:
        description: Ya existe un centro con ese nombre
      422:
        description: Faltan campos requeridos
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    name = data.get("name", "").strip()
    address = data.get("address", "").strip()
    phone = data.get("phone", "").strip()

    if not name or not address:
        return jsonify({"error": "name y address son requeridos"}), 422

    db = get_db()
    if db["centros"].find_one({"name": name}):
        return jsonify({"error": "Ya existe un centro con ese nombre"}), 409

    new_center = {"name": name, "address": address}
    if phone:
        new_center["phone"] = phone

    db["centros"].insert_one(new_center)

    return jsonify({"msg": "Centro creado correctamente"}), 201


@centros_bp.route("/centers", methods=["GET"])
@jwt_required()
def get_centers():
    """
    Obtiene una lista de todos los centros
    ---
    tags:
      - Centros
    security:
      - Bearer: []
    summary: Obtiene una lista de todos los centros
    description: Devuelve una lista en formato JSON de todos los centros disponibles.
    responses:
      200:
        description: Lista de centros
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                description: Nombre del centro
              address:
                type: string
                description: Dirección del centro
              phone:
                type: string
                description: Teléfono del centro
    """
    db = get_db()
    centers = db["centros"].find({}, {"_id": 0})
    return jsonify(list(centers)), 200
