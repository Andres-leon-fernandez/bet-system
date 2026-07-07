from domain.apuesta import Apuesta, EstadoApuesta
from .reglas import puede_apostar, calcular_ganancia, resolver_apuesta
from .validaciones import validar_apuesta, ErrorValidacion


def procesar_apuesta(usuario, partido, seleccion: str, cuota_valor: float, monto: float) -> Apuesta:
    validar_apuesta(usuario, partido, monto, cuota_valor, seleccion)

    if not puede_apostar(usuario, monto):
        raise ErrorValidacion(
            f"Saldo insuficiente: {usuario.saldo} < {monto}"
        )

    apuesta = Apuesta(
        usuario=usuario,
        partido=partido,
        seleccion=seleccion,
        cuota=cuota_valor,
        monto=monto,
    )

    usuario.descontar_saldo(monto)
    usuario.registrar_apuesta(apuesta)

    return apuesta


def resolver_apuestas_partido(partido, apuestas: list[Apuesta]) -> list[Apuesta]:
    if not partido.es_finalizado():
        raise ErrorValidacion("El partido aún no ha finalizado")

    resultado = partido.resultado()
    if resultado is None:
        raise ErrorValidacion("No se puede determinar el resultado del partido")

    resueltas = []
    for apuesta in apuestas:
        if apuesta.estado != EstadoApuesta.PENDIENTE:
            continue
        resolver_apuesta(apuesta, resultado)
        if apuesta.es_ganada():
            ganancia = calcular_ganancia(apuesta.monto, apuesta.cuota)
            apuesta.usuario.abonar_ganancia(ganancia)
        resueltas.append(apuesta)

    return resueltas


def cancelar_apuesta(apuesta: Apuesta) -> None:
    if apuesta.estado != EstadoApuesta.PENDIENTE:
        raise ErrorValidacion(
            f"Solo se pueden cancelar apuestas pendientes (estado: {apuesta.estado.value})"
        )
    apuesta.cancelar()
    apuesta.usuario.abonar_ganancia(apuesta.monto)
