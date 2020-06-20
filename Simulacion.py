from models.Camioneta import Camioneta


class Simulacion:
    experimentos = 10
    dias_a_simular = 365
    horas_por_dia = 12
    minutos_maximo = 60 * horas_por_dia

    def __init__(self):
        self.camionetas = [Camioneta(), Camioneta(), Camioneta(), Camioneta()]
