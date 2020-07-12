from events import PizzaVenceEvent
from models.actividades.Actividad import Actividad


class VencerPizza(Actividad):

    def _ejecutar(self, evento: PizzaVenceEvent):
        evento.pizza.vencida = True
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.add_desperdicio(evento.pizza, evento.hora)
        #
        #
        # camioneta = simulacion.get_camioneta_by_pizza(evento.pizza)
        # if camioneta.pedido_en_curso is not None:
        #     if len(camioneta.get_pizzas_disponibles()) >

