import unittest

from Configuracion import Configuracion
from Simulacion import Simulacion


class PedidosTest(unittest.TestCase):

    def test_pedidos_se_generan_correctamente(self):
        simulacion = Simulacion()
        simulacion.configurate(Configuracion.get_default_configuration())
        self.assertTrue(len(simulacion.fel) == 0)
        simulacion.iniciar_dia()
        self.assertTrue(len(simulacion.fel) > 0)


