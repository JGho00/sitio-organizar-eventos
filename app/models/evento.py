class Evento:
    id:int
    nombre:str
    descripcion:str
    lugar:str
    dia:int
    mes:int
    año:int
    
    def __init__(self,nombre:str,descripcion:str,lugar:str,dia:int,mes:int,año:int):
        self.nombre = nombre,
        self.descripcion = descripcion
        self.lugar= lugar
        self.dia = dia
        self.mes = mes
        self.año = año

e1 = Evento('Evento 1',"50 personas","Loisc",2,6,2026)
e2 = Evento('Evento 2',"50 personas","Lepark",2,8,2026)
e3 = Evento('Evento 3',"30 personas","Margaritas",3,1,2026)
e4 = Evento('Evento 4',"50 personas","Paseo Cultural",15,7,2026)

eventos = [e1,e2,e3,e4]