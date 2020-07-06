import unittest

from Simulacion import Simulacion
from events.LlamoClienteEvent import LlamoClienteEvent
from events.PizzaVenceEvent import PizzaVenceEvent
from models.Camioneta import Camioneta
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.actividades.EncolarPedido import EncolarPedido
from models.actividades.RechazarPedido import RechazarPedido
from datetime import timedelta

from utils.utils import Utils


class TestableUtils(Utils):

    def set_en_rango(self, en_rango):
        self.en_rango = en_rango

    def generar_ubicacion_cliente(self):
        if self.en_rango:
            return [1414, 1414]
        return [1415, 1415]


class TestableSimulacion(Simulacion):

    def __init__(self):
        super().__init__()
        self.utils = TestableUtils()

    CANTIDAD_DE_EXPERIMENTOS = 1

    def iniciar_dia(self):
        pass

    def cargar_camionetas(self):
        pass

    def ubicar_camionetas(self):
        pass

    @property
    def dias_a_simular(self):
        return 1


class SimulacionFunctionalTest(unittest.TestCase):

    def test_debe_rechazarse_un_pedido_cuando_cliente_no_esta_en_rango(self):
        simulacion = self.get_simulacion()
        simulacion.utils.set_en_rango(False)
        self.assertTrue(len(simulacion.pedidos) == 0)
        self.assertTrue(len(simulacion.pedidos_rechazados) == 0)

        evento = self.generar_evento(TipoPizza.ANANA)
        simulacion.add_event(evento)

        simulacion.run()

        self.assertFalse(simulacion.cliente_esta_en_rango(simulacion.pedidos_rechazados[0].ubicacion))
        self.assertTrue(len(simulacion.pedidos) == 0)
        self.assertFalse(len(simulacion.pedidos_rechazados) == 0)

    def test_debe_entregarse_una_pizza_cuando_cliente_esta_en_rango(self):
        simulacion = self.get_simulacion()
        simulacion.tiempo_actual = 120 # TODO : refactorizar este tiempo
        camioneta = simulacion.camionetas[0]
        camioneta.pizzas.append(Pizza(TipoPizza.ANANA))

        simulacion.utils.set_en_rango(True)
        evento = self.generar_evento(TipoPizza.ANANA)
        simulacion.add_event(evento)
        dia = simulacion

        pizza_vence_event = list(filter(lambda x: isinstance(x, PizzaVenceEvent), dia.fel))[0]
        self.assertIsInstance(pizza_vence_event, PizzaVenceEvent)
        self.assertTrue(len(camioneta.pizzas) == 1)
        self.assertTrue(len(simulacion.pedidos) == 0)

        simulacion.run()

        eventos = list(filter(lambda x: isinstance(x, PizzaVenceEvent), dia.fel))
        self.assertEqual(len(eventos), 0)
        self.assertTrue(len(camioneta.pizzas) == 0)
        self.assertTrue(len(simulacion.pedidos) == 1)
        self.assertTrue(simulacion.pedidos[0].entregado)
        self.assertTrue(camioneta.pedido_en_curso is None)

    def test_debe_asignar_el_pedido_a_la_camioneta_mas_cercana(self):
        simulacion = self.get_simulacion()
        simulacion.tiempo_actual = 120
        simulacion.camionetas.append(Camioneta())
        simulacion.camionetas.append(Camioneta())

        simulacion.camionetas[0].pizzas.append(Pizza(TipoPizza.ANANA))
        simulacion.camionetas[1].pizzas.append(Pizza(TipoPizza.ANANA))

        simulacion.utils.set_en_rango(True)
        evento = self.generar_evento(TipoPizza.ANANA)
        simulacion.camionetas[1].ubicacion = evento.pedido.ubicacion
        simulacion.add_event(evento)

        simulacion.run()
        algo = 1
        self.assertEqual(simulacion.camionetas[1], simulacion.pedidos[0].camioneta)
        self.assertTrue(simulacion.pedidos[0].entregado)

    @staticmethod
    def generar_evento(tipo_pizza):
        evento = LlamoClienteEvent(Simulacion().dia + timedelta(minutes=121))
        if tipo_pizza is not None:
            evento.tipo_pizza = tipo_pizza
        return evento.attach(RechazarPedido()).attach(EncolarPedido())

    def get_simulacion(self):
        simulacion = TestableSimulacion()
        self.clean_up(simulacion)
        simulacion.camionetas = [Camioneta()]
        return simulacion

    @staticmethod
    def clean_up(simulacion):
        simulacion.pedidos = []
        simulacion.pedidos_rechazados = []


if __name__ == '__main__':
    unittest.main()
