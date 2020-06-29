from events.EntregarPizzaEvent import EntregarPizzaEvent
from models.actividades.Actividad import Actividad


class EntregarPizza(Actividad):

    def __init__(self, pedido):
        self.pedido = pedido

    def _ejecutar(self, evento: EntregarPizzaEvent):
        evento.pedido.camioneta.entregar_pedido(evento.pedido)
        from Simulacion import Simulacion
        Simulacion().remover_evento_vencimiento_pizza(evento.pedido.pizza)

