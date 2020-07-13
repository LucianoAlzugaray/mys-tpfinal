import unittest

from exeptions.NoHayTipoPizzaEnCamionetaException import NoHayTipoPizzaEnCamionetaException
from models.Camioneta import Camioneta
from models.Cliente import Cliente
from models.Pedido import Pedido
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza


class CamionetaTest(unittest.TestCase):

    def setUp(self):
        self.camioneta = Camioneta()

    def test_tiene_tipo(self):
        simulacion = self.get_simulacion()
        self.camioneta.pizzas = []
        self.assertTrue(len(self.camioneta.pizzas) == 0)

        self.assertFalse(self.camioneta.tiene_tipo(TipoPizza.ANANA))

        simulacion = self.get_simulacion()
        pizza = simulacion.generar_pizza(TipoPizza.ANANA)
        self.camioneta.pizzas.append(pizza)
        self.assertTrue(self.camioneta.tiene_tipo(TipoPizza.ANANA))

    def test_quitar_pizza(self):
        self.get_simulacion()
        self.camioneta.cargar_pizzas()
        pizza = self.camioneta.pizzas[0]
        self.camioneta.quitar_pizza(pizza)
        self.assertTrue(len(self.camioneta.pizzas) == 39)

    def test_cargar_pizzas(self):
        self.get_simulacion()
        self.assertIsInstance(self.camioneta, Camioneta)
        self.assertTrue(len(self.camioneta.pizzas) == 0)
        self.camioneta.cargar_pizzas()
        self.assertTrue(len(self.camioneta.pizzas) == 40)
        self.camioneta.pizzas = []
        self.assertTrue(len(self.camioneta.pizzas) == 0)
        self.camioneta.pizzas = [Pizza(TipoPizza.ANANA, None),
                                 Pizza(TipoPizza.ANANA, None),
                                 Pizza(TipoPizza.ANANA, None)]
        self.assertTrue(len(self.camioneta.pizzas) == 3)
        self.camioneta.cargar_pizzas()
        self.assertEqual(40, len(self.camioneta.pizzas))

    def get_simulacion(self):
        from Simulacion import Simulacion
        from Configuracion import Configuracion
        configuracion = Configuracion.get_default_configuration()
        simulacion = Simulacion()
        simulacion.configurate(configuracion)
        return simulacion


if __name__ == '__main__':
    unittest.main()
