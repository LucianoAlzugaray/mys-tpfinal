import unittest
from models.Camioneta import Camioneta
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.camioneta = Camioneta()

    def test_tiene_tipo(self):

        self.camioneta.pizzas = []
        self.assertTrue(len(self.camioneta.pizzas) == 0)

        self.assertFalse(self.camioneta.tiene_tipo(TipoPizza.ANANA))

        pizza = Pizza(TipoPizza.ANANA, 10)
        self.camioneta.pizzas.append(pizza)
        self.assertTrue(self.camioneta.tiene_tipo(TipoPizza.ANANA))

    def test_quitar_pizza(self):
        self.camioneta.cargar_pizzas(10, [])
        pizza = self.camioneta.pizzas[0]
        self.camioneta.quitar_pizza(pizza)
        self.assertTrue(len(self.camioneta.pizzas) == 39)

    def test_cargar_pizzas(self):
        self.assertIsInstance(self.camioneta, Camioneta)
        self.assertTrue(len(self.camioneta.pizzas) == 0)
        self.camioneta.cargar_pizzas(10, [])
        self.assertTrue(len(self.camioneta.pizzas) == 40)
        self.camioneta.pizzas = []
        self.assertTrue(len(self.camioneta.pizzas) == 0)
        self.camioneta.pizzas = [Pizza(TipoPizza.ANANA, 10),
                                 Pizza(TipoPizza.ANANA, 10),
                                 Pizza(TipoPizza.ANANA, 10)]
        self.assertTrue(len(self.camioneta.pizzas) == 3)
        self.camioneta.cargar_pizzas(10, [])
        self.assertTrue(len(self.camioneta.pizzas) == 40)


if __name__ == '__main__':
    unittest.main()
