from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.api.routers import user_router
from src.api.routers import aulas_router
from src.api.routers import clases_router
from src.api.routers import asistencias_router
from src.api.routers import alarcoins_router
from src.security.middleware import decode_token_from_request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

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
    "http://localhost",  # Para pruebas en navegador (ajustar si usas otro puerto)
    "http://localhost:3000",
    "http://localhost:8082",  # Si usas React en este puerto
    "http://127.0.0.1",  # También es común usar localhost como 127.0.0.1
    "https://tu-aplicacion.web.app",  # Si tienes versión desplegada en la web
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

    # if request.method == "OPTIONS":
    #     return JSONResponse(
    #         status_code=200,
    #         content={"message": "Preflight passed"},
    #         headers={
    #             "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
    #             "Access-Control-Allow-Headers": "Authorization, Content-Type",
    #             "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    #             "Access-Control-Allow-Credentials": "true",
    #         },
    #     )

    if request.method == "OPTIONS":
        return await call_next(request)

    if (
        request.url.path == "/users/login"
        or (request.url.path == "/users/" and request.method == "POST")
        or request.url.path == "/docs"
        or request.url.path == "/openapi.json"
    ):
        return await call_next(request)

    api_key = request.headers.get("x-api-key")
    if api_key != settings.API_KEY:
        return JSONResponse(
            status_code=403, content={"detail": "API Key inválida o ausente"}
        )

    # Para otras rutas, requerir token
    try:
        user = await decode_token_from_request(request)
        request.state.user = user
    except HTTPException as e:
        return JSONResponse(status_code=401, content={"detail": e.detail})

    response = await call_next(request)
    return response


app.include_router(user_router.router, prefix="/users", tags=["Usuarios"])
app.include_router(aulas_router.router, prefix="/aulas", tags=["Aulas"])
app.include_router(clases_router.router, prefix="/clases", tags=["Clases"])
app.include_router(
    asistencias_router.router, prefix="/asistencias", tags=["Asistencias"]
)
app.include_router(alarcoins_router.router, prefix="/alarcoins", tags=["Alarcoins"])
