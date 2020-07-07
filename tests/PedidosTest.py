import unittest

from Simulacion import Simulacion
from events.LlamoClienteEvent import LlamoClienteEvent
from models.Camioneta import Camioneta

class PedidosTest(unittest.TestCase):

    def test_pedidos_se_generan_correctamente(self):
        simulacion = Simulacion()
        self.assertTrue(len(simulacion.fel) == 0)
        simulacion.iniciar_dia()
        self.assertTrue(len(simulacion.fel) > 0)


