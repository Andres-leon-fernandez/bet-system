from enum import Enum


class EstadoApuesta(Enum):
    PENDIENTE = "pendiente"
    GANADA = "ganada"
    PERDIDA = "perdida"
    CANCELADA = "cancelada"


class Apuesta:
    def __init__(
        self,
        usuario,
        partido,
        seleccion: str,
        cuota: float,
        monto: float,
    ):
        self.usuario = usuario
        self.partido = partido
        self.seleccion = seleccion
        self.cuota = cuota
        self.monto = monto
        self.estado = EstadoApuesta.PENDIENTE
        self.ganancia_potencial = round(monto * cuota, 2)

    def calcular_ganancia(self) -> float:
        return round(self.monto * self.cuota, 2)

    def resolver(self, resultado_partido: str) -> None:
        if self.seleccion == resultado_partido:
            self.estado = EstadoApuesta.GANADA
        else:
            self.estado = EstadoApuesta.PERDIDA

    def cancelar(self) -> None:
        self.estado = EstadoApuesta.CANCELADA

    def es_ganada(self) -> bool:
        return self.estado == EstadoApuesta.GANADA

    def __repr__(self) -> str:
        return (
            f"Apuesta({self.usuario.nombre} → {self.seleccion} "
            f"@ {self.cuota}, ${self.monto}, {self.estado.value})"
        )
