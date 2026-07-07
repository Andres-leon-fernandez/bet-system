from sqlalchemy.orm import Session
from .models import EquipoDB


class EquipoRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, nombre: str, continente: str, ranking_fifa: int = 0, valor_mercado: float = 0.0) -> EquipoDB:
        equipo = EquipoDB(
            nombre=nombre,
            continente=continente,
            ranking_fifa=ranking_fifa,
            valor_mercado=valor_mercado,
        )
        self.session.add(equipo)
        self.session.commit()
        self.session.refresh(equipo)
        return equipo

    def obtener_por_id(self, equipo_id: int) -> EquipoDB | None:
        return self.session.query(EquipoDB).filter(EquipoDB.id == equipo_id).first()

    def obtener_por_nombre(self, nombre: str) -> EquipoDB | None:
        return self.session.query(EquipoDB).filter(EquipoDB.nombre == nombre).first()

    def listar(self) -> list[EquipoDB]:
        return self.session.query(EquipoDB).all()

    def actualizar_ranking(self, equipo_id: int, ranking: int) -> EquipoDB | None:
        equipo = self.obtener_por_id(equipo_id)
        if equipo:
            equipo.ranking_fifa = ranking
            self.session.commit()
            self.session.refresh(equipo)
        return equipo
