from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.api.routers import user_router
from src.api.routers import aulas_router
from src.api.routers import clases_router
from src.api.routers import asistencias_router
from src.security.middleware import decode_token_from_request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

origins = [
    "http://localhost",  # Para pruebas en navegador (ajustar si usas otro puerto)
    "http://localhost:8081",  # Si usas React en este puerto
    "http://127.0.0.1",  # También es común usar localhost como 127.0.0.1
    "exp://127.0.0.1:19000",  # Para Expo (React Native)
    "https://tu-aplicacion.web.app",  # Si tienes versión desplegada en la web
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite los orígenes configurados
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):

    if request.method == "OPTIONS":
        return JSONResponse(
            status_code=200,
            content={"message": "Preflight passed"},
            headers={
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Headers": "Authorization, Content-Type",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Credentials": "true",
            },
        )

    if (
        request.url.path == "/users/login"
        or (request.url.path == "/users/" and request.method == "POST")
        or request.url.path == "/docs"
        or request.url.path == "/openapi.json"
    ):
        return await call_next(request)

    # Para otras rutas, requerir token
    try:
        user = await decode_token_from_request(request)
        request.state.user = user
    except HTTPException as e:
        raise e

    response = await call_next(request)
    return response


app.include_router(user_router.router, prefix="/users", tags=["Usuarios"])
app.include_router(aulas_router.router, prefix="/aulas", tags=["Aulas"])
app.include_router(clases_router.router, prefix="/clases", tags=["Clases"])
app.include_router(
    asistencias_router.router, prefix="/asistencias", tags=["Asistencias"]
)
