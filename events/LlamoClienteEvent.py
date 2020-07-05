import math
from models.Cliente import Cliente
from events.SimulacionEvent import SimulacionEvent


class LlamoClienteEvent(SimulacionEvent):

    def __init__(self, hora, cliente, dia=None):
        super().__init__(hora)
        self.dia = dia
        self.cliente = cliente
        from Simulacion import Simulacion
        self.tipo_pizza = Simulacion().utils.generar_tipo_de_pizza()

    @staticmethod
    def obtener_camionetas_disponibles(camionetas):
        return list(filter(lambda x: x.disponible, camionetas))

    @staticmethod
    def camionetas_con_pizza_pedida(tipo, camionetas):
        return list(filter(lambda x: x.tiene_tipo(tipo), camionetas))
