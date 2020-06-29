from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad


class RechazarPedido(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        if not evento.cliente_esta_en_rango():
            from Simulacion import Simulacion
            Simulacion().rechazar_pedido(evento.cliente)