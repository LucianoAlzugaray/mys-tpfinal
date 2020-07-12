import unittest


class MyTestCase(unittest.TestCase):

    def test_simulacion(self):
        from Simulacion import Simulacion
        from Configuracion import Configuracion

        simulacion = Simulacion()
        simulacion.configurate(Configuracion.get_default_configuration())

        simulacion.run()

        self.assertEqual(True, True)


    def test_asd(self):
        from models.Cliente import Cliente
        cliente = Cliente()
        asd = cliente.__dict__
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
