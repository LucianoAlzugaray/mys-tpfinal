from datetime import timedelta

from events.EntregarPizzaEvent import EntregarPizzaEvent
from models.EventTypeEnum import EventTypeEnum
from models.actividades.Actividad import Actividad
from events.EnviarPedidoEvent import EnviarPedidoEvent


class EnviarPedido(Actividad):

    def __init__(self):
        from Simulacion import Simulacion
        self.demora = Simulacion().utils.tiempo_entrega()

    def _ejecutar(self, evento: EnviarPedidoEvent):
        evento.pedido.camioneta.enviar_pedido()
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.add_event(EventTypeEnum.ENTREGAR_PIZZA, {'hora': Simulacion().time + timedelta(minutes=self.demora), 'pedido': evento.pedido})

