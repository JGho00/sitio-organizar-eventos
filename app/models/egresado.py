egresados = [
    {"id": 1, "nombre": "Juan Pérez", "escuela": "Colegio Nacional"},
    {"id": 2, "nombre": "María Gómez", "escuela":"Escuela Comercial"},
    {"id": 3, "nombre": "Carlos Rodríguez", "escuela": "Escuela Provincial"},
    {"id": 4, "nombre": "Ana Martínez", "escuela": "Colegio Nacional"}
]

class Egresado:
    dni: int
    nombre: str
    direccion: str
    telefono: str
    escuela_id: int

    def __init__(self, dni: int, nombre: str, direccion: str, telefono: str, escuela_id: int):
        self.dni = dni
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.escuela_id = escuela_id


e1 = Egresado(1, "Juan Pérez", "Calle Falsa 123", "123456789", 1)
e2 = Egresado(2, "María Gómez", "Avenida Siempre Viva 456", "987654321", 2)
e3 = Egresado(3, "Carlos Rodríguez", "Boulevard de los Sueños Rotos 789", "555555555", 3)
e4 = Egresado(4, "Ana Martínez", "Calle de la Tecnología 321", "111222333", 4)
egresados = [e1, e2, e3, e4]