from fastapi import APIRouter, HTTPException
from services import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/")
def crear_usuario(nombre: str, email: str, saldo: float = 1000.0):
    service = UsuarioService()
    try:
        usuario = service.crear_usuario(nombre, email, saldo)
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        service.cerrar()


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    service = UsuarioService()
    usuario = service.obtener_usuario(usuario_id)
    service.cerrar()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.get("/")
def listar_usuarios():
    service = UsuarioService()
    usuarios = service.listar_usuarios()
    service.cerrar()
    return usuarios
