from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.utils.db import get_db

from . import citas_bp


def _format_dates(dates):
    result = []
    for date in dates:
        date["date"] = f"{date['day']} {date['hour']}:00:00"
        del date["day"]
        del date["hour"]
        result.append(date)
    result.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y %H:00:00"))
    return result


@citas_bp.route("/date/create", methods=["POST"])
@jwt_required()
def create_date():
    """
    Crea una nueva cita
    ---
    tags:
      - Citas
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - center
            - date
          properties:
            center:
              type: string
              description: Nombre del centro (debe existir en /centers)
              example: "Centro de Salud Madrid Norte"
            date:
              type: string
              description: Fecha y hora en formato DD/MM/YYYY HH:00:00
              example: "25/12/2025 14:00:00"
    responses:
      201:
        description: Cita creada correctamente
        schema:
          type: object
          properties:
            msg:
              type: string
              example: Cita creada correctamente
      400:
        description: Formato de fecha inválido o centro no encontrado
      409:
        description: La franja horaria ya está ocupada en ese centro
      422:
        description: Faltan campos requeridos
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    center = data.get("center", "").strip()
    date_str = data.get("date", "").strip()

    if not center or not date_str:
        return jsonify({"error": "center y date son requeridos"}), 422

    db = get_db()

    if not db["centros"].find_one({"name": center}):
        return jsonify({"error": "Centro no encontrado"}), 400

    try:
        parsed_date = datetime.strptime(date_str, "%d/%m/%Y %H:00:00")
        day = parsed_date.strftime("%d/%m/%Y")
        hour = parsed_date.strftime("%H")
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Usar DD/MM/YYYY HH:00:00"}), 400

    if db["citas"].find_one({"day": day, "hour": hour, "center": center}):
        return jsonify({"error": "La franja horaria ya está ocupada en ese centro"}), 409

    current_user = get_jwt_identity()
    db["citas"].insert_one({
        "username": current_user,
        "day": day,
        "hour": hour,
        "center": center,
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    })

    return jsonify({"msg": "Cita creada correctamente"}), 201


@citas_bp.route("/date/getByDay", methods=["POST"])
@jwt_required()
def get_dates_by_day():
    """
    Obtiene las citas de un día concreto
    ---
    tags:
      - Citas
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - day
          properties:
            day:
              type: string
              description: Fecha en formato DD/MM/YYYY
              example: "25/12/2025"
    responses:
      200:
        description: Lista de citas para el día indicado
        schema:
          type: array
          items:
            type: object
            properties:
              username:
                type: string
              date:
                type: string
                example: "25/12/2025 14:00:00"
              center:
                type: string
      400:
        description: Parámetro day requerido o formato inválido
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    day = data.get("day", "").strip()
    if not day:
        return jsonify({"error": "El parámetro day es requerido"}), 400

    try:
        datetime.strptime(day, "%d/%m/%Y")
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Usar DD/MM/YYYY"}), 400

    db = get_db()
    dates = db["citas"].find({"day": day, "cancel": {"$ne": 1}}, {"_id": 0})
    return jsonify(_format_dates(list(dates))), 200


@citas_bp.route("/date/getByUser", methods=["GET"])
@jwt_required()
def get_dates_by_user():
    """
    Obtiene las citas del usuario autenticado
    ---
    tags:
      - Citas
    security:
      - Bearer: []
    summary: Obtiene las citas del usuario autenticado
    description: Devuelve todas las citas no canceladas del usuario que realiza la petición.
    responses:
      200:
        description: Lista de citas del usuario
        schema:
          type: array
          items:
            type: object
            properties:
              username:
                type: string
              date:
                type: string
                example: "25/12/2025 14:00:00"
              center:
                type: string
              created_at:
                type: string
    """
    current_user = get_jwt_identity()
    db = get_db()
    dates = db["citas"].find({"username": current_user, "cancel": {"$ne": 1}}, {"_id": 0})
    return jsonify(_format_dates(list(dates))), 200


@citas_bp.route("/date/delete", methods=["POST"])
@jwt_required()
def delete_date():
    """
    Cancela una cita existente
    ---
    tags:
      - Citas
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - date
            - center
          properties:
            date:
              type: string
              description: Fecha y hora de la cita en formato DD/MM/YYYY HH:00:00
              example: "25/12/2025 14:00:00"
            center:
              type: string
              description: Nombre del centro de la cita
              example: "Centro de Salud Madrid Norte"
    responses:
      200:
        description: Cita cancelada correctamente
        schema:
          type: object
          properties:
            msg:
              type: string
              example: Cita cancelada correctamente
      400:
        description: Formato de fecha inválido o cita no encontrada
      401:
        description: No autorizado para cancelar esta cita
      422:
        description: Faltan campos requeridos
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    center = data.get("center", "").strip()
    date_str = data.get("date", "").strip()

    if not center or not date_str:
        return jsonify({"error": "center y date son requeridos"}), 422

    try:
        parsed_date = datetime.strptime(date_str, "%d/%m/%Y %H:00:00")
        day = parsed_date.strftime("%d/%m/%Y")
        hour = parsed_date.strftime("%H")
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Usar DD/MM/YYYY HH:00:00"}), 400

    db = get_db()
    cita = db["citas"].find_one({"day": day, "hour": hour, "center": center})

    if not cita:
        return jsonify({"error": "Cita no encontrada"}), 404

    current_user = get_jwt_identity()
    if cita["username"] != current_user:
        return jsonify({"error": "No autorizado para cancelar esta cita"}), 401

    db["citas"].update_one(
        {"day": day, "hour": hour, "center": center},
        {"$set": {"cancel": 1}},
    )

    return jsonify({"msg": "Cita cancelada correctamente"}), 200


@citas_bp.route("/dates", methods=["GET"])
@jwt_required()
def get_all_dates():
    """
    Obtiene todas las citas no canceladas
    ---
    tags:
      - Citas
    security:
      - Bearer: []
    summary: Obtiene todas las citas no canceladas
    description: Devuelve todas las citas activas del sistema, ordenadas por fecha.
    responses:
      200:
        description: Lista de todas las citas no canceladas
        schema:
          type: array
          items:
            type: object
            properties:
              username:
                type: string
              date:
                type: string
                example: "25/12/2025 14:00:00"
              center:
                type: string
              created_at:
                type: string
    """
    db = get_db()
    dates = db["citas"].find({"cancel": {"$ne": 1}}, {"_id": 0})
    return jsonify(_format_dates(list(dates))), 200
