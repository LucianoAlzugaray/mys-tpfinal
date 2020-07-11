from events.EntregarPedidoEvent import EntregarPedidoEvent
from models.actividades.Actividad import Actividad


class EntregarPedido(Actividad):

    def _ejecutar(self, evento: EntregarPedidoEvent):
        if not evento.pedido.esta_fuera_de_hora_de_entrega() or evento.pedido.entregado:
            from Simulacion import Simulacion
            simulacion = Simulacion()
            evento.pedido.camioneta.entregar_pedido(evento.pedido)
            simulacion.remover_evento_vencimiento_pizza(evento.pedido.pizza)

