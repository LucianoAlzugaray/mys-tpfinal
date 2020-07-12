from events.SimulacionEvent import SimulacionEvent


class EntregarPedidoEvent(SimulacionEvent):

    def __init__(self, hora, pedido):
        super().__init__(hora)
        self.pedido = pedido
        self.cliente = pedido.cliente