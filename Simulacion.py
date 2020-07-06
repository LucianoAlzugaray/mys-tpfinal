import itertools
import math
from datetime import time, datetime

from events.LlamoClienteEvent import LlamoClienteEvent
from events.PizzaVenceEvent import PizzaVenceEvent
from models.Cliente import Cliente
from models.Dia import Dia
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.actividades.EncolarCliente import EncolarCliente
from models.actividades.RechazarPedido import RechazarPedido
from models.meta.Singleton import Singleton
from utils.utils import Utils
from models.Reloj import Reloj

def generar_camionetas():
    from models.Camioneta import Camioneta
    return [Camioneta(), Camioneta(), Camioneta(), Camioneta()]


class Simulacion(metaclass=Singleton):

    CANTIDAD_HORAS_LABORALES = 12
    CANTIDAD_MINUTOS_LABORALES = CANTIDAD_HORAS_LABORALES * 60
    HORA_DE_CIERRE = 23
    MINUTOS_DE_CIERRE = 0
    HORA_FIN_TOMA_DE_PEDIDOS = 22
    MINUTOS_FIN_TOMA_DE_PEDIDOS = 30

    DIA_INICIO = 5
    MES_INICIO = 7
    ANIO_INICIO = 2020
    HORA_INICIO = 11
    MINUTOS_INICIO = 0
    TIEMPO_INICIO = datetime(
        ANIO_INICIO,
        MES_INICIO,
        DIA_INICIO,
        HORA_INICIO,
        MINUTOS_INICIO
    )

    DIA_FIN = 5
    MES_FIN = 7
    ANIO_FIN = 2020
    HORA_FIN = 11
    MINUTOS_FIN = 0
    TIEMPO_FIN = datetime(
        ANIO_FIN,
        MES_FIN,
        DIA_FIN,
        HORA_FIN,
        MINUTOS_FIN
    )



    def __init__(self):
        self.reloj = Reloj()
        self.experimentos = 10
        self.dias_a_simular = 365
        self.horas_por_dia = 12
        self.minutos_maximo = 60 * self.horas_por_dia
        self.dias_corridos = []
        self.camionetas = generar_camionetas()
        self.events = []
        self.utils = Utils()
        self.volver_al_terminar_todos_los_pedidos = False
        self.pedidos = []
        self.clientes_rechazados = []
        self.rango_de_atencion = 2000
        self.fel = []
        self.pedidos_rechazados_en_llamada = []

    def run(self):
        for experimento in range(self.experimentos):
            for dia in range(self.dias_a_simular):
                self.iniciar_dia()
                while not self.termino_dia():
                    for evento in self.obtener_eventos_de_ahora():
                        evento.notify()
                    self.avanzar_reloj(1)

                for camioneta in self.camionetas:
                    camioneta.volver_a_pizzeria()

                self.clientes_rechazados += self.pedidos_rechazados
                self.dias_corridos.append(self.dia_actual)
                # TODO preguntar que poner
                # self.dia_actual = Dia(self.minutos_maximo, self.camionetas)

    def obtener_datos(self):
        pass

    def add_event(self, event):
        self.fel.append(event)

    @property
    def time(self):
        return self.reloj.dia

    def get_camioneta_by_pizza(self, pizza):
        camionetas = list(filter(lambda x: x.get_pizza(pizza) is not None, self.camionetas))
        return None if len(camionetas) == 0 else camionetas[0]

    def rechazar_pedido(self, cliente: Cliente) -> None:
        self.pedidos_rechazados_en_llamada.append(cliente)


    def get_camioneta_by_cliente(self, cliente: Cliente):
        camionetas = list(filter(lambda x: x.get_pedido_by_cliente(cliente) is not None, self.camionetas))
        return None if len(camionetas) == 0 else camionetas[0]

    def seleccionar_camioneta(self, cliente: Cliente, tipo: TipoPizza):
        camionetas = self.ordenar_camionetas_por_ubicacion(cliente.ubicacion, 'get_ubicacion')

        for camioneta in camionetas:
            if camioneta.tiene_tipo(tipo):
                return camioneta

        return None

    def ordenar_camionetas_por_ubicacion(self, ubicacion, method_name):

        distancias = {}

        for camioneta in self.camionetas:
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
            itertools.chain(*map(lambda x: x.get_pizzas_disponibles(), self.camionetas)))
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
            self.fel.remove(evento)

    def get_pizza_vence_by_pizza(self, pizza):
        eventos = list(filter(lambda x: isinstance(x, PizzaVenceEvent) and x.pizza == pizza, self.fel))
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
        self.generar_pedidos()
        self.inicializar_camionetas()

    def generar_pedidos(self):
        for hora_de_pedido in self.utils.get_horas_de_pedidos(self.horas_por_dia):
            # si hora de pedido es un time solamente tengo que agarrar el date de la simulacion y concatenarle el time
            # hora = datetime(self.dia_actual.year, self.dia_actual.month, self.dia_actual.day, hora_de_pedido.hour, hora_de_pedido.minute)
            # evento = LlamoClienteEvent(hora, Cliente())
            evento = LlamoClienteEvent(hora_de_pedido, Cliente())
            evento.attach(EncolarCliente())
            evento.attach(RechazarPedido())
            self.fel.append(evento)

    def inicializar_camionetas(self):
        list(map(lambda camioneta: camioneta.volver_a_pizzeria(), self.camionetas))
        list(map(lambda camioneta: camioneta.cargar_pizzas(), self.camionetas))

    @property
    def tiempo_inicio(self):
        return self.TIEMPO_INICIO

    @property
    def tiempo_fin(self):
        return self.TIEMPO_FIN

    def termino_dia(self):
        return self.reloj.termino_dia()

    def obtener_dt_futuro(self, minutos):
        return self.reloj.obtener_dt_futuro(minutos)

    def obtener_eventos_de_ahora(self):
        return list(filter(lambda x: x.hora == self.time, self.fel))