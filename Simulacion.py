import itertools
import math

from models.Cliente import Cliente
from models.Dia import Dia
from models.TipoPizza import TipoPizza
from models.meta.Singleton import Singleton
from utils.utils import Utils


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
    utils = Utils()
    volver_al_terminar_todos_los_pedidos = False

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
        camionetas = self.ordenar_camionetas_por_ubicacion(cliente.ubicacion, 'get_ubicacion')

        for camioneta in camionetas:
            if camioneta.tiene_tipo(tipo):
                return camioneta

        return None

    def ordenar_camionetas_por_ubicacion(self, ubicacion, method_name):

        distancias = {}

        for camioneta in self.dia_actual.camionetas:
            metodo = getattr(camioneta, method_name)
            ubicacion_camioneta = metodo()
            distancia = self.obtener_distancia(ubicacion, ubicacion_camioneta)
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

    def get_tipos_disponibles_en_camionetas(self):
        pizzas_disponibles = list(itertools.chain(*map(lambda x: x.get_pizzas_disponibles(), self.dia_actual.camionetas)))
        return list(set(map(lambda x: x.tipo, pizzas_disponibles)))

    def obtener_camioneta_a_volver_al_restaurante(self):
        if self.volver_al_terminar_todos_los_pedidos:
            return self.obtener_camioneta_mas_proxima_a_liberarse()

        return self.obtener_camioneta_mas_cercana_al_restaurante()

    def obtener_camioneta_mas_proxima_a_liberarse(self):
        # TODO: la camioneta debe calcular cuanto va a tardar en liberarse
        return self.ordenar_camionetas_por_ubicacion([0, 0], 'cuanto_tardas_en_linerarte')[0]

    def obtener_camioneta_mas_cercana_al_restaurante(self):
        return self.ordenar_camionetas_por_ubicacion([0, 0], 'get_ubicacion_siguiente_pedido')[0]
