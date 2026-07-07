from fastapi import APIRouter, HTTPException
from services import ApuestaService
from logic.validaciones import ErrorValidacion

router = APIRouter(prefix="/apuestas", tags=["Apuestas"])


@router.post("/")
def realizar_apuesta(usuario_id: int, partido_id: int, seleccion: str, cuota: float, monto: float):
    service = ApuestaService()
    try:
        apuesta = service.realizar_apuesta(usuario_id, partido_id, seleccion, cuota, monto)
        return apuesta
    except (ValueError, ErrorValidacion) as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        service.cerrar()


@router.post("/{apuesta_id}/cancelar")
def cancelar_apuesta(apuesta_id: int):
    service = ApuestaService()
    try:
        resultado = service.cancelar_apuesta(apuesta_id)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        service.cerrar()


@router.get("/usuario/{usuario_id}")
def historial_usuario(usuario_id: int):
    service = ApuestaService()
    historial = service.historial_usuario(usuario_id)
    service.cerrar()
    return historial
