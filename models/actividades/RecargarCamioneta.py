from datetime import timedelta

from events.EventType import EventType
from models.actividades.Actividad import Actividad


class RecargarCamioneta(Actividad):

    def _ejecutar(self, evento):
        camioneta = evento.camioneta
        camioneta.recargarse(evento.pedido)