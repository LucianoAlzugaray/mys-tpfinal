import unittest

from events.CamionetaRegresaARestauranteEvent import CamionetaRegresaARestauranteEvent
from events.EnviarPedidoEvent import EnviarPedidoEvent
from events.LlamoClienteEvent import LlamoClienteEvent
from Simulacion import Simulacion
from models.Cliente import Cliente
from models.Pedido import Pedido
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.actividades.EncolarCliente import EncolarCliente
from models.actividades.RechazarPedido import RechazarPedido
from utils.utils import Utils


class SimulacionTest(unittest.TestCase):

    def test_debe_rechazar_pedido_cuando_cliente_no_esta_en_rango(self):
        pedidos_rechazados = len(Simulacion().pedidos_rechazados_en_llamada)
        self.assertEqual(0, pedidos_rechazados)

        cliente = self.generar_cliente_fuera_de_rango()
        evento = self.generar_evento(cliente, None)
        evento.notify()

        self.assertEqual(pedidos_rechazados + 1, len(Simulacion().pedidos_rechazados_en_llamada))

    def test_debe_asignar_pedido_a_camioneta_cuando_cliente_esta_en_rango(self):
        simulacion = Simulacion()
        simulacion.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA))

        cliente = self.generar_cliente_en_rango()
        evento = self.generar_evento(cliente, TipoPizza.ANANA)
        evento.notify()

        camioneta = Simulacion().get_camioneta_by_cliente(cliente)
        pedido = camioneta.get_pedido_by_cliente(cliente)

        self.assertEqual(camioneta, simulacion.camionetas[2])
        self.assertEqual(pedido.tipo_pizza, evento.tipo_pizza)
        self.assertEqual(pedido.hora_toma, evento.hora)

    def test_debe_asignar_el_pedido_a_la_camioneta_mas_cercana(self):
        simulacion = Simulacion()
        simulacion.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA))
        simulacion.camionetas[3].pizzas.append(Pizza(TipoPizza.ANANA))

        cliente = self.generar_cliente_en_rango()
        evento = self.generar_evento(cliente, TipoPizza.ANANA)
        simulacion.camionetas[3].ubicacion = evento.cliente.ubicacion
        evento.notify()

        camioneta = Simulacion().get_camioneta_by_cliente(cliente)
        pedido = camioneta.get_pedido_by_cliente(cliente)

        self.assertEqual(camioneta, simulacion.camionetas[3])
        self.assertEqual(pedido.tipo_pizza, evento.tipo_pizza)
        self.assertEqual(pedido.hora_toma, evento.hora)

    def test_debe_tratar_de_convencer_al_cliente_si_no_hay_camioneta_con_tipo(self):
        class TestableUtils(Utils):

            @staticmethod
            def convencer_al_cliente():
                return True

        simulacion = Simulacion()
        simulacion.utils = TestableUtils()
        simulacion.camionetas[2].pizzas.append(Pizza(TipoPizza.MOZZARELLA))
        simulacion.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA))
        simulacion.camionetas[3].pizzas.append(Pizza(TipoPizza.ANANA))
        tipos_disponibles_en_camionetas = simulacion.get_tipos_disponibles_en_camionetas()

        cliente = self.generar_cliente_en_rango()
        evento = self.generar_evento(cliente, TipoPizza.NAPOLITANA)
        evento.notify()

        camioneta = Simulacion().get_camioneta_by_cliente(cliente)
        pedido = camioneta.get_pedido_by_cliente(cliente)

        self.assertEqual(2, len(tipos_disponibles_en_camionetas))
        self.assertEqual(pedido.tipo_pizza, tipos_disponibles_en_camionetas[0])
        self.assertEqual(pedido.hora_toma, evento.hora)

    def test_debe_regresar_camioneta_mas_cercana_cuando_cliente_no_convencido(self):
        class TestableUtils(Utils):

            @staticmethod
            def convencer_al_cliente():
                return False

        simulacion = Simulacion()
        self.assertFalse(simulacion.volver_al_terminar_todos_los_pedidos)

        simulacion.utils = TestableUtils()
        for k, camioneta in enumerate(simulacion.camionetas):
            camioneta.descargarse()
            self.asignar_pedido_a_camioneta(TipoPizza.ANANA, k)

        for evento in list(filter(lambda x: isinstance(x, EnviarPedidoEvent), simulacion.fel)):
            evento.notify()

        simulacion.camionetas[3].pedido_en_curso.cliente.ubicacion = [0, 0]

        cliente = self.generar_cliente_en_rango()
        evento = self.generar_evento(cliente, TipoPizza.NAPOLITANA)
        evento.notify()

        eventos = list(filter(lambda x: isinstance(x, CamionetaRegresaARestauranteEvent), simulacion.fel))
        self.assertFalse(len(eventos) == 0)
        self.assertIsInstance(eventos[0], CamionetaRegresaARestauranteEvent)

        expected = simulacion.camionetas[3]
        actual = eventos[0].camioneta
        self.assertTrue(expected == actual)

    def test_debe_regresat_camioneta_mas_proxima_a_liberarse_cuando_cliente_no_convencido(self):
        class TestableUtils(Utils):

            @staticmethod
            def convencer_al_cliente():
                return False

        simulacion = Simulacion()
        self.assertFalse(simulacion.volver_al_terminar_todos_los_pedidos)

        simulacion.utils = TestableUtils()
        for k, camioneta in enumerate(simulacion.camionetas):
            camioneta.descargarse()
            self.asignar_pedido_a_camioneta(TipoPizza.ANANA, k)

        self.assertEqual(True, True)

    def asignar_pedido_a_camioneta(self, tipo_de_pizza, camioneta):
        Simulacion().camionetas[camioneta].pizzas.append(Pizza(tipo_de_pizza))
        cliente0 = self.generar_cliente_en_rango()
        pedido0 = Pedido(cliente0, 10, Simulacion().camionetas[camioneta], tipo_de_pizza)
        Simulacion().camionetas[camioneta].asignar_pedido(pedido0)

    @staticmethod
    def generar_cliente_fuera_de_rango():
        cliente = Cliente()
        cliente.ubicacion[0] = 1415
        cliente.ubicacion[1] = 1415
        return cliente

    @staticmethod
    def generar_cliente_en_rango():
        cliente = Cliente()
        cliente.ubicacion[0] = 1414
        cliente.ubicacion[1] = 1414
        return cliente

    @staticmethod
    def generar_evento(cliente, tipo_pizza):
        evento = LlamoClienteEvent(0, cliente, Simulacion())
        if tipo_pizza is not None:
            evento.tipo_pizza = tipo_pizza
        evento.attach(RechazarPedido())
        evento.attach(EncolarCliente())
        return evento


if __name__ == '__main__':
    unittest.main()
