class EntregarPizzaEvent(object):

    def __init__(self, tiempo_entrega, camioneta, pizza):
        self.tiempo_de_entrega = tiempo_entrega
        self.camioneta = camioneta
        self.pizza = pizza