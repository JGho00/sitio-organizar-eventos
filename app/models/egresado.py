
class Persona:
    dni:int
    nombre:str
    edad:int
    nacionalidad:str

    def __init__(self,dni:int,nombre:str,edad:int,nacionalidad:str):
        self.dni = dni
        self.nombre = nombre
        self.edad = edad
        self.nacionalidad = nacionalidad
        
class Egresado(Persona):
    direccion: str
    telefono: str
    escuela_id: int

    def __init__(self, dni: int, nombre: str, edad:int,nacionalidad:str,direccion: str, telefono: str, escuela_id: int):
        super().__init__(dni,nombre,edad,nacionalidad)
        self.direccion = direccion
        self.telefono = telefono
        self.escuela_id = escuela_id


e1 = Egresado(1, "Juan Pérez",23,"Argentina","Calle Falsa 123", "123456789", 1)
e2 = Egresado(2, "María Gómez",34,"Argentina","Avenida Siempre Viva 456", "987654321", 2)
e3 = Egresado(3, "Carlos Rodríguez",55,"Argentina","Boulevard de los Sueños Rotos 789", "555555555", 3)
e4 = Egresado(4, "Ana Martínez",66,"Argentina","Calle de la Tecnología 321", "111222333", 4)

egresados = [e1, e2, e3, e4]