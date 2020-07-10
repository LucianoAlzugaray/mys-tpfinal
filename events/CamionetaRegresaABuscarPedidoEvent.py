from events.SimulacionEvent import SimulacionEvent


class CamionetaRegresaABuscarPedidoEvent(SimulacionEvent):

    def __init__(self, pedido, hora):
        super().__init__(hora)
        self.pedido = pedido
        self.camioneta = pedido.camioneta
