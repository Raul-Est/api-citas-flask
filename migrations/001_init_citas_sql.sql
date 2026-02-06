create database if not exists citas;

use citas;

--- Tabla de Centros ---
CREATE TABLE centros (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL
);

--- Tabla de Usuarios ---
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Para el hash de bcrypt
    name VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(20),
    birth_date DATE
);

--- Tabla de Citas ---
CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    centro_id INTEGER REFERENCES centros(id) ON DELETE CASCADE,
    day DATE NOT NULL,
    hour TIME NOT NULL,
    
    CONSTRAINT unique_date_per_center UNIQUE (day, hour, centro_id)
);