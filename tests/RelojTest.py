import unittest
from datetime import timedelta, datetime

from Simulacion import Simulacion


class RelojTest(unittest.TestCase):

    def test_something(self):

        simulacion = Simulacion()
        simulacion.iniciar_dia()
        dia_actual = simulacion.dia
        dt_una_hora = datetime.now()

        self.assertFalse(simulacion.reloj.termino_dia())
        self.assertFalse(simulacion.reloj.termino_horario_de_toma_de_pedido())
        self.assertIsInstance(simulacion.dia, datetime.now().__class__)

        simulacion.avanzar_reloj(15)
        self.assertEqual(simulacion.dia, dia_actual + timedelta(minutes=15))

        simulacion.reloj.dia = simulacion.reloj.dia.replace(minute=30, hour=23, second=0,
                                                            year=simulacion.reloj.dia.year,
                                                            month=simulacion.reloj.dia.month,
                                                            day=simulacion.reloj.dia.day)

        # self.assertTrue(simulacion.reloj.termino_dia())
        # self.assertTrue(simulacion.reloj.termino_horario_de_toma_de_pedido())

        dt_una_hora = dt_una_hora.replace(minute=20, hour=22, second=0, year=simulacion.reloj.dia.year,
                                          month=simulacion.reloj.dia.month, day=simulacion.reloj.dia.day)

        # self.assertEqual(simulacion.reloj.get_diferencia_hora_actual(dt_una_hora), 60)

if __name__ == '__main__':
    unittest.main()
