# AdminAulas

AdminAulas es una plataforma web diseñada para facilitar la gestión integral de aulas, tanto para profesores como para alumnos. Ofrece funcionalidades como asistencia, incentivos con moneda virtual (epetcoins), historial de participación y visualización personalizada según el rol del usuario.

## 🚀 Características principales

- **Toma de asistencia:** Registro de presente, ausente o tarde.
- **Cálculo de porcentaje de asistencia:** Visualización clara por colores.
- **Sistema de incentivos:** Los profesores pueden activar una moneda virtual personalizada (epetcoin) y asignarla a sus alumnos.
- **Gestión por tipo de aula:**
  - _Aulas teóricas:_ Toda la clase cursa junta.
  - _Aulas taller:_ Los alumnos se dividen en grupos con diferentes días de cursada.
- **Historial de asistencia y epetcoins:** Por materia y por alumno.
- **Autenticación:** Basada en JWT.
- **Tematización:** Utilizando React Native Paper.

## 👥 Roles

### Profesores

- Visualizan todas las aulas donde dictan clases.
- Pueden tomar asistencia según la modalidad del aula (general o por grupo).
- Activan una epetcoin personalizada para asignar a sus estudiantes.
- Visualizan el historial de asignaciones de monedas y asistencia.

### Alumnos

- Visualizan las materias en las que están inscriptos.
- Consultan su porcentaje de asistencia (con tarjetas que cambian de color).
- Revisan detalle por clase: presente, ausente, tarde o sin clase aún.
- Consultan el historial de asignación de epetcoins.

## 🧱 Tecnologías

| Parte         | Tecnología                              |
| ------------- | --------------------------------------- |
| Frontend      | React Native (orientado a Web) + Vercel |
| Backend       | FastAPI + Render                        |
| Base de datos | PostgreSQL + Supabase                   |
| Autenticación | JWT                                     |
| UI            | React Native Paper                      |

---

¡Con AdminAulas, la gestión de clases es más simple, visual y motivadora para toda la comunidad educativa!

Desarrollado con **FastAPI**, **SQLAlchemy**, **PostgreSQL** y **Alembic**.

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
