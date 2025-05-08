# AulasAdmin 🎓📚

Sistema de gestión de aulas y clases para instituciones educativas. Desarrollado con **FastAPI**, **SQLAlchemy**, **PostgreSQL** y **Alembic**.

## 🚀 Características

- Autenticación con JWT.
- CRUD de usuarios (alumnos y profesores).
- Creación y gestión de aulas.
- Registro y consulta de clases por aula.
- Asistencia por clase (alumnos presentes o ausentes).
- Roles de usuario: alumno, profesor (y próximamente, administrador).
- Middleware para obtener el usuario autenticado.
- Migraciones con Alembic.

## 🧱 Tecnologías

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT (auth)
- Uvicorn

## 🗂️ Estructura de carpetas

src/
├── api/
│ ├── routes/ # Endpoints de la API
│ ├── deps.py # Dependencias comunes (como get_db)
├── auth/ # Autenticación y seguridad
│ ├── auth.py
│ ├── security.py
│ └── middleware.py
├── config/
│ ├── database.py
│ └── settings.py
├── controllers/ # Lógica de negocio (opcional)
├── crud/ # Operaciones con la base de datos
├── models/ # Modelos SQLAlchemy
├── schemas/ # Esquemas Pydantic
├── utils/ # Utilidades generales
├── main.py # Punto de entrada de la app

bash
Copiar
Editar

## ⚙️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/aulasadmin.git
cd aulasadmin
Crea y activa un entorno virtual:

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
Instala dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Configura las variables de entorno en un archivo .env:

ini
Copiar
Editar
DATABASE_URL=postgresql://user:password@localhost:5432/aulasdb
SECRET_KEY=clave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
Ejecuta las migraciones:

bash
Copiar
Editar
alembic upgrade head
Inicia el servidor:

bash
Copiar
Editar
uvicorn src.main:app --reload
📬 Endpoints principales
POST /auth/login: Login y obtención del token.

GET /users/me: Obtener usuario autenticado.

POST /aulas: Crear un aula.

PUT /aulas/{id} o /aulas/me: Editar un aula (según permisos).

POST /clases: Registrar una clase en un aula.

POST /asistencias: Registrar asistencia a una clase.

🛡️ Pendiente por implementar
Panel de administración.

Roles más específicos (admin).

Filtros avanzados y paginación.

Documentación Swagger personalizada.

🧑‍💻 Autor
Proyecto creado por Hernaldo para su curso de Construcción de Software.
```
