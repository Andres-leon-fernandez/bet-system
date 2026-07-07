from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.usuarios import router as usuarios_router
from api.partidos import router as partidos_router
from api.apuestas import router as apuestas_router
from api.predicciones import router as predicciones_router
from api.reportes import router as reportes_router

app = FastAPI(title="Bet System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router)
app.include_router(partidos_router)
app.include_router(apuestas_router)
app.include_router(predicciones_router)
app.include_router(reportes_router)


@app.get("/")
def root():
    return {"message": "Bet System API - Simulación de apuestas deportivas"}
