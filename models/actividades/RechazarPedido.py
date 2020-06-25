from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad


class RechazarPedido(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        if not evento.cliente_esta_en_rango():
            evento.dia.rechazar_pedido()
