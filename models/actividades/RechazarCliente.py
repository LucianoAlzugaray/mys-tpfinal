from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad


class RechazarCliente(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        if not simulacion.cliente_esta_en_rango(evento.cliente):
            simulacion.rechazar_cliente(evento)
