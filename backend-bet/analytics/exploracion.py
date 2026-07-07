import pandas as pd
import numpy as np

RUTA_DATASET = "datasets/worldcup.csv"


def cargar_datos(ruta: str = RUTA_DATASET) -> pd.DataFrame:
    return pd.read_csv(ruta)


def exploracion_basica(df: pd.DataFrame) -> dict:
    return {
        "shape": df.shape,
        "columnas": list(df.columns),
        "tipos": {c: str(df[c].dtype) for c in df.columns},
        "nulos_por_columna": df.isnull().sum().to_dict(),
        "porcentaje_nulos": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        "filas_duplicadas": df.duplicated().sum(),
    }


def resumen_estadistico(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include="all").transpose()


def contar_equipos_unicos(df: pd.DataFrame) -> int:
    return df["team"].nunique()


def contar_continentes(df: pd.DataFrame) -> pd.Series:
    return df["continent"].value_counts()


def ediciones_mundial(df: pd.DataFrame) -> list:
    return sorted(df["version"].unique().tolist())


def equipos_por_edicion(df: pd.DataFrame) -> pd.Series:
    return df.groupby("version")["team"].count()


def ganadores_por_edicion(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["winner"] == 1][["version", "team", "continent"]]


def resumen_columnas_categoricas(df: pd.DataFrame) -> dict:
    categoricas = df.select_dtypes(include=["object"]).columns
    return {c: df[c].value_counts().to_dict() for c in categoricas}


if __name__ == "__main__":
    df = cargar_datos()
    print("=== EXPLORACION INICIAL ===")
    info = exploracion_basica(df)
    print(f"Dimensiones: {info['shape']}")
    print(f"Columnas ({len(info['columnas'])}): {info['columnas']}")
    print(f"\nNulos por columna:\n{pd.Series(info['nulos_por_columna'])}")
    print(f"\nFilas duplicadas: {info['filas_duplicadas']}")
    print(f"\nEquipos únicos: {contar_equipos_unicos(df)}")
    print(f"\nContinentes:\n{contar_continentes(df)}")
    print(f"\nEdiciones: {ediciones_mundial(df)}")
    print(f"\nEquipos por edición:\n{equipos_por_edicion(df)}")
    print(f"\nGanadores por edición:\n{ganadores_por_edicion(df)}")
