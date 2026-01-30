import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "misuperclavedeldestinofinal")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "misuperclavedeldestinofinal")
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://mongodb:27017/")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "Clinica")
