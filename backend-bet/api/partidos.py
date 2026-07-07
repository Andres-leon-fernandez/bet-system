from fastapi import APIRouter, HTTPException
from services import PartidoService

router = APIRouter(prefix="/partidos", tags=["Partidos"])


@router.post("/")
def crear_partido(equipo_local: str, equipo_visitante: str, fecha: str):
    service = PartidoService()
    try:
        partido = service.crear_partido(equipo_local, equipo_visitante, fecha)
        return partido
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        service.cerrar()


@router.get("/{partido_id}")
def obtener_partido(partido_id: int):
    service = PartidoService()
    partido = service.obtener_partido(partido_id)
    service.cerrar()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido


@router.get("/")
def listar_partidos():
    service = PartidoService()
    partidos = service.listar_partidos()
    service.cerrar()
    return partidos


@router.put("/{partido_id}/finalizar")
def finalizar_partido(partido_id: int, goles_local: int, goles_visitante: int):
    service = PartidoService()
    partido = service.finalizar_partido(partido_id, goles_local, goles_visitante)
    service.cerrar()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido
