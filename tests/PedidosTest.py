import unittest
from Simulacion import Simulacion
import numpy as np

from events.LlamoClienteEvent import LlamoClienteEvent
from models.Camioneta import Camioneta
from models.Dia import Dia


class PedidosTest(unittest.TestCase):

    def test_pedidos_se_generan_correctamente(self):
        dia = Dia(10, [Camioneta()])
        dia.iniciar_dia()

        fel = dia.fel

        self.assertTrue(len(fel) > 0)

        for evento in dia.fel:
            self.assertIsInstance(evento, LlamoClienteEvent)


