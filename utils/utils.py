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
        for hora in range(horas):
            for pedido in range(np.random.poisson(Simulacion().pedidos_por_hora)):
                tiempo_exacto = math.trunc(random.uniform(0, 60)) + 60 * hora
                from Simulacion import Simulacion
                timestamp = Simulacion().tiempo_inicio + timedelta(minutes=tiempo_exacto)
                eventos_en_hora.append(timestamp)
        return eventos_en_hora

    ## Genera tipo de pizza aleatorio
    @staticmethod
    def generar_tipo_de_pizza():
        opcion = random.random()*100
        from Simulacion import Simulacion
        #[(PIZZA, PROB), (PIZZA,PROB)]
        pizzas_disponibles = Simulacion().pizzas_disponibles_con_probabilidades()
        selected = np.random.choice(len(pizzas_disponibles), 1, p=[pd[1] for pd in pizzas_disponibles])[0]
        return pizzas_disponibles[selected][0]


    ## Obtiene una ubicación del cliente aleatoria
    @staticmethod
    def generar_ubicacion_cliente():
        return np.random.normal(0, 10, 2) * 100  ##Para que quede como maximo 2000 como en el gráfico de bruno

    @staticmethod
    def sumar_minutos_a_hora(hora, minutos):
        return (datetime.combine(date.today(), hora) + timedelta(minutes=minutos)).time()
