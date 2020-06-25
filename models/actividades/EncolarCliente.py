from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad


class EncolarCliente(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        if evento.cliente_esta_en_rango():
            evento.dia.encolar_cliente(evento)
