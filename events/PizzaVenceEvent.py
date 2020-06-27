from events.SimulacionEvent import SimulacionEvent


class PizzaVenceEvent(SimulacionEvent):
    tiempo_vencimiento_de_pizza = 120

    def __init__(self, pizza):
        super().__init__(pizza.hora + self.tiempo_vencimiento_de_pizza)
        self.pizza = pizza
