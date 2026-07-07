import numpy as np
import pandas as pd


def simular_goles_poisson(lambda_goles: float) -> int:
    return np.random.poisson(lambda_goles)


def simular_partido(
    fuerza_local: float, fuerza_visitante: float
) -> dict:
    goles_local = simular_goles_poisson(fuerza_local)
    goles_visitante = simular_goles_poisson(fuerza_visitante)

    if goles_local > goles_visitante:
        resultado = "local"
    elif goles_visitante > goles_local:
        resultado = "visitante"
    else:
        resultado = "empate"

    return {
        "goles_local": goles_local,
        "goles_visitante": goles_visitante,
        "resultado": resultado,
    }


def simular_n_partidos(
    fuerza_local: float, fuerza_visitante: float, n: int = 1000
) -> pd.DataFrame:
    resultados = []
    for _ in range(n):
        resultados.append(simular_partido(fuerza_local, fuerza_visitante))

    df = pd.DataFrame(resultados)
    frecuencias = df["resultado"].value_counts(normalize=True).round(4)
    return pd.DataFrame({
        "resultado": frecuencias.index,
        "frecuencia": frecuencias.values,
        "simulaciones": n,
    })


def ajustar_fuerza_por_ventaja_local(fuerza: float, ventaja: float = 0.3) -> float:
    return fuerza + ventaja


if __name__ == "__main__":
    np.random.seed(42)

    print("=== SIMULACIÓN DE PARTIDOS ===")
    print("Método: Distribución Poisson")

    fuerza_local = 1.8
    fuerza_visitante = 1.2

    print(f"\nPartido individual (fuerza local={fuerza_local}, visitante={fuerza_visitante}):")
    for i in range(5):
        resultado = simular_partido(fuerza_local, fuerza_visitante)
        print(f"  Sim {i+1}: {resultado['goles_local']}-{resultado['goles_visitante']} ({resultado['resultado']})")

    print(f"\nSimulación de 10,000 partidos:")
    resumen = simular_n_partidos(fuerza_local, fuerza_visitante, 10000)
    print(resumen)

    print("\n--- Con ventaja local ---")
    fl = ajustar_fuerza_por_ventaja_local(1.5)
    fv = 1.2
    resumen2 = simular_n_partidos(fl, fv, 10000)
    print(f"Fuerza local={fl}, visitante={fv}")
    print(resumen2)
