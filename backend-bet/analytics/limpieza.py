import pandas as pd
import numpy as np

RUTA_DATASET = "datasets/worldcup.csv"


def cargar_datos(ruta: str = RUTA_DATASET) -> pd.DataFrame:
    return pd.read_csv(ruta)


def diagnosticar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    nulos = pd.DataFrame({
        "columna": df.columns,
        "nulos": df.isnull().sum().values,
        "porcentaje": (df.isnull().sum() / len(df) * 100).values,
    })
    return nulos[nulos["nulos"] > 0].sort_values("nulos", ascending=False)


def imputar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    return df


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def normalizar_nombres_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def convertir_tipos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "version" in df.columns:
        df["version"] = df["version"].astype(int)
    if "is_host" in df.columns:
        df["is_host"] = df["is_host"].astype(int)
    return df


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = eliminar_duplicados(df)
    df = convertir_tipos(df)
    df = imputar_nulos(df)
    return df


if __name__ == "__main__":
    df = cargar_datos()
    print("=== DIAGNÓSTICO DE NULOS ===")
    nulos = diagnosticar_nulos(df)
    print(nulos if not nulos.empty else "Sin nulos detectados")
    print(f"\nShape original: {df.shape}")
    df_limpio = limpiar(df)
    print(f"Shape después de limpieza: {df_limpio.shape}")
    print(f"Nulos después de imputar: {df_limpio.isnull().sum().sum()}")
