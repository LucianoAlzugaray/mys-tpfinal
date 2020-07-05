import math

import numpy as np
import random

from models.TipoPizza import TipoPizza

class Utils:
    ## Obtiene una velocidad probabilistica para cargar pizzas
    @staticmethod
    def velocidad_carga_pizza():
        return np.random.exponential(1 / 10)

    ## Obtiene un tiempo de entrega probabilistico
    @staticmethod
    def tiempo_entrega():
        return np.random.exponential(10)

    ## Obtiene si se convenció al cliente o no de cambiar el tipo de pizza
    @staticmethod
    def convencer_al_cliente():
        return np.random.binomial(1, 0.3) == 1

    ## Obtiene pedidos generados en una hora
    # TODO: renombrar a generar pedidos y que ya devuelta una lista de horas distribuidas
    @staticmethod
    def cantidad_de_pedidos_en_una_hora():
        return np.random.poisson(20)

    @staticmethod
    def get_horas_de_pedidos(horas):
        eventos_en_hora = []
        for hora in range(horas):
            for pedido in range(Utils.cantidad_de_pedidos_en_una_hora()):
                tiempo_exacto = math.trunc(random.uniform(0, 60)) + 60 * hora
                eventos_en_hora.append(tiempo_exacto)
        return eventos_en_hora

    ## Genera tipo de pizza aleatorio
    @staticmethod
    def generar_tipo_de_pizza():
        opcion = random.random()
        if (opcion < 0.05):
            return TipoPizza.ANANA
        elif (opcion < 0.20):
            return TipoPizza.CALABRESA
        elif (opcion < 0.55):
            return TipoPizza.MOZZARELLA
        elif (opcion < 0.75):
            return TipoPizza.FUGAZZETA
        else:
            return TipoPizza.NAPOLITANA


    ## Obtiene una ubicación del cliente aleatoria
    @staticmethod
    def generar_ubicacion_cliente():
        ubicacion = np.random.normal(0, 10, 2)
        return ubicacion * 100  ##Para que quede como maximo 2000 como en el gráfico de bruno