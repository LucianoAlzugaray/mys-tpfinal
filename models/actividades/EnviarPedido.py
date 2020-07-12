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
        evento.camioneta.enviar_pedido()
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.dispatch(EventType.ENTREGAR_PEDIDO, {'hora': simulacion.time + timedelta(minutes=self.demora), 'pedido': evento.pedido})

