from database import get_session
from database.models import ApuestaDB, UsuarioDB, PartidoDB


class ReporteService:
    def __init__(self):
        self.session = get_session()

    def resumen_apuestas(self) -> dict:
        total = self.session.query(ApuestaDB).count()
        ganadas = self.session.query(ApuestaDB).filter(ApuestaDB.estado == "ganada").count()
        perdidas = self.session.query(ApuestaDB).filter(ApuestaDB.estado == "perdida").count()
        pendientes = self.session.query(ApuestaDB).filter(ApuestaDB.estado == "pendiente").count()
        total_monto = sum(a[0] for a in self.session.query(ApuestaDB.monto).all() if a[0])
        return {"total_apuestas": total, "ganadas": ganadas, "perdidas": perdidas, "pendientes": pendientes, "total_apostado": round(total_monto, 2)}

    def top_apostadores(self, limite: int = 5) -> list[dict]:
        return [
            {"nombre": r.nombre, "email": r.email, "saldo": r.saldo}
            for r in self.session.query(UsuarioDB.nombre, UsuarioDB.email, UsuarioDB.saldo).order_by(UsuarioDB.saldo.desc()).limit(limite).all()
        ]

    def estadisticas_partidos(self) -> dict:
        total = self.session.query(PartidoDB).count()
        finalizados = self.session.query(PartidoDB).filter(PartidoDB.estado == "finalizado").count()
        pendientes = self.session.query(PartidoDB).filter(PartidoDB.estado == "pendiente").count()
        return {"total_partidos": total, "finalizados": finalizados, "pendientes": pendientes}

    def cerrar(self):
        self.session.close()
