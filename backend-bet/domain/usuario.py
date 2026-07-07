class Usuario:
    def __init__(self, nombre: str, email: str, saldo: float = 1000.0):
        self.nombre = nombre
        self.email = email
        self.saldo = saldo
        self.historial_apuestas: list = []

    def tiene_saldo_suficiente(self, monto: float) -> bool:
        return self.saldo >= monto

    def descontar_saldo(self, monto: float) -> None:
        if not self.tiene_saldo_suficiente(monto):
            raise ValueError(f"Saldo insuficiente: {self.saldo} < {monto}")
        self.saldo -= monto

    def abonar_ganancia(self, monto: float) -> None:
        self.saldo += monto

    def registrar_apuesta(self, apuesta) -> None:
        self.historial_apuestas.append(apuesta)

    def __repr__(self) -> str:
        return f"Usuario({self.nombre}, saldo={self.saldo:.2f})"
