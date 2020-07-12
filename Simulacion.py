import itertools
import json
import math
import os
from datetime import datetime, time
from functools import reduce
import numpy as np
import pandas as pd
from events.EntregarPedidoEvent import EntregarPedidoEvent
from events.PizzaVenceEvent import PizzaVenceEvent
from events.SimulacionEventFactory import SimulacionEventFactory
from models.Cliente import Cliente
from models.Pedido import Pedido
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.meta.Singleton import Singleton
from utils.utils import Utils
from models.Reloj import Reloj
from events.EventType import EventType
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
        self.pedidos_en_espera = []
        self.clientes_rechazados = []
        self._tipos_de_pizza_disponibles = []
        self.porcentaje_desperdicio_diario = []
        self.resultados_experimentos = []

        self.utils = Utils()
        self.reloj = Reloj()
        self.event_factory = SimulacionEventFactory()

        self.data = {
            "desperdicios": None,
            "clientes_rechazados": None,
            "pedidos": None
        }

        self.client = paho.Client()
        self.client.connect("172.16.240.10", 1883)

    def configurate(self, configuracion):
        self.dias_a_simular = (configuracion['fin'] - configuracion['inicio']).days
        self.tiempo_inicio = configuracion['inicio']
        self.tiempo_fin = configuracion['fin']
        self.experimentos = configuracion['cantidadExperimentos']
        self.pedidos_por_hora = configuracion['pedidosPorHora']
        from models.Camioneta import Camioneta
        self.camionetas += [Camioneta(configuracion['hornosPorCamioneta'], configuracion['pizzasPorHorno']) for i in range(configuracion['cantidadCamionetas'])]
        self._tipos_de_pizza_disponibles = configuracion['tipos_de_pizza']


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
                print(f"PUBLICANDO RESULTADOS DEL DIA {self.time.date()}")
                self.publicar_resultados_dia()
            print(f"PUBLICANDO RESULTADOS DEL EXPERIMENTO {experimento+1}")
            self.publicar_resultados_experimento(experimento)
            self.guardar_datos(experimento)
            self.clean_experimento()
        self.exportar_datos()


    @property
    def tipos_de_pizza_disponibles(self):
        return list(map(lambda x: x['tipo'], self._tipos_de_pizza_disponibles))

    def clean_experimento(self):
        self.fel = []
        self.events = []
        self.pedidos = []
        self.desperdicios = []
        self.clientes_rechazados = []
        self.porcentaje_desperdicio_diario = []

    def publicar_resultados_experimento(self, experimento):
        row = {
            "corrida": experimento.__str__(),
            "esperaClientes": self.tiempo_espera(),
            "clientesHora": np.mean(self.clientes_atendidos_por_hora()),
            "pizzasDia": len(self.pedidos_entregados()) / self.reloj.dias_transcurridos,
            "desperdicios": self.porcentaje_desperdicio(),
            "distanciasRecorridas": self.distacia_recorrida(),
            "recargaCamionetas": self.tiempo_entre_recargas()
        }

        self.resultados_experimentos.append(row)
        data = json.dumps(self.resultados_experimentos)
        self.client.publish('resumen', data)

    def publicar_resultados_dia(self):
        if len(self.pedidos) == 0:
            return
        tiempo_espera = self.tiempo_espera()
        porcentaje_desperdicio = self.porcentaje_desperdicio()
        pedidos_entregados = self.pedidos_entregados()
        pedidos_perdidos = self.pedidos_perdidos()
        distacia_recorrida = self.distacia_recorrida()
        tiempo_entre_recargas = self.tiempo_entre_recargas()
        pizzas_pedidas_por_tipo = json.dumps(self.pizzas_pedidas_por_tipo())

        self.client.publish("espera-de-cliente", tiempo_espera)
        self.client.publish("porcentaje-de-desperdicios", porcentaje_desperdicio)
        self.client.publish("pedidos-entregados", len(pedidos_entregados))
        self.client.publish("pedidos-rechazados", len(pedidos_perdidos))
        self.client.publish("distancias-recorridas", distacia_recorrida)
        self.client.publish("tiempo-entre-recargas", tiempo_entre_recargas)
        self.client.publish("pedido-sin-tipo-de-camioneta", math.trunc(random() * 10))
        self.client.publish("pizzas-pedidas-por-tipo", pizzas_pedidas_por_tipo)

    # TODO: armar los csv de pedidos y desperdicios
    def guardar_datos(self, experimento):
        pedidos_data = [pedido.to_dict() for pedido in self.pedidos]
        desperdicios_data = [pizza.to_dict() for pizza in self.desperdicios]
        clientes_rechazados_data = [cliente.to_dict() for cliente in self.clientes_rechazados]

        pedidos_df = pd.DataFrame(pedidos_data)
        desperdicios_df = pd.DataFrame(desperdicios_data)
        clientes_rechazados_df = pd.DataFrame(clientes_rechazados_data)

        pedidos_df["experimento"] = experimento + 1
        desperdicios_df["experimento"] = experimento + 1
        clientes_rechazados_df["experimento"] = experimento + 1


        if self.data["pedidos"] is None:
            self.data["pedidos"] = pedidos_df
        else:
            self.data["pedidos"].append(pedidos_df)

        if self.data["desperdicios"] is None:
            self.data["desperdicios"] = desperdicios_df
        else:
            self.data["desperdicios"].append(desperdicios_df)

        if self.data["clientes_rechazados"] is None:
            self.data["clientes_rechazados"] = clientes_rechazados_df
        else:
            self.data["clientes_rechazados"].append(clientes_rechazados_df)

    def exportar_datos(self):
        outdir = './store'
        if not os.path.exists(outdir):
            os.mkdir(outdir)

        self.data["pedidos"].to_csv(f"{outdir}/pedidos.csv", index=False)
        self.data["desperdicios"].to_csv(f"{outdir}/desperdicios.csv", index=False)
        self.data["clientes_rechazados"].to_csv(f"{outdir}/clientes_rechazados.csv", index=False)

    def dispatch(self, event, kwargs=None):
        if event == EventType.ENTREGAR_PEDIDO:
            eventos_entregar_pedido = list(filter(lambda x: isinstance(x, EntregarPedidoEvent), self.events))
            tiene_el_mismo_pedido = list(filter(lambda x: x.pedido == kwargs['pedido'], eventos_entregar_pedido))
            if len(tiene_el_mismo_pedido) > 0:
                return

        event = self.event_factory.get_event(event, kwargs)

        self.fel.append(event)
        self.fel = sorted(self.fel, key=lambda evento: evento.hora)


    def get_camioneta_by_pizza(self, pizza):
        camionetas = list(filter(lambda x: x.get_pizza(pizza) is not None, self.camionetas))
        return None if len(camionetas) == 0 else camionetas[0]

    def rechazar_pedido(self, pedido: Pedido) -> None:
        pedido.entregado = False
        pedido.camioneta.pedido_en_curso = None


    def rechazar_cliente(self, cliente):
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

        camionetas_disponibles = list(filter(lambda x: x.disponible, self.camionetas))
        for camioneta in camionetas_disponibles:
            metodo = getattr(camioneta, method_name)
            ubicacion_camioneta = metodo()
            distancia = self.obtener_distancia(ubicacion, ubicacion_camioneta)
            distancias[camioneta] = distancia

        if None in list(map(lambda x: x[1], distancias.items())):
            raise Exception("ordenar_camionetas_por_ubicacion: No es posible ordenar las camionetas", [camionetas_disponibles, ubicacion, method_name])

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
        tipos_de_pizza_disponibles = list(set(map(lambda x: x.tipo, pizzas_disponibles)))
        return tipos_de_pizza_disponibles if tipos_de_pizza_disponibles else [self.utils.generar_pizza()]

    def obtener_camioneta_a_volver_al_restaurante(self):
        if self.volver_al_terminar_todos_los_pedidos:
            return self.obtener_camioneta_mas_proxima_a_liberarse()

        return self.obtener_camioneta_mas_cercana_al_restaurante()

    def obtener_camioneta_mas_proxima_a_liberarse(self):
        # TODO: la camioneta debe calcular cuanto va a tardar en liberarse
        return self.ordenar_camionetas_por_ubicacion([0, 0], 'cuanto_tardas_en_linerarte')

    def obtener_camioneta_mas_cercana_al_restaurante(self):
        camionetas = self.ordenar_camionetas_por_ubicacion([0, 0], 'get_ubicacion_pedido_en_curso')
        return camionetas[0] if len(camionetas) > 0 else None

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
        self.reloj.iniciar_dia()
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
        self.dispatch(EventType.LLAMO_CLIENTE, kwargs)

    def inicializar_camionetas(self):
        list(map(lambda camioneta: camioneta.volver_a_pizzeria(), self.camionetas))
        list(map(lambda camioneta: camioneta.cargar_pizzas(), self.camionetas))

    def termino_dia(self):
        return self.reloj.termino_dia

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

    def get_pedido_by_pizza(self, pizza):
        result = list(filter(lambda x: x.pizza == pizza, self.pedidos))
        if len(result) > 0:
            return result[0]

        raise Exception("get_pedido_by_pizza: Se pinchó para la mierda")


    @property
    def horas_por_dia(self):
        return self.CANTIDAD_HORAS_LABORALES

    def get_diferencia_hora_actual(self, dt_hora):
        return self.reloj.get_diferencia_hora_actual(dt_hora)

    '''Pedidos que fueron entregados realmente'''
    def pedidos_entregados(self):
        return list(filter(lambda pedido: pedido.entregado, self.pedidos))

    '''Pedidos que fueron rechazados'''
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


    '''El porcentaje de desperdicios a nivel corrida (365 dias)'''
    def porcentaje_desperdicio(self):
        return np.mean(self.porcentaje_desperdicio_diario)

    '''devuelve la cantidad de clientes atendidos (que recibieron una pizza) por hora'''
    def clientes_atendidos_por_hora(self):

        clientes_atendidos_por_hora = []
        for hora in range(self.horas_por_dia):
            # TODO pedido.hora_entrega.hour por el timestamp, hacer diccionario?
            # TODO 10 cambiar a hora de inicio
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

        lista_de_tiempos_promedio_entre_recargas = list(map(lambda x: np.mean(x.tiempo_entre_recargas), self.camionetas))
        tiempo_promedio_entre_recargas = np.mean(lista_de_tiempos_promedio_entre_recargas)
        if(math.isnan(tiempo_promedio_entre_recargas)):
            return 0
        return tiempo_promedio_entre_recargas

    def generar_pizza(self, tipo_pizza):
        pizza = Pizza(tipo_pizza, self.time)
        self.dispatch(EventType.PIZZA_VENCE, {'pizza': pizza})
        return pizza


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
        self.reloj.avanzar_time(evento.hora)
        self.events.append(evento)
        self.fel.remove(evento)
        return evento

    def finalizar_dia(self):
        desperdicios = list(itertools.chain(*map(lambda x: x.pizzas, self.camionetas)))
        list(map(lambda x: self.add_desperdicio(x, self.dia), desperdicios))
        list(map(lambda x: x.finalizar_dia(), self.camionetas))

    def atender_pedidos_en_espera(self, camioneta):
        pedidos_en_espera = self.pedidos_en_espera[0: camioneta.cantidad_de_pizzas_a_cargar]

        for pedido in pedidos_en_espera:
            camioneta.pizzas.append(self.generar_pizza(pedido.tipo_pizza))
            camioneta.pedidos.append(pedido)
            pedido.camioneta = camioneta
            self.add_pedido(pedido)
            self.pedidos_en_espera.remove(pedido)



