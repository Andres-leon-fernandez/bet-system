from fastapi import APIRouter, HTTPException
from services import PrediccionService

router = APIRouter(prefix="/predicciones", tags=["Predicciones"])


@router.post("/cuotas")
def generar_cuotas(fuerza_local: float, fuerza_visitante: float):
    service = PrediccionService()
    try:
        resultado = service.generar_cuotas_para_partido(fuerza_local, fuerza_visitante)
        return resultado
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/simular")
def simular_partido(fuerza_local: float, fuerza_visitante: float, n: int = 1000):
    service = PrediccionService()
    resultado = service.simular_partido(fuerza_local, fuerza_visitante, n)
    return resultado
