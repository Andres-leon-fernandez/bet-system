from fastapi import APIRouter
from services import ReporteService

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/apuestas")
def resumen_apuestas():
    service = ReporteService()
    resumen = service.resumen_apuestas()
    service.cerrar()
    return resumen


@router.get("/top-apostadores")
def top_apostadores(limite: int = 5):
    service = ReporteService()
    top = service.top_apostadores(limite)
    service.cerrar()
    return top


@router.get("/partidos")
def estadisticas_partidos():
    service = ReporteService()
    stats = service.estadisticas_partidos()
    service.cerrar()
    return stats
