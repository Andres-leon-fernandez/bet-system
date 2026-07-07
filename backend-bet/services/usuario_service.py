from database import UsuarioRepository, get_session
from domain import Usuario


class UsuarioService:
    def __init__(self):
        self.session = get_session()
        self.repo = UsuarioRepository(self.session)

    def crear_usuario(self, nombre: str, email: str, saldo: float = 1000.0) -> dict:
        existente = self.repo.obtener_por_email(email)
        if existente:
            raise ValueError(f"Ya existe un usuario con email {email}")
        usuario_db = self.repo.crear(nombre, email, saldo)
        return {
            "id": usuario_db.id,
            "nombre": usuario_db.nombre,
            "email": usuario_db.email,
            "saldo": usuario_db.saldo,
        }

    def obtener_usuario(self, usuario_id: int) -> dict | None:
        usuario_db = self.repo.obtener_por_id(usuario_id)
        if not usuario_db:
            return None
        return {
            "id": usuario_db.id,
            "nombre": usuario_db.nombre,
            "email": usuario_db.email,
            "saldo": usuario_db.saldo,
        }

    def listar_usuarios(self) -> list[dict]:
        return [
            {"id": u.id, "nombre": u.nombre, "email": u.email, "saldo": u.saldo}
            for u in self.repo.listar()
        ]

    def obtener_dominio(self, usuario_id: int) -> Usuario | None:
        usuario_db = self.repo.obtener_por_id(usuario_id)
        if not usuario_db:
            return None
        return Usuario(nombre=usuario_db.nombre, email=usuario_db.email, saldo=usuario_db.saldo)

    def cerrar(self):
        self.session.close()
