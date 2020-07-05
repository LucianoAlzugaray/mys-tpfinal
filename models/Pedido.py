class Pedido:

    def __init__(self, cliente, hora_toma, camioneta, tipo_pizza):
        from Simulacion import Simulacion
        self.cliente = cliente
        self.hora_toma = hora_toma
        # TODO: quitar (se pasa a la actividad Entregar pedido)
        self.tiempo_de_demora = Simulacion().utils.tiempo_entrega()
        self.hora_entrega = None
        self.ubicacion_origen = None
        self.tipo_pizza = tipo_pizza
        self.pizza = None
        self.camioneta = camioneta
        self.entregado = False

    @property
    def ubicacion(self):
        return self.cliente.ubicacion
