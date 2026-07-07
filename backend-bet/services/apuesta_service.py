from database import ApuestaRepository, get_session
from logic.validaciones import ErrorValidacion
from services.usuario_service import UsuarioService
from services.partido_service import PartidoService


class ApuestaService:
    def __init__(self):
        self.session = get_session()
        self.repo = ApuestaRepository(self.session)
        self.usuario_service = UsuarioService()
        self.partido_service = PartidoService()

    def realizar_apuesta(self, usuario_id: int, partido_id: int, seleccion: str, cuota_valor: float, monto: float) -> dict:
        usuario = self.usuario_service.obtener_dominio(usuario_id)
        partido = self.partido_service.obtener_dominio(partido_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        if not partido:
            raise ValueError("Partido no encontrado")

        if not usuario.tiene_saldo_suficiente(monto):
            raise ErrorValidacion(f"Saldo insuficiente: {usuario.saldo} < {monto}")
        if partido.estado.value != "pendiente":
            raise ErrorValidacion(f"No se puede apostar: el partido está {partido.estado.value}")

        ganancia_potencial = round(monto * cuota_valor, 2)
        apuesta_db = self.repo.crear(usuario_id, partido_id, seleccion, cuota_valor, monto, ganancia_potencial)
        usuario.descontar_saldo(monto)
        self.usuario_service.repo.actualizar_saldo(usuario_id, usuario.saldo)

        return {
            "id": apuesta_db.id,
            "usuario_id": usuario_id,
            "partido_id": partido_id,
            "seleccion": seleccion,
            "cuota": cuota_valor,
            "monto": monto,
            "ganancia_potencial": ganancia_potencial,
            "estado": "pendiente",
        }

    def resolver_apuestas_partido(self, partido_id: int) -> list[dict]:
        partido_db = self.partido_service.repo.obtener_por_id(partido_id)
        if not partido_db:
            raise ValueError("Partido no encontrado")
        if partido_db.estado != "finalizado":
            raise ValueError("El partido aún no ha finalizado")

        if partido_db.goles_local > partido_db.goles_visitante:
            resultado = "local"
        elif partido_db.goles_visitante > partido_db.goles_local:
            resultado = "visitante"
        else:
            resultado = "empate"

        apuestas_db = self.repo.listar_pendientes_por_partido(partido_id)
        resultados = []

        for a_db in apuestas_db:
            if a_db.seleccion == resultado:
                ganancia = round(a_db.monto * a_db.cuota, 2)
                self.repo.actualizar_estado(a_db.id, "ganada", ganancia)
                usuario_db = self.usuario_service.repo.obtener_por_id(a_db.usuario_id)
                if usuario_db:
                    self.usuario_service.repo.actualizar_saldo(a_db.usuario_id, usuario_db.saldo + ganancia)
                resultados.append({"id": a_db.id, "usuario_id": a_db.usuario_id, "resultado": "ganada", "ganancia": ganancia})
            else:
                self.repo.actualizar_estado(a_db.id, "perdida")
                resultados.append({"id": a_db.id, "usuario_id": a_db.usuario_id, "resultado": "perdida", "ganancia": 0})

        return resultados

    def cancelar_apuesta(self, apuesta_id: int) -> dict:
        apuesta_db = self.repo.obtener_por_id(apuesta_id)
        if not apuesta_db:
            raise ValueError("Apuesta no encontrada")
        if apuesta_db.estado != "pendiente":
            raise ValueError(f"No se puede cancelar: la apuesta está {apuesta_db.estado}")

        self.repo.actualizar_estado(apuesta_id, "cancelada")
        usuario_db = self.usuario_service.repo.obtener_por_id(apuesta_db.usuario_id)
        if usuario_db:
            self.usuario_service.repo.actualizar_saldo(apuesta_db.usuario_id, usuario_db.saldo + apuesta_db.monto)
        return {"id": apuesta_db.id, "estado": "cancelada", "reembolso": apuesta_db.monto}

    def historial_usuario(self, usuario_id: int) -> list[dict]:
        return [
            {
                "id": a.id,
                "partido_id": a.partido_id,
                "seleccion": a.seleccion,
                "cuota": a.cuota,
                "monto": a.monto,
                "estado": a.estado,
                "ganancia_potencial": a.ganancia_potencial,
                "ganancia_real": a.ganancia_real,
            }
            for a in self.repo.listar_por_usuario(usuario_id)
        ]

    def cerrar(self):
        self.session.close()
        self.usuario_service.cerrar()
        self.partido_service.cerrar()
