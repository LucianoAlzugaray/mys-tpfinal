from events import PizzaVenceEvent
from models.actividades.Actividad import Actividad


class VencerPizza(Actividad):

    def _ejecutar(self, evento: PizzaVenceEvent):
        evento.pizza.vencida = True
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.add_desperdicio(evento.pizza, evento.hora)
