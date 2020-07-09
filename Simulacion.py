import itertools
import math
from datetime import time, datetime

from events.PizzaVenceEvent import PizzaVenceEvent
from models.Cliente import Cliente
from models.Dia import Dia
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.meta.Singleton import Singleton
from utils.utils import Utils
from models.Reloj import Reloj

import numpy as np
from functools import reduce


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

    DIA_INICIO = 9
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

    DIA_FIN = 9
    MES_FIN = 7
    ANIO_FIN = 2020
    HORA_FIN = 23
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
        return self.dia_actual.tiempo_actual
        # return self.reloj.dia

    def get_camioneta_by_pizza(self, pizza):
        camionetas = list(filter(lambda x: x.get_pizza(pizza) is not None, self.dia_actual.camionetas))
        return None if len(camionetas) == 0 else camionetas[0]

    def get_fel(self):
        return self.dia_actual.get_fel()

    @property
    def pedidos_rechazados(self):
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

    def get_diferencia_hora_actual(self, dt_hora):
        return self.reloj.get_diferencia_hora_actual(dt_hora)

    '''Pedidos que fueron entregados realmente'''
    def pedidos_entregados(self):
        return list(filter(lambda pedido: pedido.entregado == True, self.pedidos))

    '''Pedidos que fueron rechazados'''
    #TODO el nombre rechazado en el dashboard no me parece correcto deberia ser perdido
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

        return np.mean(minutos_espera)

    '''El porcentaje de desperdicios a nivel corrida (365 dias)'''
    def porcentaje_desperdicio(self):
        desperdicio_total = []

        for dia in range(self.dias_a_simular):
            desperdicio_diario = dia.desperdicios + dia.desperdicio_por_fin_de_dia
            desperdicio_total.append(desperdicio_diario)

        return np.mean(desperdicio_total)

    '''devuelve la cantidad de clientes atendidos (que recibieron una pizza) por hora'''
    def clientes_atendidos_por_hora(self):

        clientes_atendidos_por_hora = []
        for hora in range(self.horas_por_dia):
            #TODO pedido.hora_entrega.hour por el timestamp, hacer diccionario?
            clientes_atendidos = list(filter(lambda pedido: pedido.hora_entrega.hour == (hora+10), self.pedidos_entregados()))
            clientes_atendidos_por_hora.append(len(clientes_atendidos))

        return clientes_atendidos_por_hora

    '''las camionetas deberian llevar su distancia recorrida'''
    def distacia_recorrida(self):

        distancias_camionetas = list(map(lambda x: x.distancia_recorrida, self.camionetas))

        return reduce(lambda acumulador, distancia_camioneta: acumulador+distancia_camioneta, distancias_camionetas)

    ''' tiempo promedio entre recargas a nivel simulación'''
    def tiempo_entre_recargas(self):

        tiempo_promedio_entre_recargas = list(map(lambda x: np.mean(x.tiempo_entre_recargas), self.camionetas))

        return np.mean(tiempo_promedio_entre_recargas)
