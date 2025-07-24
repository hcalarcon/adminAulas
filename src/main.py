from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.modules.usuarios import user_router
from src.modules.aula import aulas_router
from src.modules.clase import clases_router
from src.modules.asistencia import asistencias_router
from src.modules.epetcoins import epetcoins_router
from src.modules.grupos import grupos_router
from src.modules.nota import notas_router
from src.modules.tarea import tarea_router
from src.modules.evaluacion import router as evaluacion_router
from src.security.middleware import decode_token_from_request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import ALL_METHODS


from src.core.limiter import limiter


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# rate limit
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# origenes permitidos
origins = [
    # También es común usar localhost como 127.0.0.1
    "https://admin-aulas-web.vercel.app",  # Si tienes versión desplegada en la web
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite los orígenes configurados
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=[
        "x-api-key",  # ← agregalo explícitamente
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "User-Agent",
        "X-Requested-With",
    ],  # Permite todos los headers
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
        or request.url.path == "/users/refresh"
    ):
        return await call_next(request)

    # Para otras rutas, requerir token
    try:
        user = await decode_token_from_request(request)
        request.state.user = user
    except HTTPException as e:
        origin = request.headers.get("origin", "*")
        return JSONResponse(
            status_code=401,
            content={"detail": e.detail},
            headers={
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Headers": "Authorization, Content-Type",
                "Access-Control-Allow-Methods": ", ".join(ALL_METHODS),
            },
        )

    response = await call_next(request)
    return response


app.include_router(user_router.router, prefix="/users", tags=["Usuarios"])
app.include_router(aulas_router.router, prefix="/aulas", tags=["Aulas"])
app.include_router(clases_router.router, prefix="/clases", tags=["Clases"])
app.include_router(
    asistencias_router.router, prefix="/asistencias", tags=["Asistencias"]
)
app.include_router(epetcoins_router.router, prefix="/epetcoins", tags=["Epetcoins"])
app.include_router(grupos_router.router, prefix="/grupos", tags=["Grupos"])
app.include_router(tarea_router.router, prefix="/tareas", tags=["Tareas"])
app.include_router(notas_router.router, prefix="/notas", tags=["Notas"])
app.include_router(evaluacion_router.router, prefix="/evaluacion", tags=["Evaluacion"])
