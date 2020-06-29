from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad


class RechazarPedido(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        if not simulacion.cliente_esta_en_rango(evento.cliente):
            simulacion.rechazar_pedido(evento.cliente)
