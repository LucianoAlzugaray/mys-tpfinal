import unittest
from models.Dia import Dia
from events.LlamoClienteEvent import LlamoClienteEvent
from models.actividades.EncolarCliente import EncolarCliente
from models.actividades.RechazarPedido import RechazarPedido


class DiaTestCase(unittest.TestCase):

    def setUp(self):
        self.dia = Dia(10, 4)

    def test_cargar_camionetas(self):
        self.dia.cargar_camionetas()
        for camioneta in self.dia.camionetas:
            self.assertTrue(len(camioneta.pizzas) == 40)

    def test_ubicar_camionetas(self):
        self.dia.camionetas[0].ubicacion = [1, 1]
        self.assertTrue(self.dia.camionetas[0].ubicacion == [1, 1])
        self.dia.ubicar_camionetas()
        for camioneta in self.dia.camionetas:
            self.assertTrue(camioneta.ubicacion == [0, 0])

    def test_generar_pedidos(self):
        pedidos_en_hora = self.dia.generar_pedidos_en_hora(1)
        self.assertFalse(len(pedidos_en_hora) == 0)

        pedidos = self.dia.generar_pedidos()
        self.assertFalse(len(pedidos) == 0)

    def test_obtener_cliente_de_la_cola(self):

        cliente = self.dia.obtener_cliente_de_cola()
        self.assertTrue(cliente is None)
        evento = LlamoClienteEvent(1, self.dia)
        evento.attach(EncolarCliente())
        evento.attach(RechazarPedido())
        evento.notify()

        cliente2 = self.dia.obtener_cliente_de_cola()
        if evento.cliente_esta_en_rango():
            self.assertFalse(cliente2 is None)
            self.assertIsInstance(cliente2, LlamoClienteEvent)
        else:
            self.assertEqual(1, self.dia.pedidos_rechazados)

    def test_hay_camionetas_disponibles(self):

        for camioneta in self.dia.camionetas:
            self.assertTrue(camioneta.disponible)
        self.assertTrue(self.dia.hay_camionetas_disponibles())

        for camioneta in self.dia.camionetas:
            camioneta.disponible = False

        for camioneta in self.dia.camionetas:
            self.assertFalse(camioneta.disponible)
        self.assertFalse(self.dia.hay_camionetas_disponibles())

    def test_obtener_eventos_de_ahora(self):
        eventos_de_ahora = self.dia.obtener_eventos_de_ahora()
        self.assertTrue(len(eventos_de_ahora) == 0)

        tiempo_actual = 30
        for i in range(4):
            evento = LlamoClienteEvent(tiempo_actual)
            evento.hora = tiempo_actual
            self.dia.fel.append(evento)

        self.dia.tiempo_actual = tiempo_actual

        eventos_de_ahora = self.dia.obtener_eventos_de_ahora()
        self.assertTrue(len(eventos_de_ahora) == 4)


if __name__ == '__main__':
    unittest.main()
