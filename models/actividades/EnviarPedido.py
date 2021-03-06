from datetime import timedelta

from events.EventType import EventType
from models.actividades.Actividad import Actividad
from events.EnviarPedidoEvent import EnviarPedidoEvent


class EnviarPedido(Actividad):

    def __init__(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        self.demora = simulacion.utils.tiempo_entrega()

    def _ejecutar(self, evento: EnviarPedidoEvent):
        camioneta = evento.camioneta
        camioneta.enviar_pedido(evento.pedido)

