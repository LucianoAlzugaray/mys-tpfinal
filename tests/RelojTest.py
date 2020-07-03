import unittest
from datetime import timedelta, datetime

from Simulacion import Simulacion


class MyTestCase(unittest.TestCase):

    def test_something(self):

        simulacion = Simulacion()
        simulacion.iniciar_dia()
        dia_actual = simulacion.dia

        self.assertIsInstance(simulacion.dia, datetime.now().__class__)
        simulacion.avanzar_reloj(15)
        self.assertEqual(simulacion.dia, dia_actual + timedelta(minutes=15))


if __name__ == '__main__':
    unittest.main()
