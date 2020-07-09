from datetime import timedelta

from events.EntregarPizzaEvent import EntregarPizzaEvent
from models.actividades.Actividad import Actividad
from events.EnviarPedidoEvent import EnviarPedidoEvent
from models.actividades.EntregarPizza import EntregarPizza


class EnviarPedido(Actividad):

    def __init__(self):
        from Simulacion import Simulacion
        self.demora = self.tiempo_de_demora = Simulacion().utils.tiempo_entrega()

    def _ejecutar(self, evento: EnviarPedidoEvent):
        evento.pedido.camioneta.enviar_pedido()
        from Simulacion import Simulacion
        entregar_pizza_event = EntregarPizzaEvent(Simulacion().get_hora() + timedelta(minutes=self.demora), evento.pedido)
        entregar_pizza_event.attach(EntregarPizza(evento.pedido))
        Simulacion().add_event(entregar_pizza_event)