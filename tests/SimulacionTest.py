import unittest

from events.LlamoClienteEvent import LlamoClienteEvent
from Simulacion import Simulacion
from models.Cliente import Cliente
from models.Pizza import Pizza
from models.TipoPizza import TipoPizza
from models.actividades.EncolarCliente import EncolarCliente
from models.actividades.RechazarPedido import RechazarPedido


class SimulacionTest(unittest.TestCase):

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

    def test_debe_rechazar_pedido_cuando_cliente_no_esta_en_rango(self):
        pedidos_rechazados = len(Simulacion().pedidos_rechazados)
        self.assertEqual(0, pedidos_rechazados)

        cliente = self.generar_cliente_fuera_de_rango()
        evento = LlamoClienteEvent(0, cliente, Simulacion().dia_actual)
        evento.attach(RechazarPedido())
        evento.attach(EncolarCliente())
        evento.notify()

        self.assertEqual(pedidos_rechazados + 1, len(Simulacion().pedidos_rechazados))

    def generar_cliente_fuera_de_rango(self):
        cliente = Cliente()
        cliente.ubicacion[0] = 1415
        cliente.ubicacion[1] = 1415
        return cliente

    def generar_cliente_en_rango(self):
        cliente = Cliente()
        cliente.ubicacion[0] = 1414
        cliente.ubicacion[1] = 1414
        return cliente


if __name__ == '__main__':
    unittest.main()
