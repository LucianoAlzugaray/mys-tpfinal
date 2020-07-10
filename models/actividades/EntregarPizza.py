from events.EntregarPedidoEvent import EntregarPedidoEvent
from models.actividades.Actividad import Actividad


class EntregarPizza(Actividad):

    def _ejecutar(self, evento: EntregarPedidoEvent):
        if not evento.pedido.esta_fuera_de_hora_de_entrega():
            evento.pedido.camioneta.entregar_pedido(evento.pedido)
            from Simulacion import Simulacion
            simulacion = Simulacion()
            simulacion.remover_evento_vencimiento_pizza(evento.pedido.pizza)

