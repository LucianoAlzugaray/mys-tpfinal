from models.Pedido import Pedido


class Cliente:

    def __init__(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        self.ubicacion = simulacion.utils.generar_ubicacion_cliente()

    def acepta_pedido(self, pedido: Pedido):
        return not pedido.esta_fuera_de_hora_de_entrega()
