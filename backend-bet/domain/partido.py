from enum import Enum


class EstadoPartido(Enum):
    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"


class Partido:
    def __init__(self, equipo_local, equipo_visitante, fecha: str):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.fecha = fecha
        self.estado = EstadoPartido.PENDIENTE
        self.goles_local: int | None = None
        self.goles_visitante: int | None = None
        self.cuotas: list = []

    def iniciar(self) -> None:
        self.estado = EstadoPartido.EN_CURSO

    def finalizar(self, goles_local: int, goles_visitante: int) -> None:
        self.goles_local = goles_local
        self.goles_visitante = goles_visitante
        self.estado = EstadoPartido.FINALIZADO

    def es_finalizado(self) -> bool:
        return self.estado == EstadoPartido.FINALIZADO

    def resultado(self) -> str | None:
        if not self.es_finalizado():
            return None
        if self.goles_local > self.goles_visitante:
            return "local"
        elif self.goles_visitante > self.goles_local:
            return "visitante"
        return "empate"

    def agregar_cuota(self, cuota) -> None:
        self.cuotas.append(cuota)

    def __repr__(self) -> str:
        return f"Partido({self.equipo_local.nombre} vs {self.equipo_visitante.nombre}, {self.estado.value})"
