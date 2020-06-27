from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad
from ..Pedido import Pedido


class EncolarCliente(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        if evento.cliente_esta_en_rango():
            from Simulacion import Simulacion
            camioneta = Simulacion().seleccionar_camioneta(evento.cliente, evento.tipo_pizza)
            pizza = camioneta.reservar_pizza(evento.tipo_pizza)
            pedido = Pedido(evento.cliente, evento.hora, camioneta, pizza)
            camioneta.asignar_pedido(pedido)
            evento.dia.encolar_cliente(evento)