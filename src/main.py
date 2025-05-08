from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.api.routers import userRouter
from src.api.routers import aulasRouter
from src.security.middleware import get_current_user

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
        user_id = await get_current_user(request)
        request.state.user_id = user_id
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    response = await call_next(request)
    return response


app.include_router(userRouter.router, prefix="/users", tags=["Usuarios"])
app.include_router(aulasRouter.router, prefix="/aulas", tags=["Aulas"])
