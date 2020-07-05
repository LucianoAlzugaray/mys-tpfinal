import math
from models.Cliente import Cliente
from events.SimulacionEvent import SimulacionEvent


class LlamoClienteEvent(SimulacionEvent):

    def __init__(self, hora, cliente, dia=None):
        super().__init__(hora)
        self.dia = dia
        from Simulacion import Simulacion
        simulacion = Simulacion()
        self.cliente = cliente
        self.tipo_pizza = simulacion.utils.generar_tipo_de_pizza()

    # TODO: quitar
    @staticmethod
    def obtener_camionetas_disponibles(camionetas):
        return list(filter(lambda x: x.disponible, camionetas))

    # TODO: quitar
    @staticmethod
    def camionetas_con_pizza_pedida(tipo, camionetas):
        return list(filter(lambda x: x.tiene_tipo(tipo), camionetas))
