import unittest

from Simulacion import Simulacion
from events.LlamoClienteEvent import LlamoClienteEvent
from models.Cliente import Cliente
from models.Camioneta import Camioneta
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza


class LlamoClienteEventTest(unittest.TestCase):

    def setUp(self):
        self.evento = LlamoClienteEvent(10, None)
        self.camionetas = [Camioneta() for i in range(4)]

    def test_cliente_esta_en_rango(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        cliente = Cliente()

        cliente.ubicacion[0] = 1415
        cliente.ubicacion[1] = 1415
        self.evento.cliente = cliente

        self.assertFalse(simulacion.cliente_esta_en_rango(cliente))

        cliente.ubicacion[0] = 1414
        cliente.ubicacion[1] = 1414
        self.evento.cliente = cliente
        self.assertTrue(simulacion.cliente_esta_en_rango(cliente))

if __name__ == '__main__':
    unittest.main()
