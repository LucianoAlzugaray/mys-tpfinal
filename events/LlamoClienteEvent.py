from events.SimulacionEvent import SimulacionEvent


class LlamoClienteEvent(SimulacionEvent):

    def __init__(self, hora, cliente, tipo_pizza):
        super().__init__(hora)
        self.cliente = cliente
        self.tipo_pizza = tipo_pizza

    def to_dict(self):
        return {
            "id": id(self),
            "cliente_id": id(self.cliente),
            "ubicacion": self.cliente.ubicacion,
            "tipo_de_pizza": self.tipo_pizza
        }
