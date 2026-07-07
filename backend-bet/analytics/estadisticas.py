import pandas as pd
import numpy as np

RUTA_DATASET = "datasets/worldcup.csv"


def cargar_datos(ruta: str = RUTA_DATASET) -> pd.DataFrame:
    return pd.read_csv(ruta)


def top_equipos_goles_anotados(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("team")["goals_scored_last_4y"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )


def promedio_goles_por_edicion(df: pd.DataFrame) -> pd.Series:
    return df.groupby("version")["goals_scored_last_4y"].mean()


def ranking_fifa_promedio(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("team")["fifa_rank_pre_tournament"]
        .mean()
        .sort_values()
        .head(20)
        .reset_index()
    )


def equipos_mas_ganadores(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["winner"] == 1][["version", "team", "continent"]]


def continente_dominante(df: pd.DataFrame) -> pd.Series:
    ganadores = df[df["winner"] == 1]
    return ganadores["continent"].value_counts()


def mejor_promedio_victorias(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("team")["wins_last_4y"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )


def resumen_por_continente(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("continent").agg({
        "goals_scored_last_4y": "mean",
        "goals_received_last_4y": "mean",
        "wins_last_4y": "mean",
        "fifa_rank_pre_tournament": "mean",
        "winner": "sum",
        "semi_finalist": "sum",
    }).round(2)


def correlaciones(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = df.select_dtypes(include=[np.number]).columns
    return df[num_cols].corr()


def equipos_mas_participaciones(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("team")["world_cup_participations_before"]
        .max()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )


if __name__ == "__main__":
    df = cargar_datos()
    print("=== TOP 10 EQUIPOS CON MÁS GOLES ANOTADOS (histórico) ===")
    print(top_equipos_goles_anotados(df))
    print("\n=== PROMEDIO DE GOLES POR EDICIÓN ===")
    print(promedio_goles_por_edicion(df))
    print("\n=== TOP 20 RANKING FIFA PROMEDIO ===")
    print(ranking_fifa_promedio(df))
    print("\n=== GANADORES POR EDICIÓN ===")
    print(equipos_mas_ganadores(df))
    print("\n=== CONTINENTE DOMINANTE (títulos) ===")
    print(continente_dominante(df))
    print("\n=== MEJOR PROMEDIO DE VICTORIAS ===")
    print(mejor_promedio_victorias(df))
    print("\n=== RESUMEN POR CONTINENTE ===")
    print(resumen_por_continente(df))
