from events.PizzaVenceEvent import PizzaVenceEvent
from models.actividades.VencerPizza import VencerPizza


class Pizza:
    def __init__(self, tipo):
        from Simulacion import Simulacion
        self.tipo = tipo
        self.vencida = False
        self.reservada = False
        self.hora = Simulacion().get_hora()
        evento = PizzaVenceEvent(self)
        evento.attach(VencerPizza())
        Simulacion().add_event(evento)
