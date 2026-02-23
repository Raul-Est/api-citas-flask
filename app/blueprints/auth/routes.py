from datetime import datetime

import bcrypt
from flask import jsonify, request
from flask_jwt_extended import create_access_token

from app.utils.db import get_db

from . import auth_bp


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Iniciar sesión en la aplicación
    ---
    tags:
      - Autenticación
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "admin"
            password:
              type: string
              example: "admin123"
    responses:
      200:
        description: Token de acceso generado correctamente
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Credenciales incorrectas
        schema:
          type: object
          properties:
            error:
              type: string
              example: Credenciales incorrectas
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    db = get_db()
    user = db["usuarios"].find_one({"username": username})

    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Credenciales incorrectas"}), 401


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Autenticación
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "juanperez"
            password:
              type: string
              example: "mipassword123"
            name:
              type: string
              example: "Juan"
            lastname:
              type: string
              example: "Pérez"
            email:
              type: string
              example: "juan@email.com"
            phone:
              type: string
              example: "600000000"
            date:
              type: string
              format: date
              example: "25/12/1990"
              description: Fecha de nacimiento en formato DD/MM/YYYY
    responses:
      201:
        description: Usuario creado correctamente
        schema:
          type: object
          properties:
            msg:
              type: string
              example: Usuario creado correctamente
      400:
        description: Solicitud incorrecta o formato de fecha inválido
      409:
        description: El nombre de usuario ya existe
      422:
        description: Faltan campos requeridos
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username y password son requeridos"}), 422

    date_str = data.get("date", "")
    if date_str:
        try:
            date_str = datetime.strptime(date_str, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Usar DD/MM/YYYY"}), 400

    db = get_db()
    if db["usuarios"].find_one({"username": username}):
        return jsonify({"error": "El nombre de usuario ya existe"}), 409

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user = {
        "username": username,
        "password": hashed_password,
        "name": data.get("name", "").strip(),
        "lastname": data.get("lastname", "").strip(),
        "email": data.get("email", "").strip(),
        "phone": data.get("phone", "").strip(),
        "date": date_str,
    }
    db["usuarios"].insert_one(user)

    return jsonify({"msg": "Usuario creado correctamente"}), 201
