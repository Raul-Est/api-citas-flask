"""Script de migración inicial para la base de datos Clinica.

Crea las colecciones necesarias y añade índices y datos de ejemplo
para que la API pueda funcionar desde el primer arranque.
"""
import os
import sys
from typing import Iterable

# Añadir el directorio raíz al path para poder importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymongo
from pymongo.database import Database
import bcrypt
from config import Config


def ensure_collections(db: Database, names: Iterable[str]) -> None:
    """Crea las colecciones listadas si no existen todavía."""
    existing = set(db.list_collection_names())
    for name in names:
        if name not in existing:
            db.create_collection(name)


def ensure_indexes(db: Database) -> None:
    """Configura índices básicos para las colecciones principales."""
    db["usuarios"].create_index("username", unique=True)
    db["citas"].create_index(
        [("day", pymongo.ASCENDING), ("hour", pymongo.ASCENDING), ("center", pymongo.ASCENDING)],
        unique=True,
        name="unique_date_per_center",
    )


def seed_centers(db: Database) -> None:
    """Inserta centros por defecto si la colección está vacía."""
    if db["centros"].count_documents({}) > 0:
        return

    db["centros"].insert_many(
        [
            {
                "name": "Centro de Salud Madrid Norte",
                "address": "Calle de la Salud, 123, Madrid",
            },
            {
                "name": "Centro Médico Madrid Sur",
                "address": "Avenida de la Medicina, 456, Madrid",
            },
        ]
    )


def seed_users(db: Database) -> None:
    """Inserta un usuario administrador por defecto si no existe."""
    users_col = db["usuarios"]
    if not users_col.find_one({"username": "admin"}):
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        users_col.insert_one({
            "username": "admin",
            "password": hashed_password,
            "name": "Admin",
            "lastname": "User",
            "email": "admin@example.com",
            "phone": "123456789",
            "date": "01/01/1980"
        })
        print("Created default admin user.")


def main() -> None:
    client = pymongo.MongoClient(Config.MONGODB_URI)
    db = client[Config.MONGO_DB_NAME]

    ensure_collections(db, ["usuarios", "centros", "citas"])
    ensure_indexes(db)
    seed_centers(db)
    seed_users(db)

    print(
        "Migración completada. Base de datos '{db}' en '{uri}' lista para usarse.".format(
            db=Config.MONGO_DB_NAME, uri=Config.MONGODB_URI
        )
    )


if __name__ == "__main__":
    main()
