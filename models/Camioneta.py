from SimulacionExceptions.NoHayTipoPizzaEnCamionetaException import NoHayTipoPizzaEnCamionetaException
from utils.utils import *
from models.Pizza import Pizza


class Camioneta:
    cantidad_hornos = 1
    tamanio_hornos = 40

    def __init__(self):
        self.ubicacion = [0, 0]
        self.pizzas = []
        self.disponible = True

    def cargar_pizzas(self):
        for i in range(self.tamanio_hornos - len(self.pizzas)):
            self.pizzas.append(Pizza(generar_tipo_de_pizza()))

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

    def get_pizza(self, pizza):
        pizzas = list(filter(lambda x: x.pizza == pizza, self.pizzas))
        return None if len(pizzas) == 0 else pizzas[0]

    def reservar_pizza(self, tipo: TipoPizza) -> None:
        pizzas_disponibles = self.get_pizzas_disponibles()
        pizza_del_tipo = list(filter(lambda x: x.tipo == tipo, pizzas_disponibles))
        if len(pizza_del_tipo) == 0:
            raise NoHayTipoPizzaEnCamionetaException(f"No hay pizza del tipo {tipo}")

        pizza_del_tipo[0].reservada = True

    def get_pizzas_disponibles(self):
        return list(filter(lambda x: not x.vencida and not x.reservada, self.pizzas))

    @property
    def pizzas_reservadas(self):
        return list(filter(lambda x: x.reservada, self.pizzas))
