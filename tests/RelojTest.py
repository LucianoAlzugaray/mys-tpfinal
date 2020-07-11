import unittest

from Configuracion import Configuracion
from Simulacion import Simulacion


class RelojTest(unittest.TestCase):

    def test_debe_inicializarse_segun_el_timestamp_de_la_configuracion_de_la_simulacion(self):
        simulacion = Simulacion()
        simulacion.configurate(Configuracion.get_default_configuration())
        self.assertEqual(simulacion.tiempo_inicio, simulacion.reloj.dia)


if __name__ == '__main__':
    unittest.main()
