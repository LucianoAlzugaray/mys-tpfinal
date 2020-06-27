import unittest
from events.LlamoClienteEvent import LlamoClienteEvent
from models.Camioneta import Camioneta
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza


class LlamoClienteEventTest(unittest.TestCase):

    def setUp(self):
        self.evento = LlamoClienteEvent(10)
        self.camionetas = [Camioneta() for i in range(4)]

    def test_camionetas_con_pizza_pedida(self):
        for k, v in enumerate(self.camionetas):
            if k % 2 == 0:
                self.camionetas[k].pizzas.append(Pizza(TipoPizza.ANANA))
        camionetas_con_pizza_pedida = self.evento.camionetas_con_pizza_pedida(TipoPizza.ANANA, self.camionetas)
        self.assertTrue(len(camionetas_con_pizza_pedida) == 2)
        for camioneta in camionetas_con_pizza_pedida:
            pizzas = list(filter(lambda x: x.tipo == TipoPizza.ANANA, camioneta.pizzas))
            self.assertTrue(len(pizzas) > 0)

    def test_obtener_camionestas_disponibles(self):
        for camioneta in self.camionetas:
            camioneta.disponible = False
        self.assertTrue(len(self.evento.obtener_camionetas_disponibles(self.camionetas)) == 0)
        for camioneta in self.camionetas:
            camioneta.disponible = True
        self.assertTrue(len(self.evento.obtener_camionetas_disponibles(self.camionetas)) == 4)

    def test_cliente_esta_en_rango(self):

        self.evento.ubicacion[0] = 1415
        self.evento.ubicacion[1] = 1415
        self.assertFalse(self.evento.cliente_esta_en_rango())

        self.evento.ubicacion[0] = 1414
        self.evento.ubicacion[1] = 1414
        self.assertTrue(self.evento.cliente_esta_en_rango())


if __name__ == '__main__':
    unittest.main()
