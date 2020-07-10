import itertools
import json
import math
from datetime import datetime, timedelta, time
from functools import reduce
import numpy as np
from events.PizzaVenceEvent import PizzaVenceEvent
from events.SimulacionEventFactory import SimulacionEventFactory
from models.Cliente import Cliente
from models.Pedido import Pedido
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.meta.Singleton import Singleton
from utils.utils import Utils
from models.Reloj import Reloj
from models.EventTypeEnum import EventTypeEnum
import paho.mqtt.client as paho
from random import random
import json

def generar_camionetas(configuracion):
    from models.Camioneta import Camioneta
    return [Camioneta(configuracion.hornosPorCamioneta, configuracion.pizzasPorHorno) for i in range(configuracion.cantidadCamionetas)]

class Simulacion(metaclass=Singleton):
    CANTIDAD_HORAS_LABORALES = 12
    CANTIDAD_MINUTOS_LABORALES = CANTIDAD_HORAS_LABORALES * 60
    HORA_DE_CIERRE = 23
    MINUTOS_DE_CIERRE = 0
    HORA_FIN_TOMA_DE_PEDIDOS = 22
    MINUTOS_FIN_TOMA_DE_PEDIDOS = 30

    def __init__(self):
        self.dias_a_simular = None
        self.tiempo_inicio = None
        self.tiempo_fin = None
        self.pedidos_por_hora = None
        self.experimentos = None
        self.rango_de_atencion = 2000
        self.volver_al_terminar_todos_los_pedidos = False

        self.fel = []
        self.events = []
        self.pedidos = []
        self.camionetas = []
        self.desperdicios = []
        self.clientes_rechazados = []
        self.tipos_de_pizza_disponibles = []
        self.porcentaje_desperdicio_diario = []

        self.utils = Utils()
        self.reloj = Reloj()
        self.event_factory = SimulacionEventFactory()

    def configurate(self, configuracion):
        self.dias_a_simular = (configuracion['fin'] - configuracion['inicio']).days
        self.tiempo_inicio = configuracion['inicio']
        self.tiempo_fin = configuracion['fin']
        self.experimentos = configuracion['cantidadExperimentos']
        self.pedidos_por_hora = configuracion['pedidosPorHora']
        self.dias_corridos = []
        from models.Camioneta import Camioneta
        self.camionetas += [Camioneta(configuracion['hornosPorCamioneta'], configuracion['pizzasPorHorno']) for i in range(configuracion['cantidadCamionetas'])]
        self.tipos_de_pizza_disponibles = configuracion['tipos_de_pizza']

        self.reloj.configurate({
            'dia': self.tiempo_inicio,
            'hora_cierre': time(self.HORA_DE_CIERRE, self.MINUTOS_DE_CIERRE),
        })

    def run(self):
        for experimento in range(self.experimentos):
            for dia in range(self.dias_a_simular):
                self.iniciar_dia()

                while not self.termino_dia():
                    evento = self.next_event()
                    if evento is not None:
                        evento.notify()

                self.finalizar_dia()
                self.publicar_resultados()

    def publicar_resultados(self):
        tiempo_espera = self.tiempo_espera()
        porcentaje_desperdicio = self.porcentaje_desperdicio()
        pedidos_entregados = self.pedidos_entregados()
        pedidos_perdidos = self.pedidos_perdidos()
        distacia_recorrida = self.distacia_recorrida()
        tiempo_entre_recargas = self.tiempo_entre_recargas()
        pizzas_pedidas_por_tipo = json.dumps(self.pizzas_pedidas_por_tipo())

        client = paho.Client()
        client.connect("172.16.240.10", 1883)
        client.publish("espera-de-cliente", tiempo_espera)
        client.publish("porcentaje-de-desperdicios", porcentaje_desperdicio)
        client.publish("pedidos-entregados", len(pedidos_entregados))
        client.publish("pedidos-rechazados", len(pedidos_perdidos))
        client.publish("distancias-recorridas", distacia_recorrida)
        client.publish("tiempo-entre-recargas", tiempo_entre_recargas)
        client.publish("pedido-sin-tipo-de-camioneta", math.trunc(random() * 10))
        client.publish("pizzas-pedidas-por-tipo", pizzas_pedidas_por_tipo)

    # TODO: armar los csv de pedidos y desperdicios
    def obtener_datos(self):
        pass

    def add_event(self, event, kwargs=None):
        event = self.event_factory.get_event(event, kwargs)
        self.fel.append(event)
        self.fel = sorted(self.fel, key=lambda evento: evento.hora)


    def get_camioneta_by_pizza(self, pizza):
        camionetas = list(filter(lambda x: x.get_pizza(pizza) is not None, self.camionetas))
        return None if len(camionetas) == 0 else camionetas[0]

    def rechazar_pedido(self, pedido: Pedido) -> None:
        self.clientes_rechazados.append(pedido)

    def rechazar_cliente(self, cliente: Cliente) -> None:
        self.clientes_rechazados.append(cliente)

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
        if ((punto1 is None )or(punto2 is None)):
            return None
        else:
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
        return self.ordenar_camionetas_por_ubicacion([0, 0], 'get_ubicacion_pedido_en_curso')[0]

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

    def iniciar_dia(self):
        self.generar_eventos_de_llamada()
        self.inicializar_camionetas()

    def generar_eventos_de_llamada(self):
        list(map(lambda hora_de_pedido: self.generar_llamo_cliente_event(hora_de_pedido),
                 self.utils.get_horas_de_pedidos(self.horas_por_dia - 1)))

    def generar_llamo_cliente_event(self, hora_de_pedido):
        kwargs = {
            'hora': hora_de_pedido,
            'cliente': Cliente(),
            'tipo_pizza': self.generar_tipo_de_pizza()
        }
        self.add_event(EventTypeEnum.LLAMO_CLIENTE, kwargs)

    def inicializar_camionetas(self):
        list(map(lambda camioneta: camioneta.volver_a_pizzeria(), self.camionetas))
        list(map(lambda camioneta: camioneta.cargar_pizzas(), self.camionetas))

    def termino_dia(self):
        return self.reloj.termino_dia()

    def obtener_dt_futuro(self, minutos):
        return self.reloj.obtener_dt_futuro(minutos)

    def obtener_eventos_de_ahora(self):
        if None in self.fel:
            return None
        return list(filter(lambda x: x.hora == self.time, self.fel))

    def generar_tipo_de_pizza(self):
        return self.utils.generar_tipo_de_pizza()

    @property
    def time(self):
        return self.reloj.dia

    @property
    def dia(self):
        return self.reloj.dia

    def iniciar_dia(self):
        self.generar_eventos_de_llamada()
        self.inicializar_camionetas()

    @property
    def horas_por_dia(self):
        return self.CANTIDAD_HORAS_LABORALES

    def get_diferencia_hora_actual(self, dt_hora):
        return self.reloj.get_diferencia_hora_actual(dt_hora)

    '''Pedidos que fueron entregados realmente'''
    def pedidos_entregados(self):
        return list(filter(lambda pedido: pedido.entregado == True, self.pedidos))

    '''Pedidos que fueron rechazados'''
    # TODO el nombre rechazado en el dashboard no me parece correcto deberia ser perdido
    def pedidos_perdidos(self):
        return list(filter(lambda pedido: pedido.entregado == False, self.pedidos))

    '''Devuelve un diccionario tipo_pizza: cantidad'''
    def pizzas_pedidas_por_tipo(self):
        cont_anana = 0
        cont_mozzarela = 0
        cont_napolitana = 0
        cont_calabresa = 0
        cont_fugazzeta = 0

        for pedido in self.pedidos_entregados():
            if pedido.pizza.tipo == TipoPizza.FUGAZZETA:
                cont_fugazzeta += 1
            elif pedido.pizza.tipo == TipoPizza.NAPOLITANA:
                cont_napolitana += 1
            elif pedido.pizza.tipo == TipoPizza.ANANA:
                cont_anana += 1
            elif pedido.pizza.tipo == TipoPizza.CALABRESA:
                cont_calabresa += 1
            else:
                cont_mozzarela += 1

        return {'Anana': cont_anana, 'Mozzarella': cont_mozzarela, 'Napolitana': cont_napolitana,
                'Calabresa': cont_calabresa, 'Fugazzeta': cont_fugazzeta}

    '''Tiempo promedio de espera de los clientes a nivel simulacion'''
    def tiempo_espera(self):

        minutos_espera = list(map(lambda pedido: pedido.hora_entrega - pedido.hora_toma, self.pedidos_entregados()))
        media = np.mean(minutos_espera)
        return math.trunc(media.seconds / 60)
        # minutos = media. * 60 + media.minute


    '''El porcentaje de desperdicios a nivel corrida (365 dias)'''
    def porcentaje_desperdicio(self):
        return np.mean(self.porcentaje_desperdicio_diario)

    '''devuelve la cantidad de clientes atendidos (que recibieron una pizza) por hora'''
    def clientes_atendidos_por_hora(self):

        clientes_atendidos_por_hora = []
        for hora in range(self.horas_por_dia):
            # TODO pedido.hora_entrega.hour por el timestamp, hacer diccionario?
            clientes_atendidos = list(
                filter(lambda pedido: pedido.hora_entrega.hour == (hora + 10), self.pedidos_entregados()))
            clientes_atendidos_por_hora.append(len(clientes_atendidos))

        return clientes_atendidos_por_hora

    '''las camionetas deberian llevar su distancia recorrida'''
    def distacia_recorrida(self):

        distancias_camionetas = list(map(lambda x: x.distancia_recorrida, self.camionetas))

        return reduce(lambda acumulador, distancia_camioneta: acumulador + distancia_camioneta, distancias_camionetas)

    ''' tiempo promedio entre recargas a nivel simulación'''
    def tiempo_entre_recargas(self):

        tiempo_promedio_entre_recargas = list(map(lambda x: np.mean(x.tiempo_entre_recargas), self.camionetas))

        return np.mean(tiempo_promedio_entre_recargas)

    def generar_pizza(self, tipo_pizza):
        pizza = Pizza(tipo_pizza, self.time)
        self.add_event(EventTypeEnum.PIZZA_VENCE, {'pizza': pizza})
        return pizza

    ''' Metodo para avanzar el tiempo dado un datetime.'''
    def avanzar_reloj_time(self, time: datetime):
        self.reloj.avanzar_time(time)

    '''Obtiene el porcentaje de desperdicios en el dia'''
    def add_desperdicio(self, pizza, hora):
        self.desperdicios.append(pizza)
        if self.pedidos_del_dia > 0:
            self.porcentaje_desperdicio_diario = (self.desperdicios_del_dia/self.pedidos_del_dia) * 100
        else:
            self.porcentaje_desperdicio_diario = 0

    @property
    def desperdicios_del_dia(self):
        return len(list(filter(lambda x: x.hora.day == self.time.day, self.desperdicios)))

    @property
    def pedidos_del_dia(self):
        return len(list(filter(lambda x: x.hora_toma.day == self.time.day, self.pedidos)))

    def next_event(self):
        if len(self.fel) == 0:
            self.reloj.terminar_el_dia()
            return None

        evento = self.fel[0]
        self.events.append(evento)
        self.fel.remove(evento)
        return evento

    def finalizar_dia(self):
        desperdicios = list(itertools.chain(*map(lambda x: x.pizzas, self.camionetas)))
        list(map(lambda x: self.add_desperdicio(x, self.dia), desperdicios))
        list(map(lambda x: x.finalizar_dia(), self.camionetas))


