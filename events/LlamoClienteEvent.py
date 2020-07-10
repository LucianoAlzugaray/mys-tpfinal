from events.SimulacionEvent import SimulacionEvent


class LlamoClienteEvent(SimulacionEvent):

    def __init__(self, hora, cliente, tipo_pizza):
        super().__init__(hora)
        self.cliente = cliente
        self.tipo_pizza = tipo_pizza
