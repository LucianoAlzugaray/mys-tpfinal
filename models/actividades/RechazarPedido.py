from events.EntregarPedidoEvent import EntregarPedidoEvent
from models.actividades.Actividad import Actividad


class RechazarPedido(Actividad):

    def _ejecutar(self, evento: EntregarPedidoEvent):
        pedido = evento.pedido
        cliente = evento.cliente
        if not cliente.acepta_pedido(pedido):
            pedido.camioneta.rechazar_pedido(pedido)
