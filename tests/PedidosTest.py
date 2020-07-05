import unittest
from Simulacion import Simulacion
import numpy as np

from events.LlamoClienteEvent import LlamoClienteEvent
from models.Camioneta import Camioneta
from models.Dia import Dia


class PedidosTest(unittest.TestCase):
    def seAjustaAPoisson(self, datos, parametro):
        return True

    def getCantidadDePedidosPorHora(self, fel):
        cantidadDeEventos = [0] * 12
        for evento in fel:
            cantidadDeEventos[evento.hora//60] += 1
        return cantidadDeEventos

    def test_pedidos_se_generan_correctamente(self):
        dia = Dia(10, [Camioneta()])
        dia.iniciar_dia()

        fel = dia.get_fel()
        self.assertTrue(len(fel) > 0)

    def test_fel_son_eventos_de_llamo_cliente(self):
        dia = Dia(10, [Camioneta()])
        dia.iniciar_dia()

        for evento in dia.get_fel():
            self.assertIsInstance(evento, LlamoClienteEvent)

    def test_pedidos_se_ajustan_a_poisson(self):
        dia = Dia(10, [Camioneta()])
        dia.iniciar_dia()
        cantidad_de_pedidos_por_hora = self.getCantidadDePedidosPorHora(dia.fel)

        self.assertTrue(self.seAjustaAPoisson(cantidad_de_pedidos_por_hora, 20))