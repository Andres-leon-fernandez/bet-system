class Cuota:
    def __init__(
        self,
        mercado,
        valor_local: float,
        valor_empate: float,
        valor_visitante: float,
    ):
        self.mercado = mercado
        self.valor_local = valor_local
        self.valor_empate = valor_empate
        self.valor_visitante = valor_visitante

    def obtener_valor(self, seleccion: str) -> float:
        valores = {
            "local": self.valor_local,
            "empate": self.valor_empate,
            "visitante": self.valor_visitante,
        }
        if seleccion not in valores:
            raise ValueError(f"Selección inválida: {seleccion}")
        return valores[seleccion]

    def __repr__(self) -> str:
        return (
            f"Cuota({self.mercado.nombre}: "
            f"L={self.valor_local} E={self.valor_empate} V={self.valor_visitante})"
        )
