from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.api.routers import user_router
from src.api.routers import aulas_router
from src.api.routers import clases_router
from src.api.routers import asistencias_router
from src.security.middleware import decode_token_from_request

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
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
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    response = await call_next(request)
    return response


app.include_router(user_router.router, prefix="/users", tags=["Usuarios"])
app.include_router(aulas_router.router, prefix="/aulas", tags=["Aulas"])
app.include_router(clases_router.router, prefix="/clases", tags=["Clases"])
app.include_router(
    asistencias_router.router, prefix="/asistencias", tags=["Asistencias"]
)
