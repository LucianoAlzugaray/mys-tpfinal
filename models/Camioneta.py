from utils.utils import *
from models.Pizza import Pizza
from events.PizzaVenceEvent import PizzaVenceEvent


class Camioneta:
    pizzas_maximas = 40

    def __init__(self):
        self.ubicacion = [0, 0]
        self.pizzas = []
        self.disponible = True

    def cargar_camionetas(self, hora, fel):
        cantidad_pizzas_a_cargar = self.pizzas_maximas - len(self.pizzas)
        for i in range(cantidad_pizzas_a_cargar):
            pizza = self.generar_pizza(hora, fel)
            self.pizzas.append(pizza)

    def generar_pizza(self, hora, fel):
        tipo = generar_tipo_de_pizza()
        pizza = Pizza(tipo, hora)
        self.generar_evento_de_vencimiento(pizza, fel)
        return pizza

    def generar_evento_de_vencimiento(self, pizza, fel):
        vencimiento_de_pizza = PizzaVenceEvent(pizza, self)
        fel.append(vencimiento_de_pizza)

    def quitar_pizza(self, pizza):
        self.pizzas.remove(pizza)

    def tiene_tipo(self, tipo):
        lista_de_pizzas_de_tipo = [pizza for pizza in self.pizzas if pizza.tipo == tipo]
        return len(lista_de_pizzas_de_tipo) > 0
    
    def volver_a_pizzeria(self):
        self.ubicacion = [0,0]

    def descargarse(self):
        pizzas_descargadas = len(self.pizzas)
        self.pizzas = []
        return pizzas_descargadas