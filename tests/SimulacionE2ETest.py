import unittest

from Configuracion import Configuracion
from utils.utils import Utils
from  main import iniciar_simulacion

class MyTestCase(unittest.TestCase):

    def test_simulacion(self):
        from Simulacion import Simulacion
        from Configuracion import Configuracion

        simulacion = Simulacion()
        simulacion.configurate(Configuracion.get_default_configuration())

        simulacion.run()

        self.assertEqual(True, True)

    def test_iniciar_simulacion(self):
        from Simulacion import Simulacion
        from Configuracion import Configuracion
        configuracion = {'inicio': 1593804446561, 'fin': 1593907973714, 'volverAlRestaurante': None, 'pedidosPorHora': 10, 'hornosPorCamioneta': 1, 'pizzasPorHorno': 5, 'cantidadCamionetas': 2, 'anana': None, 'napolitana': None, 'fugazzeta': None, 'mozzarella': None, 'calabresa': None, 'cantidadExperimentos': 1, 'nombreExperimento': 'Nombre', 'rangoAtencion': None}
        #configuracion = {'inicio': None, 'fin': None, 'volverAlRestaurante': None, 'pedidosPorHora': None, 'hornosPorCamioneta': None, 'pizzasPorHorno': None, 'cantidadCamionetas': None, 'anana': None, 'napolitana': None, 'fugazzeta': None, 'mozzarella': False, 'calabresa': None, 'cantidadExperimentos': None, 'nombreExperimento': None, 'rangoAtencion': None}

        iniciar_simulacion(configuracion)


        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()