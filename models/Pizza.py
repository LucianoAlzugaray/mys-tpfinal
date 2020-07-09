from events.PizzaVenceEvent import PizzaVenceEvent
from models.actividades.VencerPizza import VencerPizza
from models.EventTypeEnum import EventTypeEnum

class Pizza:
    def __init__(self, tipo, hora):
        self.tipo = tipo
        self.vencida = False
        self.reservada = False
        self.hora = hora
