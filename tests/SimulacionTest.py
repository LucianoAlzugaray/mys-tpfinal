import unittest

from events.CamionetaRegresaARestauranteEvent import CamionetaRegresaARestauranteEvent
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
        pedidos_rechazados = len(Simulacion().pedidos_rechazados)
        self.assertEqual(0, pedidos_rechazados)

        cliente = self.generar_cliente_fuera_de_rango()
        evento = LlamoClienteEvent(0, cliente, Simulacion().dia_actual)
        evento.attach(RechazarPedido())
        evento.attach(EncolarCliente())
        evento.notify()

        self.assertEqual(pedidos_rechazados + 1, len(Simulacion().pedidos_rechazados))

    def test_debe_asignar_pedido_a_camioneta_cuando_cliente_esta_en_rango(self):
        simulacion = Simulacion()
        simulacion.dia_actual.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA))

        cliente = self.generar_cliente_en_rango()
        evento = LlamoClienteEvent(0, cliente, Simulacion().dia_actual)
        evento.tipo_pizza = TipoPizza.ANANA
        evento.attach(RechazarPedido())
        evento.attach(EncolarCliente())
        evento.notify()

        # hay una camioneta con un pedido asignado al cliente.
        camioneta = Simulacion().get_camioneta_by_cliente(cliente)
        self.assertEqual(camioneta, simulacion.dia_actual.camionetas[2])
        pedido = camioneta.get_pedido_by_cliente(cliente)
        self.assertEqual(pedido.pizza.tipo, evento.tipo_pizza)
        self.assertEqual(pedido.hora_toma, evento.hora)

    def test_debe_asignar_el_pedido_a_la_camioneta_mas_cercana(self):
        simulacion = Simulacion()
        simulacion.dia_actual.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA))
        simulacion.dia_actual.camionetas[3].pizzas.append(Pizza(TipoPizza.ANANA))

        cliente = self.generar_cliente_en_rango()
        evento = LlamoClienteEvent(0, cliente, Simulacion().dia_actual)
        evento.tipo_pizza = TipoPizza.ANANA
        simulacion.dia_actual.camionetas[3].ubicacion = evento.cliente.ubicacion
        evento.attach(RechazarPedido())
        evento.attach(EncolarCliente())
        evento.notify()

        camioneta = Simulacion().get_camioneta_by_cliente(cliente)
        self.assertEqual(camioneta, simulacion.dia_actual.camionetas[3])
        pedido = camioneta.get_pedido_by_cliente(cliente)
        self.assertEqual(pedido.pizza.tipo, evento.tipo_pizza)
        self.assertEqual(pedido.hora_toma, evento.hora)

    def test_debe_tratar_de_convencer_al_cliente_si_no_hay_camioneta_con_tipo(self):
        class TestableUtils(Utils):

            @staticmethod
            def convencer_al_cliente():
                return True

        simulacion = Simulacion()
        simulacion.utils = TestableUtils()
        simulacion.dia_actual.camionetas[2].pizzas.append(Pizza(TipoPizza.MOZZARELLA))
        simulacion.dia_actual.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA))
        simulacion.dia_actual.camionetas[3].pizzas.append(Pizza(TipoPizza.ANANA))
        tipos_disponibles_en_camionetas = simulacion.get_tipos_disponibles_en_camionetas()

        cliente = self.generar_cliente_en_rango()
        evento = LlamoClienteEvent(0, cliente, Simulacion().dia_actual)
        evento.tipo_pizza = TipoPizza.NAPOLITANA
        evento.attach(RechazarPedido())
        evento.attach(EncolarCliente())
        evento.notify()

        camioneta = Simulacion().get_camioneta_by_cliente(cliente)
        pedido = camioneta.get_pedido_by_cliente(cliente)

        self.assertEqual(2, len(tipos_disponibles_en_camionetas))
        self.assertEqual(pedido.pizza.tipo, tipos_disponibles_en_camionetas[0])
        self.assertEqual(pedido.hora_toma, evento.hora)

    def test_debe_regresar_camioneta_mas_cercana_cuando_cliente_no_convencido(self):
        class TestableUtils(Utils):

            @staticmethod
            def convencer_al_cliente():
                return False

        simulacion = Simulacion()
        simulacion.utils = TestableUtils()

        for camioneta in simulacion.dia_actual.camionetas:
            camioneta.descargarse()

        simulacion.dia_actual.camionetas[0].pizzas.append(Pizza(TipoPizza.ANANA))
        simulacion.dia_actual.camionetas[1].pizzas.append(Pizza(TipoPizza.ANANA))
        simulacion.dia_actual.camionetas[2].pizzas.append(Pizza(TipoPizza.MOZZARELLA))
        simulacion.dia_actual.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA))
        simulacion.dia_actual.camionetas[3].pizzas.append(Pizza(TipoPizza.ANANA))

        cliente0 = Cliente()
        cliente0.ubicacion = [1414, 1414]

        cliente1 = Cliente()
        cliente1.ubicacion = [1414, 1414]

        cliente2 = Cliente()
        cliente2.ubicacion = [1414, 1414]

        cliente3 = Cliente()
        cliente3.ubicacion = [0, 0]

        pedido0 = Pedido(cliente0, 10, simulacion.dia_actual.camionetas[0], Pizza(TipoPizza.ANANA))
        pedido1 = Pedido(cliente1, 10, simulacion.dia_actual.camionetas[1], Pizza(TipoPizza.ANANA))
        pedido2 = Pedido(cliente2, 10, simulacion.dia_actual.camionetas[2], Pizza(TipoPizza.ANANA))
        pedido3 = Pedido(cliente3, 10, simulacion.dia_actual.camionetas[3], Pizza(TipoPizza.ANANA))

        simulacion.dia_actual.camionetas[0].asignar_pedido(pedido0)
        simulacion.dia_actual.camionetas[1].asignar_pedido(pedido1)
        simulacion.dia_actual.camionetas[2].asignar_pedido(pedido2)
        simulacion.dia_actual.camionetas[3].asignar_pedido(pedido3)

        cliente = self.generar_cliente_en_rango()
        evento = LlamoClienteEvent(0, cliente, Simulacion().dia_actual)
        evento.tipo_pizza = TipoPizza.NAPOLITANA
        evento.attach(RechazarPedido())
        evento.attach(EncolarCliente())
        evento.notify()

    #     en la fel del dia haya un evento de CamionetaRegrasaARestaurante
    #         que la camioneta sea la mas cercana al restaurante
    #         que la hora del evento sea la correcta

    #         que la camioneta del evento tenga un pedido para el cliente

        eventos = list(filter(lambda x: isinstance(x, CamionetaRegresaARestauranteEvent), simulacion.dia_actual.fel))
        self.assertFalse(len(eventos) == 0)
        self.assertIsInstance(eventos[0], CamionetaRegresaARestauranteEvent)

        expected = simulacion.dia_actual.camionetas[3]
        actual = eventos[0].camioneta
        self.assertTrue(expected == actual)

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


if __name__ == '__main__':
    unittest.main()
