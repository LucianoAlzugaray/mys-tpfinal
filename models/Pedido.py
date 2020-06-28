class Pedido:

    def __init__(self, cliente, hora_toma, camioneta, pizza):
        self.cliente = cliente
        self.hora_toma = hora_toma
        self.hora_entrga = None
        self.ubicacion_origen = None
        self.pizza = pizza
        self.camioneta = camioneta

    @property
    def ubicacion(self):
        return self.cliente.ubicacion
