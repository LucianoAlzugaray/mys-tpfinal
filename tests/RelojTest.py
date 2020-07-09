import unittest
from Simulacion import Simulacion


# TODO: ver aserts de isInstance reloj.dia = datetime, y metodo reloj.get_diferencia_hora_actual
class RelojTest(unittest.TestCase):

    def test_debe_inicializarse_segun_el_timestamp_de_la_configuracion_de_la_simulacion(self):
        simulacion = Simulacion()
        self.assertEqual(simulacion.tiempo_inicio, simulacion.reloj.dia)

    # TODO: renombrar
    def test_debe_terminar_el_dia_corectamente(self):
        simulacion = Simulacion()

        self.assertFalse(simulacion.reloj.termino_dia())
        self.assertFalse(simulacion.reloj.termino_horario_de_toma_de_pedido())
        simulacion.avanzar_reloj(simulacion.CANTIDAD_MINUTOS_LABORALES)
        self.assertTrue(simulacion.termino_dia())
        self.assertTrue(simulacion.reloj.termino_horario_de_toma_de_pedido())


if __name__ == '__main__':
    unittest.main()
