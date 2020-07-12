import math
import numpy as np
import random
from models.TipoPizza import TipoPizza
from datetime import timedelta, datetime, date


class Utils:

    ## Obtiene una velocidad probabilistica para cargar pizzas
    @staticmethod
    def velocidad_carga_pizza():
        return math.trunc(np.random.exponential(10))

    ## Obtiene un tiempo de entrega probabilistico
    @staticmethod
    def tiempo_entrega():
        return math.trunc(np.random.exponential(10))


    ## Obtiene si se convenció al cliente o no de cambiar el tipo de pizza
    @staticmethod
    def convencer_al_cliente():
        return np.random.binomial(1, 0.3) == 1

    @staticmethod
    def get_horas_de_pedidos(horas):
        eventos_en_hora = []
        from Simulacion import Simulacion
        simulacion = Simulacion()
        for hora in range(horas):
            for pedido in range(np.random.poisson(simulacion.pedidos_por_hora)):
                tiempo_exacto = math.trunc(random.uniform(0, 60)) + 60 * hora
                timestamp = simulacion.time + timedelta(minutes=tiempo_exacto)
                eventos_en_hora.append(timestamp)
        return eventos_en_hora

    @staticmethod
    def generar_pizza():
        from Simulacion import Simulacion
        simulacion = Simulacion()
        opcion = random.random()
        for tipo_disponible in simulacion._tipos_de_pizza_disponibles:
            if opcion < tipo_disponible['probabilidad']:
                return tipo_disponible['tipo']

    ## Genera tipo de pizza aleatorio
    @staticmethod
    def generar_tipo_de_pizza():

        opcion = random.random()
        if opcion < 0.05:
            return TipoPizza.ANANA
        elif opcion < 0.20:
            return TipoPizza.CALABRESA
        elif opcion < 0.55:
            return TipoPizza.MOZZARELLA
        elif opcion < 0.75:
            return TipoPizza.FUGAZZETA
        else:
            return TipoPizza.NAPOLITANA




    ## Obtiene una ubicación del cliente aleatoria
    @staticmethod
    def generar_ubicacion_cliente():
        return np.random.normal(0,7,2)*100