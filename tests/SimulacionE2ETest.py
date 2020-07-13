import unittest

from Configuracion import Configuracion
from utils.utils import Utils


class MyTestCase(unittest.TestCase):

    def test_simulacion(self):
        from Simulacion import Simulacion
        from Configuracion import Configuracion

        simulacion = Simulacion()
        simulacion.configurate(Configuracion.get_default_configuration())

        simulacion.run()

        self.assertEqual(True, True)



if __name__ == '__main__':
    unittest.main()
