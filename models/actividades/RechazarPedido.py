from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad


class RechazarPedido(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        if not simulacion.cliente_esta_en_rango(evento.cliente) or not evento.tipo_pizza in simulacion.tipos_de_pizza_disponibles:
            simulacion.rechazar_pedido(evento.cliente)
