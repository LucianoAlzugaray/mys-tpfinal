class PizzaVenceEvent:
    tiempo_vencimiento_de_pizza = 120

    def __init__(self, pizza, camioneta):
        self.hora = pizza.hora + self.tiempo_vencimiento_de_pizza
        self.pizza = pizza
        self.camioneta = camioneta

    def ejecutar_actividad(self, dia):
        self.camioneta.quitar_pizza(self.pizza)
        dia.desperdicio += 1