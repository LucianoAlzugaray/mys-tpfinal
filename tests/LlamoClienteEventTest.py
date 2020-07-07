import unittest

from Simulacion import Simulacion
from events.LlamoClienteEvent import LlamoClienteEvent
from models.Camioneta import Camioneta
from models.Pedido import Pedido
from datetime import datetime

class LlamoClienteEventTest(unittest.TestCase):

    def setUp(self):
        from Simulacion import Simulacion
        self.simulacion = Simulacion()
        self.evento = LlamoClienteEvent(datetime.now())
        self.camionetas = [Camioneta() for i in range(4)]

    def test_cliente_esta_en_rango(self):
        from Simulacion import Simulacion

        pedido = self.evento.pedido
        pedido.ubicacion[0] = 1415
        pedido.ubicacion[1] = 1415
        self.simulacion = Simulacion()
        self.assertFalse(self.simulacion.cliente_esta_en_rango(pedido))

        pedido.ubicacion[0] = 1414
        pedido.ubicacion[1] = 1414

        self.assertTrue(self.simulacion.cliente_esta_en_rango(pedido))

if __name__ == '__main__':
    unittest.main()
