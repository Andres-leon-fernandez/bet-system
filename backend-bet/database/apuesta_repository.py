from sqlalchemy.orm import Session
from .models import ApuestaDB


class ApuestaRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(
        self,
        usuario_id: int,
        partido_id: int,
        seleccion: str,
        cuota: float,
        monto: float,
        ganancia_potencial: float,
    ) -> ApuestaDB:
        apuesta = ApuestaDB(
            usuario_id=usuario_id,
            partido_id=partido_id,
            seleccion=seleccion,
            cuota=cuota,
            monto=monto,
            estado="pendiente",
            ganancia_potencial=ganancia_potencial,
        )
        self.session.add(apuesta)
        self.session.commit()
        self.session.refresh(apuesta)
        return apuesta

    def obtener_por_id(self, apuesta_id: int) -> ApuestaDB | None:
        return self.session.query(ApuestaDB).filter(ApuestaDB.id == apuesta_id).first()

    def listar_por_usuario(self, usuario_id: int) -> list[ApuestaDB]:
        return self.session.query(ApuestaDB).filter(ApuestaDB.usuario_id == usuario_id).all()

    def listar_por_partido(self, partido_id: int) -> list[ApuestaDB]:
        return self.session.query(ApuestaDB).filter(ApuestaDB.partido_id == partido_id).all()

    def listar_pendientes_por_partido(self, partido_id: int) -> list[ApuestaDB]:
        return (
            self.session.query(ApuestaDB)
            .filter(ApuestaDB.partido_id == partido_id, ApuestaDB.estado == "pendiente")
            .all()
        )

    def actualizar_estado(self, apuesta_id: int, estado: str, ganancia_real: float | None = None) -> ApuestaDB | None:
        apuesta = self.obtener_por_id(apuesta_id)
        if apuesta:
            apuesta.estado = estado
            if ganancia_real is not None:
                apuesta.ganancia_real = ganancia_real
            self.session.commit()
            self.session.refresh(apuesta)
        return apuesta

    def listar_todas(self) -> list[ApuestaDB]:
        return self.session.query(ApuestaDB).all()
