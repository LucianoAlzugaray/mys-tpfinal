from utils.utils import *
from models.Pizza import Pizza
from events.PizzaVenceEvent import PizzaVenceEvent


class Camioneta:
    cantidad_hornos = 1
    tamanio_hornos = 40

    def __init__(self):
        self.ubicacion = [0, 0]
        self.pizzas = []
        self.disponible = True

    def cargar_pizzas(self, hora, fel):
        for i in range(self.tamanio_hornos - len(self.pizzas)):
            self.pizzas.append(self.generar_pizza(hora, fel))

    def generar_pizza(self, hora, fel):
        pizza = Pizza(generar_tipo_de_pizza(), hora)
        fel.append(PizzaVenceEvent(pizza, self))
        return pizza

    def quitar_pizza(self, pizza):
        self.pizzas.remove(pizza)

    def tiene_tipo(self, tipo):
        return len(list(filter(lambda x: x.tipo == tipo, self.pizzas))) > 0

    def volver_a_pizzeria(self):
        self.ubicacion = [0, 0]

    def descargarse(self):
        pizzas_descargadas = len(self.pizzas)
        self.pizzas = []
        return pizzas_descargadas

    def get_pizzas_maximas(self):
        return self.cantidad_hornos * self.tamanio_hornos

    def esta_disponible(self):
        return self.disponible

