from sqlalchemy.orm import Session
from .models import UsuarioDB


class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, nombre: str, email: str, saldo: float = 1000.0) -> UsuarioDB:
        usuario = UsuarioDB(nombre=nombre, email=email, saldo=saldo)
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def obtener_por_id(self, usuario_id: int) -> UsuarioDB | None:
        return self.session.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()

    def obtener_por_email(self, email: str) -> UsuarioDB | None:
        return self.session.query(UsuarioDB).filter(UsuarioDB.email == email).first()

    def listar(self) -> list[UsuarioDB]:
        return self.session.query(UsuarioDB).all()

    def actualizar_saldo(self, usuario_id: int, nuevo_saldo: float) -> UsuarioDB | None:
        usuario = self.obtener_por_id(usuario_id)
        if usuario:
            usuario.saldo = nuevo_saldo
            self.session.commit()
            self.session.refresh(usuario)
        return usuario

    def eliminar(self, usuario_id: int) -> bool:
        usuario = self.obtener_por_id(usuario_id)
        if usuario:
            self.session.delete(usuario)
            self.session.commit()
            return True
        return False
