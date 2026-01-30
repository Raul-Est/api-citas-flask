# 🏥 API de Clínica Médica (Flask + MongoDB)

API profesional para la gestión de usuarios, centros de salud y citas médicas. Implementada con **Flask**, **JWT** para autenticación y **MongoDB** como base de datos, todo orquestado con **Docker** y **Nginx**.

---

## 🚀 Inicio Rápido con Docker (Producción)

La forma más sencilla y recomendada de ejecutar este proyecto es utilizando Docker. Todo el stack (API, MongoDB y Nginx) se configura automáticamente.

1. **Clonar el repositorio:**
   ```bash
   git clone <link-repo>
   cd api-citas-flask
   ```

2. **Levantar el proyecto:**
   ```bash
   docker-compose up --build
   ```

3. **Acceder a la API:**
   - **Documentación Swagger:** [http://localhost:5001/apidocs/](http://localhost:5001/apidocs/)
   - La API está detrás de Nginx en el puerto **5001**.
   - Los datos iniciales (admin y centros) se cargan automáticamente al iniciar.

---

## 🛠️ Ejecución Local (Desarrollo)

Si prefieres ejecutarlo sin Docker:

### Requisitos
- Python 3.10+
- MongoDB local en el puerto 27017

### Pasos
1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configurar variables (Opcional):**
   Crea un archivo `.env` o exporta las variables:
   ```bash
   export MONGODB_URI="mongodb://localhost:27017/"
   export MONGO_DB_NAME="Clinica"
   ```
3. **Ejecutar migración inicial:**
   ```bash
   python migrations/001_init_clinica.py
   ```
4. **Iniciar servidor:**
   ```bash
   python application.py
   ```

---

## 🔐 Autenticación y Swagger

La API utiliza JWT. Para probar los endpoints protegidos en Swagger:

1. Registra un usuario en `POST /register`.
2. Inicia sesión en `POST /login` para obtener el `access_token`.
3. Haz clic en el botón **"Authorize"** (arriba a la derecha).
4. Introduce: `Bearer <tu_token>` (incluyendo la palabra "Bearer").
5. ¡Ya puedes probar todos los endpoints!

---

## 🏗️ Arquitectura del Proyecto

- **`application.py`**: Punto de entrada de la aplicación Flask.
- **`config.py`**: Gestión centralizada de configuración y secretos.
- **`migrations/`**: Scripts de inicialización de base de datos e índices.
- **`nginx.conf`**: Configuración del proxy inverso.
- **`Dockerfile` / `docker-compose.yml`**: Infraestructura como código para despliegues.

---

## 📝 Características Principales
- ✅ Autenticación Robusta con JWT.
- ✅ Inicialización automática de Base de Datos.
- ✅ Documentación interactiva con Swagger UI v3.
- ✅ Proxy Inverso con Nginx para mejor rendimiento y seguridad.
- ✅ Configuración flexible mediante variables de entorno.
