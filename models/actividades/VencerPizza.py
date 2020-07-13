from events import PizzaVenceEvent
from events.EventType import EventType
from models.actividades.Actividad import Actividad


class VencerPizza(Actividad):

    def _ejecutar(self, evento: PizzaVenceEvent):
        evento.pizza.vencida = True
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.add_desperdicio(evento.pizza, evento.hora)

        camioneta = simulacion.get_camioneta_by_pizza(evento.pizza)
        if camioneta is not None and not camioneta.tengo_pizzas():
            simulacion.dispatch(EventType.CAMIONETA_REGRESA_VACIA, {'camioneta': camioneta})



