

class Escuela:
    id: int
    nombre: str
    ciudad: str
    direccion: str
    telefono: str

    def __init__(self, id: int, nombre: str, ciudad: str, direccion: str, telefono: str):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.direccion = direccion
        self.telefono = telefono

e1 = Escuela(1, "Colegio Nacional", "La Rioja", "Calle Falsa 123", "123456789")
e2 = Escuela(2, "Escuela Comercial", "Chilecito", "Avenida Siempre Viva 456", "987654321")
e3 = Escuela(3, "Escuela Provincial", "La Rioja", "Boulevard de los Sueños Rotos 789", "555555555")
e4 = Escuela(4, "Escuela Técnica", "La Rioja", "Calle de la Tecnología 321", "111222333")

escuelas = [e1, e2, e3, e4]