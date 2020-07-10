from events.EntregarPedidoEvent import EntregarPedidoEvent
from models.actividades.Actividad import Actividad


class RechazarPedido(Actividad):

    def _ejecutar(self, evento: EntregarPedidoEvent):
        if evento.pedido.esta_fuera_de_hora_de_entrega():
            from Simulacion import Simulacion
            pizza = evento.pedido.camioneta.get_pizza(evento.pedido.pizza)
            pizza.reservada = False
            Simulacion().rechazar_pedido(evento.pedido)
