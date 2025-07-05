from pydantic import BaseModel
from typing import Optional, Literal


class ConfiguracionUsuarioBase(BaseModel):
    tipo_evaluacion: Literal["inversa", "tradicional"] = "inversa"
    dark_mode: bool = False
    color_primario: Optional[str] = "#E814F0"
    foto_perfil_url: Optional[str] = None


class ConfiguracionUsuarioCreate(ConfiguracionUsuarioBase):
    pass


class ConfiguracionUsuarioOut(ConfiguracionUsuarioBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
