import unittest

from Simulacion import Simulacion
from events.LlamoClienteEvent import LlamoClienteEvent
from events.PizzaVenceEvent import PizzaVenceEvent
from models.Camioneta import Camioneta
from models.Cliente import Cliente
from models.Dia import Dia
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.actividades.EncolarCliente import EncolarCliente
from models.actividades.RechazarPedido import RechazarPedido
from datetime import timedelta

class TestableSimulation(Simulacion):

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
        evento = self.generar_evento(cliente, TipoPizza.ANANA)
        simulacion.add_event(evento)

        simulacion.run()

        self.assertTrue(len(simulacion.pedidos) == 0)
        self.assertFalse(len(simulacion.clientes_rechazados) == 0)
        self.assertFalse(simulacion.cliente_esta_en_rango(simulacion.clientes_rechazados[0]))

    def test_debe_entregarse_una_pizza_cuando_cliente_esta_en_rango(self):

        simulacion = self.get_simulacion()
        simulacion.tiempo_actual = 120
        camioneta = simulacion.camionetas[0]
        camioneta.pizzas.append(Pizza(TipoPizza.ANANA))

        cliente = self.generar_cliente_en_rango()
        evento = self.generar_evento(cliente, TipoPizza.ANANA)
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

        simulacion.camionetas[0].pizzas.append(Pizza(TipoPizza.ANANA))
        simulacion.camionetas[1].pizzas.append(Pizza(TipoPizza.ANANA))

        cliente = self.generar_cliente_en_rango()
        simulacion.camionetas[1].ubicacion = cliente.ubicacion

        evento = self.generar_evento(cliente, TipoPizza.ANANA)
        simulacion.add_event(evento)

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
        evento = LlamoClienteEvent((Simulacion().dia + timedelta(121)).time, cliente, )
        if tipo_pizza is not None:
            evento.tipo_pizza = tipo_pizza
        evento.attach(RechazarPedido())
        evento.attach(EncolarCliente())
        return evento

    def get_simulacion(self):
        simulacion = TestableSimulation()
        self.clean_up(simulacion)
        simulacion.dias_a_simular = 1
        simulacion.experimentos = 1
        simulacion.camionetas = [Camioneta()]
        return simulacion

    @staticmethod
    def clean_up(simulacion):
        simulacion.pedidos = []
        simulacion.clientes_rechazados = []
        simulacion.dias_corridos = []

if __name__ == '__main__':
    unittest.main()
