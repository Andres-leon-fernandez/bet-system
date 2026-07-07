from database import PartidoRepository, EquipoRepository, get_session
from domain import Equipo, Partido


class PartidoService:
    def __init__(self):
        self.session = get_session()
        self.repo = PartidoRepository(self.session)
        self.equipo_repo = EquipoRepository(self.session)

    def crear_partido(self, equipo_local_nombre: str, equipo_visitante_nombre: str, fecha: str) -> dict:
        local_db = self.equipo_repo.obtener_por_nombre(equipo_local_nombre)
        visitante_db = self.equipo_repo.obtener_por_nombre(equipo_visitante_nombre)
        if not local_db or not visitante_db:
            raise ValueError("Ambos equipos deben existir en la BD")
        partido_db = self.repo.crear(local_db.id, visitante_db.id, fecha)
        return {
            "id": partido_db.id,
            "equipo_local": local_db.nombre,
            "equipo_visitante": visitante_db.nombre,
            "fecha": partido_db.fecha,
            "estado": partido_db.estado,
        }

    def finalizar_partido(self, partido_id: int, goles_local: int, goles_visitante: int) -> dict | None:
        partido_db = self.repo.actualizar_resultado(partido_id, goles_local, goles_visitante)
        if not partido_db:
            return None
        return {
            "id": partido_db.id,
            "equipo_local": partido_db.local.nombre,
            "equipo_visitante": partido_db.visitante.nombre,
            "goles_local": partido_db.goles_local,
            "goles_visitante": partido_db.goles_visitante,
            "estado": partido_db.estado,
        }

    def obtener_partido(self, partido_id: int) -> dict | None:
        partido_db = self.repo.obtener_por_id(partido_id)
        if not partido_db:
            return None
        return {
            "id": partido_db.id,
            "equipo_local": partido_db.local.nombre,
            "equipo_visitante": partido_db.visitante.nombre,
            "fecha": partido_db.fecha,
            "estado": partido_db.estado,
            "goles_local": partido_db.goles_local,
            "goles_visitante": partido_db.goles_visitante,
        }

    def obtener_dominio(self, partido_id: int):
        partido_db = self.repo.obtener_por_id(partido_id)
        if not partido_db:
            return None
        local = Equipo(partido_db.local.nombre, partido_db.local.continente)
        visitante = Equipo(partido_db.visitante.nombre, partido_db.visitante.continente)
        partido = Partido(local, visitante, partido_db.fecha)
        if partido_db.estado == "finalizado" and partido_db.goles_local is not None:
            partido.finalizar(partido_db.goles_local, partido_db.goles_visitante)
        return partido

    def listar_partidos(self) -> list[dict]:
        return [
            {
                "id": p.id,
                "equipo_local": p.local.nombre,
                "equipo_visitante": p.visitante.nombre,
                "fecha": p.fecha,
                "estado": p.estado,
            }
            for p in self.repo.listar()
        ]

    def cerrar(self):
        self.session.close()
