from events.EntregarPizzaEvent import EntregarPizzaEvent
from models.actividades.Actividad import Actividad


class RechazarPizza(Actividad):

    def _ejecutar(self, evento: EntregarPizzaEvent):
        if evento.pedido.esta_fuera_de_hora_de_entrega():
            from Simulacion import Simulacion
            Simulacion().rechazar_pedido(evento.pedido)
