import itertools
import math
from datetime import datetime

from events.LlamoClienteEvent import LlamoClienteEvent
from events.PizzaVenceEvent import PizzaVenceEvent
from models.Camioneta import Camioneta
from models.Pedido import Pedido
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.actividades.EncolarPedido import EncolarPedido
from models.actividades.RechazarPedido import RechazarPedido
from models.meta.Singleton import Singleton
from utils.utils import Utils
from models.Reloj import Reloj


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

    CANTIDAD_DE_CAMIONETAS = 4
    CANTIDAD_DE_EXPERIMENTOS = 10
    RANGO_DE_ATENCION = 2000

    def __init__(self):
        self.utils = Utils()
        self.reloj = Reloj()
        self.camionetas = [Camioneta() for i in range(self.CANTIDAD_DE_CAMIONETAS)]
        self.experimentos = self.CANTIDAD_DE_EXPERIMENTOS
        self.rango_de_atencion = self.RANGO_DE_ATENCION
        self.events = []
        self.fel = []
        self.pedidos = []
        self.pedidos_rechazados = []
        # TODO: refactorizar
        self.volver_al_terminar_todos_los_pedidos = False

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

                # TODO preguntar que poner
                # self.dia_actual = Dia(self.minutos_maximo, self.camionetas)

    def obtener_datos(self):
        pass

    def add_event(self, event):
        self.fel.append(event)

    def get_camioneta_by_pizza(self, pizza):
        camionetas = list(filter(lambda x: x.get_pizza(pizza) is not None, self.camionetas))
        return None if len(camionetas) == 0 else camionetas[0]

    def rechazar_pedido(self, pedido: Pedido) -> None:
        self.pedidos_rechazados.append(pedido)

    def get_camioneta_by_cliente(self, pedido: Pedido):
        camionetas = list(filter(lambda x: x.get_pedido_by_cliente(pedido) is not None, self.camionetas))
        return None if len(camionetas) == 0 else camionetas[0]

    def seleccionar_camioneta(self, pedido: Pedido, tipo: TipoPizza):
        camionetas = self.ordenar_camionetas_por_ubicacion(pedido.ubicacion, 'get_ubicacion')

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

    def cliente_esta_en_rango(self, pedido : Pedido):
        return self.obtener_distancia([0, 0], pedido.ubicacion) <= self.rango_de_atencion

    def avanzar_reloj(self, minutos):
        self.reloj.avanzar(minutos)

    def iniciar_dia(self):
        self.generar_pedidos()
        self.inicializar_camionetas()

    def generar_pedidos(self):
        list(map(lambda hora_de_pedido: self.generar_llamo_cliente_event(hora_de_pedido), self.utils.get_horas_de_pedidos(self.horas_por_dia)))

    def generar_llamo_cliente_event(self, hora_de_pedido):
        self.fel.append(
            LlamoClienteEvent(hora_de_pedido).attach(EncolarPedido()).attach(RechazarPedido())
        )

    def inicializar_camionetas(self):
        list(map(lambda camioneta: camioneta.volver_a_pizzeria(), self.camionetas))
        list(map(lambda camioneta: camioneta.cargar_pizzas(), self.camionetas))

    def termino_dia(self):
        return self.reloj.termino_dia()

    def obtener_dt_futuro(self, minutos):
        return self.reloj.obtener_dt_futuro(minutos)

    def obtener_eventos_de_ahora(self):
        return list(filter(lambda x: x.time == self.time, self.fel))

    def generar_tipo_de_pizza(self):
        return self.utils.generar_tipo_de_pizza()

    @property
    def time(self):
        return self.reloj.dia

    @property
    def dia(self):
        return self.reloj.dia

    @property
    def tiempo_inicio(self):
        return self.TIEMPO_INICIO

    @property
    def tiempo_fin(self):
        return self.TIEMPO_FIN

    @property
    def dias_a_simular(self):
        return self.tiempo_fin.date().day - self.tiempo_inicio.date().day

    @property
    def horas_por_dia(self):
        return self.CANTIDAD_HORAS_LABORALES

