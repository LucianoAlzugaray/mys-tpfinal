import unittest

from Simulacion import Simulacion
from SimulacionExceptions.NoHayTipoPizzaEnCamionetaException import NoHayTipoPizzaEnCamionetaException
from models.Camioneta import Camioneta
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza


class CamionetaTest(unittest.TestCase):

    def setUp(self):
        self.camioneta = Camioneta()

    def test_tiene_tipo(self):
        self.camioneta.pizzas = []
        self.assertTrue(len(self.camioneta.pizzas) == 0)

        self.assertFalse(self.camioneta.tiene_tipo(TipoPizza.ANANA))

        pizza = Pizza(TipoPizza.ANANA)
        self.camioneta.pizzas.append(pizza)
        self.assertTrue(self.camioneta.tiene_tipo(TipoPizza.ANANA))

    def test_quitar_pizza(self):
        self.camioneta.cargar_pizzas()
        pizza = self.camioneta.pizzas[0]
        self.camioneta.quitar_pizza(pizza)
        self.assertTrue(len(self.camioneta.pizzas) == 39)

    def test_cargar_pizzas(self):
        self.assertIsInstance(self.camioneta, Camioneta)
        self.assertTrue(len(self.camioneta.pizzas) == 0)
        self.camioneta.cargar_pizzas()
        self.assertTrue(len(self.camioneta.pizzas) == 40)
        self.camioneta.pizzas = []
        self.assertTrue(len(self.camioneta.pizzas) == 0)
        self.camioneta.pizzas = [Pizza(TipoPizza.ANANA),
                                 Pizza(TipoPizza.ANANA),
                                 Pizza(TipoPizza.ANANA)]
        self.assertTrue(len(self.camioneta.pizzas) == 3)
        self.camioneta.cargar_pizzas()
        self.assertTrue(len(self.camioneta.pizzas) == 40)

    def test_sabe_reservar_una_pizza(self):
        cantidad_de_eventos = len(Simulacion().dia_actual.fel)
        self.camioneta = Camioneta()
        self.camioneta.pizzas.append(Pizza(TipoPizza.ANANA))
        self.assertEqual(cantidad_de_eventos + 1, len(Simulacion().dia_actual.fel))

        self.camioneta.reservar_pizza(TipoPizza.ANANA)
        self.assertEqual(len(self.camioneta.pizzas_reservadas), 1)

        self.assertRaises(NoHayTipoPizzaEnCamionetaException, self.camioneta.reservar_pizza, TipoPizza.MOZZARELLA)


if __name__ == '__main__':
    unittest.main()
