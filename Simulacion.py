import itertools
import math
from datetime import timedelta, datetime

from events.PizzaVenceEvent import PizzaVenceEvent
from models.Cliente import Cliente
from models.Dia import Dia
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.meta.Singleton import Singleton
from utils.utils import Utils


def generar_camionetas():
    from models.Camioneta import Camioneta
    return [Camioneta(), Camioneta(), Camioneta(), Camioneta()]


class Reloj(object):

    def __init__(self):
        self.dia = None

    def iniciar_dia(self):
        self.dia = datetime.now()

    def avanzar(self, minutos):
        self.dia = self.dia + timedelta(minutes=minutos)

class Simulacion(metaclass=Singleton):

    def __init__(self):

        self.reloj = Reloj()
        self.experimentos = 10
        self.dias_a_simular = 365
        self.horas_por_dia = 12
        self.minutos_maximo = 60 * self.horas_por_dia
        self.dias_corridos = []
        self.camionetas = generar_camionetas()
        self.events = []
        self.dia_actual = Dia(self.minutos_maximo, self.camionetas)
        self.utils = Utils()
        self.volver_al_terminar_todos_los_pedidos = False
        self.pedidos = []
        self.clientes_rechazados = []
        self.rango_de_atencion = 2000

    def run(self):
        for experimento in range(self.experimentos):
            for dia in range(self.dias_a_simular):
                self.dia_actual.iniciar_dia()
                self.dia_actual.correr()
                self.clientes_rechazados += self.dia_actual.pedidos_rechazados
                self.dias_corridos.append(self.dia_actual)
                self.dia_actual = Dia(self.minutos_maximo, self.camionetas)

    def obtener_datos(self):
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
        pizzas_disponibles = list(
            itertools.chain(*map(lambda x: x.get_pizzas_disponibles(), self.dia_actual.camionetas)))
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

    def remover_evento_vencimiento_pizza(self, pizza: Pizza):
        evento = self.get_pizza_vence_by_pizza(pizza)
        if evento is not None:
            self.dia_actual.fel.remove(evento)

    def get_pizza_vence_by_pizza(self, pizza):
        eventos = list(filter(lambda x: isinstance(x, PizzaVenceEvent) and x.pizza == pizza, self.dia_actual.fel))
        return None if len(eventos) == 0 else eventos[0]

    def add_pedido(self, pedido):
        self.pedidos.append(pedido)

    def cliente_esta_en_rango(self, cliente: Cliente):
        return self.obtener_distancia([0, 0], cliente.ubicacion) <= self.rango_de_atencion

    def avanzar_reloj(self, minutos):
        self.reloj.avanzar(minutos)

    @property
    def dia(self):
        return self.reloj.dia

    def iniciar_dia(self):
        self.reloj.iniciar_dia()


