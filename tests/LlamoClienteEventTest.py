import unittest
from events.LlamoClienteEvent import LlamoClienteEvent
from models.Cliente import Cliente
from models.Camioneta import Camioneta


class LlamoClienteEventTest(unittest.TestCase):

    def setUp(self):
        from Simulacion import Simulacion
        self.simulacion = Simulacion()
        self.evento = LlamoClienteEvent(10, Cliente(), Simulacion().generar_tipo_de_pizza())
        self.camionetas = [Camioneta() for i in range(4)]

    def test_cliente_esta_en_rango(self):
        from Simulacion import Simulacion
        cliente = Cliente()

        cliente.ubicacion[0] = 1415
        cliente.ubicacion[1] = 1415
        self.evento.cliente = cliente

        self.simulacion = Simulacion()
        self.assertFalse(self.simulacion.cliente_esta_en_rango(cliente))

        cliente.ubicacion[0] = 1414
        cliente.ubicacion[1] = 1414
        self.evento.cliente = cliente
        self.assertTrue(self.simulacion.cliente_esta_en_rango(cliente))

if __name__ == '__main__':
    unittest.main()
