class Equipo:
    def __init__(
        self,
        nombre: str,
        continente: str,
        ranking_fifa: int = 0,
        valor_mercado: float = 0.0,
    ):
        self.nombre = nombre
        self.continente = continente
        self.ranking_fifa = ranking_fifa
        self.valor_mercado = valor_mercado

    def __repr__(self) -> str:
        return f"Equipo({self.nombre}, rank={self.ranking_fifa})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Equipo):
            return False
        return self.nombre == other.nombre
