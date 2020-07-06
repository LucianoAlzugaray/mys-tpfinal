from events.SimulacionEvent import SimulacionEvent
from models.Pedido import Pedido


class LlamoClienteEvent(SimulacionEvent):

    def __init__(self, time):
        super().__init__(time)
        self.pedido = Pedido(time)
