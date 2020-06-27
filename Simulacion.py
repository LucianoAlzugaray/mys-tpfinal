import math

from SimulacionExceptions.NoHayTipoPizzaEnCamionetaException import NoHayTipoPizzaEnCamionetaException
from models.Cliente import Cliente
from models.Dia import Dia
from models.TipoPizza import TipoPizza
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

    @property
    def pedidos_rechazados(self) -> int:
        return self.dia_actual.pedidos_rechazados

    def rechazar_pedido(self, cliente: Cliente) -> None:
        self.dia_actual.rechazar_pedido(cliente)

    def get_camioneta_by_cliente(self, cliente: Cliente):
        camionetas = list(filter(lambda x: x.get_pedido_by_cliente(cliente) is not None, self.dia_actual.camionetas))
        return None if len(camionetas) == 0 else camionetas[0]

    def seleccionar_camioneta(self, cliente: Cliente, tipo: TipoPizza):

        for camioneta in self.ordenar_camionetas_por_ubicacion(cliente.ubicacion):
            if camioneta.tiene_tipo(tipo):
                return camioneta

        raise NoHayTipoPizzaEnCamionetaException(f"No hay pizas del tipo {tipo}")

    def ordenar_camionetas_por_ubicacion(self, ubicacion):

        distancias = {}

        for camioneta in self.dia_actual.camionetas:
            distancia = self.obtener_distancia(ubicacion, camioneta.ubicacion)
            distancias[camioneta] = distancia

        aux = sorted(distancias.items(), key=lambda x: x[1])

        camionetas = []
        for i in aux:
            camionetas.append(i[0])

        return camionetas

    @staticmethod
    def obtener_distancia(punto1, punto2):
        cateto1 = punto2[0] - punto1[0]
        cateto2 = punto2[1] - punto1[1]
        return math.sqrt(math.pow(cateto1, 2) + math.pow(cateto2, 2))





