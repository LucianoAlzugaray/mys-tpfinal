import unittest
from Simulacion import Simulacion


class PedidosTest(unittest.TestCase):

    def test_pedidos_se_generan_correctamente(self):
        simulacion = Simulacion()
        self.assertTrue(len(simulacion.fel) == 0)
        simulacion.iniciar_dia()
        self.assertTrue(len(simulacion.fel) > 0)


