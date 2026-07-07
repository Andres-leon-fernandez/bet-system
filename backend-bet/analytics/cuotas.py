import numpy as np
import pandas as pd

MARGEN_OVERROUND = 0.05


def probabilidad_a_cuota(probabilidad: float, overround: float = MARGEN_OVERROUND) -> float:
    if probabilidad <= 0 or probabilidad >= 1:
        raise ValueError(f"Probabilidad debe estar entre 0 y 1 (exclusive): {probabilidad}")
    return round(1 / (probabilidad * (1 - overround)), 2)


def generar_cuotas_1x2(
    prob_local: float, prob_empate: float, prob_visitante: float
) -> dict:
    total = prob_local + prob_empate + prob_visitante
    if not np.isclose(total, 1.0, atol=0.01):
        raise ValueError(f"Las probabilidades deben sumar 1 (suman {total})")

    cuota_local = probabilidad_a_cuota(prob_local)
    cuota_empate = probabilidad_a_cuota(prob_empate)
    cuota_visitante = probabilidad_a_cuota(prob_visitante)

    return {
        "local": cuota_local,
        "empate": cuota_empate,
        "visitante": cuota_visitante,
    }


def fuerza_a_probabilidad(
    fuerza_local: float, fuerza_visitante: float, empate_base: float = 0.25
) -> tuple:
    total = fuerza_local + fuerza_visitante
    if total == 0:
        return (1 / 3, 1 / 3, 1 / 3)

    prob_local = fuerza_local / total * (1 - empate_base)
    prob_visitante = fuerza_visitante / total * (1 - empate_base)
    prob_empate = empate_base

    suma = prob_local + prob_empate + prob_visitante
    prob_local /= suma
    prob_empate /= suma
    prob_visitante /= suma

    return (round(prob_local, 4), round(prob_empate, 4), round(prob_visitante, 4))


def generar_cuotas_desde_fuerza(fuerza_local: float, fuerza_visitante: float) -> dict:
    probs = fuerza_a_probabilidad(fuerza_local, fuerza_visitante)
    return {
        "probabilidades": {
            "local": probs[0],
            "empate": probs[1],
            "visitante": probs[2],
        },
        "cuotas": generar_cuotas_1x2(*probs),
    }


if __name__ == "__main__":
    print("=== GENERACIÓN DE CUOTAS ===")

    probs = (0.55, 0.25, 0.20)
    print(f"\nProbabilidades: local={probs[0]}, empate={probs[1]}, visitante={probs[2]}")
    cuotas = generar_cuotas_1x2(*probs)
    print(f"Cuotas: {cuotas}")

    print("\n--- Cuotas desde fuerza ---")
    resultado = generar_cuotas_desde_fuerza(70, 30)
    print(f"Fuerza local=70, visitante=30")
    print(f"Probabilidades: {resultado['probabilidades']}")
    print(f"Cuotas: {resultado['cuotas']}")

    resultado2 = generar_cuotas_desde_fuerza(50, 50)
    print(f"\nFuerza local=50, visitante=50")
    print(f"Probabilidades: {resultado2['probabilidades']}")
    print(f"Cuotas: {resultado2['cuotas']}")
