import unittest
from models.Dia import Dia


class DiaTestCase(unittest.TestCase):
    def test_something(self):

        dia = Dia(10, 4)
        self.assertIsInstance(dia, Dia)

        pedidos_en_hora = dia.generar_pedidos_en_hora(1)
        self.assertFalse(len(pedidos_en_hora) == 0)

        pedidos = dia.generar_pedidos()
        self.assertFalse(len(pedidos) == 0)

        dia.cargar_camionetas()
        for camioneta in dia.camionetas:
            self.assertTrue(len(camioneta.pizzas) == 40)


if __name__ == '__main__':
    unittest.main()
