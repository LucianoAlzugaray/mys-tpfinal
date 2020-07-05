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