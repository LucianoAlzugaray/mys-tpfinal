import unittest
from datetime import timedelta
from Simulacion import Simulacion
from events.PizzaVenceEvent import PizzaVenceEvent
from models.Camioneta import Camioneta
from models.Cliente import Cliente
from models.EventTypeEnum import EventTypeEnum
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from utils.utils import Utils


class TestableUtils(Utils):
    en_rango = True

    def set_en_rango(self, en_rango):
        self.en_rango = en_rango

    def generar_ubicacion_cliente(self):
        if self.en_rango:
            return [1414, 1414]
        return [1415, 1415]


class TestableSimulacion(Simulacion):

    CANTIDAD_DE_EXPERIMENTOS = 1

    def __init__(self):
        super().__init__()
        self.utils = TestableUtils()

    def iniciar_dia(self):
        pass

    def cargar_camionetas(self):
        pass

    def ubicar_camionetas(self):
        pass


class SimulacionFunctionalTest(unittest.TestCase):

    def test_debe_rechazarse_un_pedido_cuando_cliente_no_esta_en_rango(self):
        simulacion = self.get_simulacion()

        cliente = self.generar_cliente_fuera_de_rango()
        self.generar_evento(cliente, TipoPizza.ANANA)

        simulacion.run()

        self.assertTrue(len(simulacion.pedidos) == 0)
        self.assertFalse(len(simulacion.clientes_rechazados) == 0)
        self.assertFalse(simulacion.cliente_esta_en_rango(simulacion.clientes_rechazados[0]))

    def test_debe_entregarse_una_pizza_cuando_cliente_esta_en_rango(self):

        simulacion = self.get_simulacion()
        camioneta = simulacion.camionetas[0]
        pizza = simulacion.generar_pizza(TipoPizza.ANANA)
        camioneta.pizzas.append(pizza)

        cliente = self.generar_cliente_en_rango()
        self.generar_evento(cliente, TipoPizza.ANANA)

        pizza_vence_event = list(filter(lambda x: isinstance(x, PizzaVenceEvent), simulacion.fel))[0]
        self.assertIsInstance(pizza_vence_event, PizzaVenceEvent)
        self.assertTrue(len(camioneta.pizzas) == 1)
        self.assertTrue(len(simulacion.pedidos) == 0)

        simulacion.run()

        eventos = list(filter(lambda x: isinstance(x, PizzaVenceEvent), simulacion.fel))
        self.assertEqual(len(eventos), 0)
        self.assertTrue(len(camioneta.pizzas) == 0)
        self.assertTrue(len(simulacion.pedidos) == 1)
        self.assertTrue(simulacion.pedidos[0].entregado)
        self.assertTrue(camioneta.pedido_en_curso is None)

    def test_debe_asignar_el_pedido_a_la_camioneta_mas_cercana(self):

        simulacion = self.get_simulacion()
        simulacion.camionetas.append(Camioneta())

        simulacion.camionetas[0].pizzas.append(Pizza(TipoPizza.ANANA, simulacion.dia))
        simulacion.camionetas[1].pizzas.append(Pizza(TipoPizza.ANANA, simulacion.dia))

        cliente = self.generar_cliente_en_rango()
        simulacion.camionetas[1].ubicacion = cliente.ubicacion

        self.generar_evento(cliente, TipoPizza.ANANA)

        simulacion.run()

        self.assertEqual(simulacion.camionetas[1], simulacion.pedidos[0].camioneta)
        self.assertTrue(simulacion.pedidos[0].entregado)

    @staticmethod
    def generar_cliente_en_rango():
        cliente = Cliente()
        cliente.ubicacion[0] = 1414
        cliente.ubicacion[1] = 1414
        return cliente

    @staticmethod
    def generar_cliente_fuera_de_rango():
        cliente = Cliente()
        cliente.ubicacion[0] = 1415
        cliente.ubicacion[1] = 1415
        return cliente

    @staticmethod
    def generar_evento(cliente, tipo_pizza):
        simulacion = Simulacion()
        hora = simulacion.TIEMPO_INICIO + timedelta(minutes=5)
        kwargs = {'hora': hora, 'cliente': cliente, 'tipo_pizza': tipo_pizza}
        simulacion.add_event(EventTypeEnum.LLAMO_CLIENTE, kwargs)

    def get_simulacion(self):
        simulacion = TestableSimulacion()
        simulacion.reloj.dia = Simulacion.TIEMPO_INICIO
        simulacion.fel = []
        simulacion.camionetas = []
        simulacion.pedidos = []
        simulacion.clientes_rechazados = []
        simulacion.dias_corridos = []
        simulacion.dias_a_simular = 1
        simulacion.experimentos = 1
        simulacion.camionetas = [Camioneta()]
        return simulacion


if __name__ == '__main__':
    unittest.main()
