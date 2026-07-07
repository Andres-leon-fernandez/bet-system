from .reglas import (
    es_cuota_valida,
    esta_dentro_limites,
    monto_minimo,
    monto_maximo,
)
from domain.partido import EstadoPartido
from domain.apuesta import EstadoApuesta


class ErrorValidacion(ValueError):
    pass


def validar_monto(monto: float) -> None:
    if monto <= 0:
        raise ErrorValidacion("El monto debe ser positivo")
    if not esta_dentro_limites(monto):
        raise ErrorValidacion(
            f"El monto debe estar entre {monto_minimo()} y {monto_maximo()}"
        )


def validar_usuario(usuario) -> None:
    if usuario is None:
        raise ErrorValidacion("El usuario no existe")


def validar_partido(partido) -> None:
    if partido is None:
        raise ErrorValidacion("El partido no existe")
    if partido.estado != EstadoPartido.PENDIENTE:
        raise ErrorValidacion(
            f"No se puede apostar: el partido está {partido.estado.value}"
        )


def validar_seleccion(seleccion: str, cuota) -> None:
    valores_validos = {"local", "empate", "visitante"}
    if seleccion not in valores_validos:
        raise ErrorValidacion(
            f"Selección inválida: {seleccion}. Debe ser: local, empate o visitante"
        )


def validar_cuota(cuota_valor: float) -> None:
    if not es_cuota_valida(cuota_valor):
        raise ErrorValidacion(
            f"Cuota inválida: {cuota_valor}. Debe estar entre 1.01 y 1000.0"
        )


def validar_apuesta(usuario, partido, monto: float, cuota_valor: float, seleccion: str) -> None:
    errores = []
    try:
        validar_usuario(usuario)
    except ErrorValidacion as e:
        errores.append(str(e))

    try:
        validar_partido(partido)
    except ErrorValidacion as e:
        errores.append(str(e))

    try:
        validar_monto(monto)
    except ErrorValidacion as e:
        errores.append(str(e))

    try:
        validar_cuota(cuota_valor)
    except ErrorValidacion as e:
        errores.append(str(e))

    try:
        validar_seleccion(seleccion, cuota_valor)
    except ErrorValidacion as e:
        errores.append(str(e))

    if errores:
        raise ErrorValidacion("; ".join(errores))
