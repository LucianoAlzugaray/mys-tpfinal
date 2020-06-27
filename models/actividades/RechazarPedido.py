from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad


class RechazarPedido(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        if not evento.cliente_esta_en_rango():
            # TODO: rechazar pedido desde Simulacion
            evento.dia.rechazar_pedido(evento.cliente)
