bet-system/

│
├── app.py                 ← inicia FastAPI
│
├── api/
│   ├── usuarios.py
│   ├── apuestas.py
│   ├── partidos.py
│   ├── reportes.py
│   └── predicciones.py
│
├── domain/
│   ├── usuario.py
│   ├── equipo.py
│   ├── partido.py
│   ├── apuesta.py
│   ├── mercado.py
│   ├── cuota.py
│   └── casa_apuestas.py
│
├── services/
│   ├── apuesta_service.py
│   ├── partido_service.py
│   ├── usuario_service.py
│   ├── reporte_service.py
│   └── prediccion_service.py
│
├── logic/
│   ├── reglas.py
│   ├── motor.py
│   └── validaciones.py
│
├── analytics/
│   ├── limpieza.py
│   ├── estadisticas.py
│   ├── cuotas.py
│   ├── prediccion.py
│   └── simulacion.py
│
├── database/
│   ├── conexion.py
│   ├── usuario_repository.py
│   ├── apuesta_repository.py
│   ├── partido_repository.py
│   └── equipo_repository.py
│
├── models/
│   ├── modelo.pkl
│   └── scaler.pkl
│
├── datasets/
│   └── worldcup.csv
│
├── tests/
│
└── requirements.txt
