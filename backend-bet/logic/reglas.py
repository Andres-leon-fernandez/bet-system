MONTO_MINIMO = 1.0
MONTO_MAXIMO = 10_000.0
CUOTA_MINIMA = 1.01
CUOTA_MAXIMA = 1000.0


def puede_apostar(usuario, monto: float) -> bool:
    return usuario.tiene_saldo_suficiente(monto)


def calcular_ganancia(monto: float, cuota: float) -> float:
    return round(monto * cuota, 2)


def resolver_apuesta(apuesta, resultado_partido: str):
    apuesta.resolver(resultado_partido)


def es_cuota_valida(cuota: float) -> bool:
    return CUOTA_MINIMA <= cuota <= CUOTA_MAXIMA


def monto_minimo() -> float:
    return MONTO_MINIMO


def monto_maximo() -> float:
    return MONTO_MAXIMO


def esta_dentro_limites(monto: float) -> bool:
    return MONTO_MINIMO <= monto <= MONTO_MAXIMO
