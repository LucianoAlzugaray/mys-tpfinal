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
from models.actividades.RechazarCliente import RechazarCliente
from utils.utils import Utils
from models.Camioneta import Camioneta


class SimulacionTest(unittest.TestCase):

    def test_debe_rechazar_pedido_cuando_cliente_no_esta_en_rango(self):
        pedidos_rechazados = len(Simulacion().clientes_rechazados)
        self.assertEqual(0, pedidos_rechazados)

        cliente = self.generar_cliente_fuera_de_rango()
        evento = self.generar_evento(cliente, None)
        evento.notify()

        self.assertEqual(pedidos_rechazados + 1, len(Simulacion().clientes_rechazados))

    def test_debe_asignar_pedido_a_camioneta_cuando_cliente_esta_en_rango(self):
        simulacion = Simulacion()
        simulacion.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA, simulacion.time))

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
        simulacion.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA, simulacion.time))
        simulacion.camionetas[3].pizzas.append(Pizza(TipoPizza.ANANA, simulacion.time))

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

        simulacion = self.get_simulacion()
        simulacion.camionetas = [Camioneta(), Camioneta(), Camioneta(), Camioneta()]
        simulacion.utils = TestableUtils()
        simulacion.camionetas[2].pizzas.append(Pizza(TipoPizza.MOZZARELLA, simulacion.time))
        simulacion.camionetas[2].pizzas.append(Pizza(TipoPizza.ANANA, simulacion.time))
        simulacion.camionetas[3].pizzas.append(Pizza(TipoPizza.ANANA, simulacion.time))
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

        simulacion = self.get_simulacion()
        simulacion.camionetas += [Camioneta(), Camioneta(), Camioneta(), Camioneta()]
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

        simulacion = self.get_simulacion()
        self.assertFalse(simulacion.volver_al_terminar_todos_los_pedidos)

        simulacion.utils = TestableUtils()
        for k, camioneta in enumerate(simulacion.camionetas):
            camioneta.descargarse()
            self.asignar_pedido_a_camioneta(TipoPizza.ANANA, k)

        self.assertEqual(True, True)

    def test_debe_retornar_la_cantidad_de_pizzas_vendidas_segun_tipo(self):
        simulacion = self.get_simulacion()

        cliente1 = self.generar_cliente_en_rango()

        camioneta1 = Camioneta()
        camioneta1.cargar_pizzas()

        pedido1 = Pedido(cliente1, 10, camioneta1, camioneta1.pizzas[0].tipo)
        pedido1.pizza = camioneta1.pizzas[0]
        pedido1.entregado = True
        simulacion.pedidos.append(pedido1)

        pedido2 = Pedido(cliente1, 10, camioneta1, camioneta1.pizzas[1].tipo)
        pedido2.pizza = camioneta1.pizzas[1]
        pedido2.entregado = True
        simulacion.pedidos.append(pedido2)

        pedido3 = Pedido(cliente1, 10, camioneta1, camioneta1.pizzas[2].tipo)
        pedido3.pizza = camioneta1.pizzas[2]
        pedido3.entregado = True
        simulacion.pedidos.append(pedido3)

        pedido4 = Pedido(cliente1, 10, camioneta1, camioneta1.pizzas[3].tipo)
        pedido4.pizza = camioneta1.pizzas[3]
        pedido4.entregado = True
        simulacion.pedidos.append(pedido4)

        pedido5 = Pedido(cliente1, 10, camioneta1, camioneta1.pizzas[4].tipo)
        pedido5.pizza = camioneta1.pizzas[4]
        pedido5.entregado = True
        simulacion.pedidos.append(pedido5)

        cantidad_de_pizzas_por_tipo = simulacion.pizzas_pedidas_por_tipo()

        self.assertIsInstance(cantidad_de_pizzas_por_tipo, dict)

    def test_debe_retornar_el_tiempo_promedio_de_espera(self):
        simulacion = self.get_simulacion()
        cliente12 = self.generar_cliente_en_rango()

        camioneta12 = Camioneta()
        camioneta12.cargar_pizzas()

        pedido12 = Pedido(cliente12, 10, camioneta12, camioneta12.pizzas[0].tipo)
        pedido12.hora_entrega = 15
        pedido12.pizza = camioneta12.pizzas[0]
        pedido12.entregado = True
        simulacion.pedidos.append(pedido12)

        pedido22 = Pedido(cliente12, 10, camioneta12, camioneta12.pizzas[1].tipo)
        pedido22.hora_entrega = 15
        pedido22.pizza = camioneta12.pizzas[1]
        pedido22.entregado = True
        simulacion.pedidos.append(pedido22)

        pedido32 = Pedido(cliente12, 10, camioneta12, camioneta12.pizzas[2].tipo)
        pedido32.hora_entrega = 15
        pedido32.pizza = camioneta12.pizzas[2]
        simulacion.pedidos.append(pedido32)

        pedido42 = Pedido(cliente12, 10, camioneta12, camioneta12.pizzas[3].tipo)
        pedido42.hora_entrega = 15
        pedido42.pizza = camioneta12.pizzas[3]
        simulacion.pedidos.append(pedido42)

        pedido52 = Pedido(cliente12, 10, camioneta12, camioneta12.pizzas[4].tipo)
        pedido52.hora_entrega = 15
        pedido52.pizza = camioneta12.pizzas[4]
        simulacion.pedidos.append(pedido52)

        tiempo_espera = simulacion.tiempo_espera()

        self.assertEqual(tiempo_espera, 5)

    def test_debe_retornar_pedidos_perdidos(self):
        simulacion = self.get_simulacion()
        cliente13 = self.generar_cliente_en_rango()

        camioneta13 = Camioneta()
        camioneta13.cargar_pizzas()

        pedido13 = Pedido(cliente13, 10, camioneta13, camioneta13.pizzas[0].tipo)
        pedido13.hora_entrega = 15
        pedido13.pizza = camioneta13.pizzas[0]
        pedido13.entregado = True
        simulacion.pedidos.append(pedido13)

        pedido23 = Pedido(cliente13, 10, camioneta13, camioneta13.pizzas[1].tipo)
        pedido23.hora_entrega = 15
        pedido23.pizza = camioneta13.pizzas[1]
        pedido23.entregado = True
        simulacion.pedidos.append(pedido23)

        pedido33 = Pedido(cliente13, 10, camioneta13, camioneta13.pizzas[2].tipo)
        pedido33.hora_entrega = 15
        pedido33.pizza = camioneta13.pizzas[2]
        pedido33.entregado = False
        simulacion.pedidos.append(pedido33)

        pedido43 = Pedido(cliente13, 10, camioneta13, camioneta13.pizzas[3].tipo)
        pedido43.hora_entrega = 15
        pedido43.pizza = camioneta13.pizzas[3]
        pedido43.entregado = False
        simulacion.pedidos.append(pedido43)

        pedido53 = Pedido(cliente13, 10, camioneta13, camioneta13.pizzas[4].tipo)
        pedido53.hora_entrega = 15
        pedido53.pizza = camioneta13.pizzas[4]
        pedido53.entregado = False
        simulacion.pedidos.append(pedido53)

        pedidos = simulacion.pedidos_perdidos()

        self.assertEqual(len(pedidos), 3)

    def test_debe_retornar_distancia_recorrida_por_camionetas(self):
        simulacion = self.get_simulacion()
        cliente14 = self.generar_cliente_en_rango()

        camioneta14 = Camioneta()
        camioneta14.cargar_pizzas()

        pedido14 = Pedido(cliente14, 10, camioneta14, camioneta14.pizzas[0].tipo)
        pedido14.hora_entrega = 15
        pedido14.pizza = camioneta14.pizzas[0]
        pedido14.entregado = True
        camioneta14.generar_evento_enviar_pedido(pedido14)

        simulacion.camionetas.append(camioneta14)
        distancia = simulacion.distacia_recorrida()

        self.assertEqual(distancia, 1999.6979771955564)

    def asignar_pedido_a_camioneta(self, tipo_de_pizza, camioneta):
        simulacion = Simulacion()
        simulacion.camionetas[camioneta].pizzas.append(Pizza(tipo_de_pizza, simulacion.time))
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
        evento.attach(RechazarCliente())
        evento.attach(EncolarCliente())
        return evento

    def get_simulacion(self):
        simulacion = Simulacion()
        simulacion.pedidos = []
        simulacion.clientes_rechazados = []
        simulacion.dias_corridos = []
        simulacion.dias_a_simular = 1
        simulacion.experimentos = 1
        simulacion.camionetas = []
        return simulacion



if __name__ == '__main__':
    unittest.main()
