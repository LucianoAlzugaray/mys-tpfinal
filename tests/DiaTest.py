import unittest

from Simulacion import Simulacion
from models.Cliente import Cliente
from events.LlamoClienteEvent import LlamoClienteEvent
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.actividades.EncolarCliente import EncolarCliente
from models.actividades.RechazarPedido import RechazarPedido


class DiaTestCase(unittest.TestCase):

    def setUp(self):
        self.dia = Simulacion().dia_actual

    def test_generar_pedidos(self):
        Simulacion().generar_pedidos()
        self.assertFalse(len(self.dia.fel) == 0)

    def test_obtener_cliente_de_la_cola(self):

        cliente = self.dia.obtener_cliente_de_cola()
        self.assertTrue(cliente is None)

        self.dia.camionetas[0].pizzas.append(Pizza(TipoPizza.ANANA))
        evento = LlamoClienteEvent(1, Cliente(), self.dia)
        evento.tipo_pizza = TipoPizza.ANANA
        evento.attach(EncolarCliente())
        evento.attach(RechazarPedido())
        evento.notify()

        cliente2 = self.dia.obtener_cliente_de_cola()
        if Simulacion().cliente_esta_en_rango( evento.cliente):
            self.assertFalse(cliente2 is None)
            self.assertIsInstance(cliente2, LlamoClienteEvent)
        else:
            self.assertEqual(1, len(self.dia.pedidos_rechazados))


if __name__ == '__main__':
    unittest.main()
