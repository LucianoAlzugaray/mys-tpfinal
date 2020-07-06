from events.SimulacionEvent import SimulacionEvent


class EnviarPedidoEvent(SimulacionEvent):

    def __init__(self, time, pedido):
        super().__init__(time)
        self.pedido = pedido
