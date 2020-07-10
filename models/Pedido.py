from datetime import timedelta


class Pedido:

    def __init__(self, cliente, hora_toma, camioneta, tipo_pizza):
        self.cliente = cliente
        self.hora_toma = hora_toma
        self.hora_entrega = None
        self.ubicacion_origen = None
        self.tipo_pizza = tipo_pizza
        self.pizza = None
        self.camioneta = camioneta
        self.entregado = False

    @property
    def ubicacion(self):
        return self.cliente.ubicacion

    def esta_fuera_de_hora_de_entrega(self):
        from Simulacion import Simulacion
        return (Simulacion().time - self.hora_toma) > timedelta(minutes=30)
