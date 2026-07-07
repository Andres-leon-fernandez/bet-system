import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

RUTA_DATASET = "datasets/worldcup.csv"
RUTA_MODELO = "models/modelo.pkl"
RUTA_SCALER = "models/scaler.pkl"
RUTA_FEATURES = "models/features.pkl"

FEATURES = [
    "goals_scored_last_4y",
    "goals_received_last_4y",
    "wins_last_4y",
    "losses_last_4y",
    "draws_last_4y",
    "world_cup_titles_before",
    "squad_total_market_value_eur",
    "fifa_rank_pre_tournament",
    "fifa_points_pre_tournament",
    "squad_avg_age",
    "world_cup_participations_before",
    "groups_passed_before",
    "round16_before",
    "quarterfinals_before",
    "semifinals_before",
    "finals_before",
    "is_host",
]

TARGET = "semi_finalist"


def cargar_datos(ruta: str = RUTA_DATASET) -> pd.DataFrame:
    df = pd.read_csv(ruta)
    df = df.dropna(subset=FEATURES)
    return df


def preparar_datos(df: pd.DataFrame):
    X = df[FEATURES].copy()
    y = df[TARGET].copy()
    return X, y


def entrenar(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    modelo = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        random_state=random_state,
        class_weight="balanced",
    )
    modelo.fit(X_train_scaled, y_train)

    y_pred = modelo.predict(X_test_scaled)
    precision = accuracy_score(y_test, y_pred)

    return modelo, scaler, {
        "precision": round(precision, 4),
        "report": classification_report(y_test, y_pred, output_dict=True),
        "matriz_confusion": confusion_matrix(y_test, y_pred).tolist(),
    }


def guardar_modelo(modelo, scaler, features: list[str]):
    os.makedirs("models", exist_ok=True)
    joblib.dump(modelo, RUTA_MODELO)
    joblib.dump(scaler, RUTA_SCALER)
    joblib.dump(features, RUTA_FEATURES)


def cargar_modelo():
    if not os.path.exists(RUTA_MODELO):
        raise FileNotFoundError("Modelo no encontrado. Ejecuta entrenar() primero.")
    modelo = joblib.load(RUTA_MODELO)
    scaler = joblib.load(RUTA_SCALER)
    features = joblib.load(RUTA_FEATURES)
    return modelo, scaler, features


def predecir_probabilidades(df_equipos: pd.DataFrame) -> pd.DataFrame:
    modelo, scaler, features = cargar_modelo()
    X = df_equipos[features].copy()
    X_scaled = scaler.transform(X)
    probs = modelo.predict_proba(X_scaled)[:, 1]
    resultado = df_equipos[["team", "version"]].copy()
    resultado["probabilidad_semi_final"] = probs.round(4)
    return resultado.sort_values("probabilidad_semi_final", ascending=False)


if __name__ == "__main__":
    print("=== ENTRENANDO MODELO ===")
    df = cargar_datos()
    print(f"Datos cargados: {df.shape}")
    X, y = preparar_datos(df)
    print(f"Features: {X.shape[1]}, Muestras: {X.shape[0]}")
    print(f"Distribución target (semi_finalist):\n{y.value_counts().to_dict()}")

    modelo, scaler, metricas = entrenar(X, y)
    guardar_modelo(modelo, scaler, FEATURES)

    print(f"\nPrecisión del modelo: {metricas['precision']}")
    print(f"\nMatriz de confusión:\n{metricas['matriz_confusion']}")
    print(f"\nModelo guardado en {RUTA_MODELO}")
