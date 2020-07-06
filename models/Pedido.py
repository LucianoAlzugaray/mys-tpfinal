class Pedido:

    def __init__(self, hora_toma):
        self.hora_toma = hora_toma
        self.entregado = False
        self.hora_entrega = None
        self.ubicacion_origen = None
        self.pizza = None
        self.camioneta = None
        from Simulacion import Simulacion
        self.ubicacion = Simulacion().utils.generar_ubicacion_cliente()
        self.tipo_pizza = Simulacion().generar_tipo_de_pizza()