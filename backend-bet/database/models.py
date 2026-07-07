from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    saldo = Column(Float, default=1000.0)

    apuestas = relationship("ApuestaDB", back_populates="usuario")


class EquipoDB(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    continente = Column(String(50))
    ranking_fifa = Column(Integer, default=0)
    valor_mercado = Column(Float, default=0.0)

    partidos_local = relationship("PartidoDB", foreign_keys="PartidoDB.equipo_local_id", back_populates="local")
    partidos_visitante = relationship("PartidoDB", foreign_keys="PartidoDB.equipo_visitante_id", back_populates="visitante")


class PartidoDB(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equipo_local_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    equipo_visitante_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    fecha = Column(String(20))
    estado = Column(String(20), default="pendiente")
    goles_local = Column(Integer, nullable=True)
    goles_visitante = Column(Integer, nullable=True)

    local = relationship("EquipoDB", foreign_keys=[equipo_local_id], back_populates="partidos_local")
    visitante = relationship("EquipoDB", foreign_keys=[equipo_visitante_id], back_populates="partidos_visitante")
    apuestas = relationship("ApuestaDB", back_populates="partido")


class ApuestaDB(Base):
    __tablename__ = "apuestas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    partido_id = Column(Integer, ForeignKey("partidos.id"), nullable=False)
    seleccion = Column(String(20), nullable=False)
    cuota = Column(Float, nullable=False)
    monto = Column(Float, nullable=False)
    estado = Column(String(20), default="pendiente")
    ganancia_potencial = Column(Float, nullable=True)
    ganancia_real = Column(Float, nullable=True)

    usuario = relationship("UsuarioDB", back_populates="apuestas")
    partido = relationship("PartidoDB", back_populates="apuestas")
