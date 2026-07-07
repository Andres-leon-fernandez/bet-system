from sqlalchemy.orm import Session
from .models import PartidoDB


class PartidoRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, equipo_local_id: int, equipo_visitante_id: int, fecha: str) -> PartidoDB:
        partido = PartidoDB(
            equipo_local_id=equipo_local_id,
            equipo_visitante_id=equipo_visitante_id,
            fecha=fecha,
            estado="pendiente",
        )
        self.session.add(partido)
        self.session.commit()
        self.session.refresh(partido)
        return partido

    def obtener_por_id(self, partido_id: int) -> PartidoDB | None:
        return self.session.query(PartidoDB).filter(PartidoDB.id == partido_id).first()

    def listar(self) -> list[PartidoDB]:
        return self.session.query(PartidoDB).all()

    def listar_pendientes(self) -> list[PartidoDB]:
        return self.session.query(PartidoDB).filter(PartidoDB.estado == "pendiente").all()

    def listar_finalizados(self) -> list[PartidoDB]:
        return self.session.query(PartidoDB).filter(PartidoDB.estado == "finalizado").all()

    def actualizar_resultado(self, partido_id: int, goles_local: int, goles_visitante: int) -> PartidoDB | None:
        partido = self.obtener_por_id(partido_id)
        if partido:
            partido.goles_local = goles_local
            partido.goles_visitante = goles_visitante
            partido.estado = "finalizado"
            self.session.commit()
            self.session.refresh(partido)
        return partido

    def eliminar(self, partido_id: int) -> bool:
        partido = self.obtener_por_id(partido_id)
        if partido:
            self.session.delete(partido)
            self.session.commit()
            return True
        return False
