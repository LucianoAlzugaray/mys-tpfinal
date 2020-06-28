import unittest

from Simulacion import Simulacion
from SimulacionExceptions.NoHayTipoPizzaEnCamionetaException import NoHayTipoPizzaEnCamionetaException
from events.LlamoClienteEvent import LlamoClienteEvent
from models.Camioneta import Camioneta
from models.Cliente import Cliente
from models.Pedido import Pedido
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.actividades.EncolarCliente import EncolarCliente
from models.actividades.RechazarPedido import RechazarPedido


class CamionetaTest(unittest.TestCase):

    def setUp(self):
        self.camioneta = Camioneta()

    def test_tiene_tipo(self):
        self.camioneta.pizzas = []
        self.assertTrue(len(self.camioneta.pizzas) == 0)

        self.assertFalse(self.camioneta.tiene_tipo(TipoPizza.ANANA))

        pizza = Pizza(TipoPizza.ANANA)
        self.camioneta.pizzas.append(pizza)
        self.assertTrue(self.camioneta.tiene_tipo(TipoPizza.ANANA))

    def test_quitar_pizza(self):
        self.camioneta.cargar_pizzas()
        pizza = self.camioneta.pizzas[0]
        self.camioneta.quitar_pizza(pizza)
        self.assertTrue(len(self.camioneta.pizzas) == 39)

    def test_cargar_pizzas(self):
        self.assertIsInstance(self.camioneta, Camioneta)
        self.assertTrue(len(self.camioneta.pizzas) == 0)
        self.camioneta.cargar_pizzas()
        self.assertTrue(len(self.camioneta.pizzas) == 40)
        self.camioneta.pizzas = []
        self.assertTrue(len(self.camioneta.pizzas) == 0)
        self.camioneta.pizzas = [Pizza(TipoPizza.ANANA),
                                 Pizza(TipoPizza.ANANA),
                                 Pizza(TipoPizza.ANANA)]
        self.assertTrue(len(self.camioneta.pizzas) == 3)
        self.camioneta.cargar_pizzas()
        self.assertTrue(len(self.camioneta.pizzas) == 40)

    def test_sabe_reservar_una_pizza(self):
        cantidad_de_eventos = len(Simulacion().dia_actual.fel)
        self.camioneta = Camioneta()
        self.camioneta.pizzas.append(Pizza(TipoPizza.ANANA))
        self.assertEqual(cantidad_de_eventos + 1, len(Simulacion().dia_actual.fel))

        cliente = Cliente()
        cliente.ubicacion = [1414, 1414]
        pedido = Pedido(cliente, Simulacion().get_hora(), self.camioneta, TipoPizza.ANANA)
        self.camioneta.reservar_pizza(pedido)
        self.assertEqual(len(self.camioneta.pizzas_reservadas), 1)

        self.assertRaises(NoHayTipoPizzaEnCamionetaException, self.camioneta.reservar_pizza, pedido)


    def test_debe_enviar_pedido_asignado_cuando_no_tiene_pedido_en_curso_y_cambiar_pedido_en_curso_al_enviar(self):

        Simulacion().dia_actual.tiempo_actual = 120
        Simulacion().dias_a_simular = 1
        Simulacion().experimentos = 1

        cliente = self.generar_cliente_en_rango()
        evento = self.generar_evento(cliente, None)
        Simulacion().add_event(evento)
        Simulacion().run()

        self.assertTrue(True)

    @staticmethod
    def generar_cliente_en_rango():
        cliente = Cliente()
        cliente.ubicacion[0] = 1414
        cliente.ubicacion[1] = 1414
        return cliente

    @staticmethod
    def generar_evento(cliente, tipo_pizza):
        evento = LlamoClienteEvent(121, cliente, Simulacion().dia_actual)
        if tipo_pizza is not None:
            evento.tipo_pizza = tipo_pizza
        evento.attach(RechazarPedido())
        evento.attach(EncolarCliente())
        return evento

        # self.camioneta.pizzas.append(Pizza(TipoPizza.NAPOLITANA))
        # pedido2 = Pedido(cliente, 10, self.camioneta, TipoPizza.NAPOLITANA)
        # self.camioneta.asignar_pedido(pedido2)
        # self.assertEqual(pedido, self.camioneta.pedido_en_curso)
        #
        # self.camioneta.enviar_pedido()
        # self.assertEqual(pedido2, self.camioneta.pedido_en_curso)



        # calcular variable aleatoria de tiempo de entrega
        # generar un evento de pizza entregada
        #
        #     cuando se produce un evento de pizza entregada
        #         hay que decirle a la camioneta enviar_siguiente_pedido
        #             si no tiene pedidos que entregar debe se queda donde está




if __name__ == '__main__':
    unittest.main()
