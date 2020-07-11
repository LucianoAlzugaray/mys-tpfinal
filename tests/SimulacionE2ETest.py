import unittest


class MyTestCase(unittest.TestCase):

    def test_something(self):
        from Simulacion import Simulacion
        from Configuracion import Configuracion

        simulacion = Simulacion()
        simulacion.configurate(Configuracion.get_default_configuration())

        simulacion.run()

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
