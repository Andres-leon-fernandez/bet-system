import pandas as pd
from analytics.prediccion import cargar_modelo, predecir_probabilidades
from analytics.cuotas import fuerza_a_probabilidad, generar_cuotas_1x2
from analytics.simulacion import simular_n_partidos


class PrediccionService:
    def __init__(self):
        self._modelo_cargado = False
        try:
            self.modelo, self.scaler, self.features = cargar_modelo()
            self._modelo_cargado = True
        except FileNotFoundError:
            self._modelo_cargado = False

    def predecir_partido(self, df_equipos: pd.DataFrame) -> list[dict]:
        if not self._modelo_cargado:
            raise RuntimeError("Modelo no entrenado. Ejecuta analytics/prediccion.py primero")
        return predecir_probabilidades(df_equipos).to_dict(orient="records")

    def generar_cuotas_para_partido(self, fuerza_local: float, fuerza_visitante: float) -> dict:
        prob_local, prob_empate, prob_visitante = fuerza_a_probabilidad(fuerza_local, fuerza_visitante)
        cuotas = generar_cuotas_1x2(prob_local, prob_empate, prob_visitante)
        return {"probabilidades": {"local": prob_local, "empate": prob_empate, "visitante": prob_visitante}, "cuotas": cuotas}

    def simular_partido(self, fuerza_local: float, fuerza_visitante: float, n: int = 1000) -> dict:
        return simular_n_partidos(fuerza_local, fuerza_visitante, n).to_dict(orient="records")
