from models.Dia import Dia
from models.meta.Singleton import Singleton


def generar_camionetas():
    from models.Camioneta import Camioneta
    return [Camioneta(), Camioneta(), Camioneta(), Camioneta()]


class Simulacion(metaclass=Singleton):
    experimentos = 10
    dias_a_simular = 365
    horas_por_dia = 12
    minutos_maximo = 60 * horas_por_dia
    dias_corridos = []
    camionetas = generar_camionetas()
    events = []
    dia_actual = Dia(minutos_maximo, camionetas)

    def correr_simulacion(self):
        # Correr simulacion
        for experimento in range(self.experimentos):
            # por cada dia, generar un nuevo objeto dia y correrlo
            for dia in range(self.dias_a_simular):
                self.dia_actual.correr()
                self.dias_corridos.append(self.dia_actual)
                self.dia_actual = Dia(self.minutos_maximo, self.camionetas)

    def obtener_datos(self):
        # Obtener datos finales
        # retorna datos en np array o como sea
        pass

    def add_event(self, event):
        self.dia_actual.fel.append(event)

    def get_hora(self):
        return self.dia_actual.get_tiempo_actual()

    def get_camioneta_by_pizza(self, pizza):
        camionetas = list(filter(lambda x: x.get_pizza(pizza) is not None, self.dia_actual.camionetas))
        return None if len(camionetas) == 0 else camionetas[0]

    def get_fel(self):
        return self.dia_actual.get_fel()
