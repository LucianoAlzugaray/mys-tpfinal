import unittest
from models.Camioneta import Camioneta
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza


class MyTestCase(unittest.TestCase):
    def test_something(self):

        camioneta = Camioneta()
        self.assertIsInstance(camioneta, Camioneta)
        self.assertTrue(len(camioneta.pizzas) == 0)
        camioneta.cargar_pizzas(10, [])
        self.assertTrue(len(camioneta.pizzas) == 40)

        camioneta.pizzas = []
        self.assertTrue(len(camioneta.pizzas) == 0)

        camioneta.pizzas = [Pizza(TipoPizza.ANANA, 10),
                            Pizza(TipoPizza.ANANA, 10),
                            Pizza(TipoPizza.ANANA, 10)]

        self.assertTrue(len(camioneta.pizzas) == 3)

        camioneta.cargar_pizzas(10, [])
        self.assertTrue(len(camioneta.pizzas) == 40)


if __name__ == '__main__':
    unittest.main()
