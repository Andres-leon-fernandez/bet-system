class Mercado:
    def __init__(self, nombre: str, descripcion: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self) -> str:
        return f"Mercado({self.nombre})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Mercado):
            return False
        return self.nombre == other.nombre
