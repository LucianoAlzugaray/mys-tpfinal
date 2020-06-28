from events.SimulacionEvent import SimulacionEvent


class EnviarPedidoEvent(SimulacionEvent):

    def __init__(self, hora, pedido):
        super().__init__(hora)
        self.pedido = pedido
