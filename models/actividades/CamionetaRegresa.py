from events.CamionetaRegresaARestauranteEvent import CamionetaRegresaARestauranteEvent
from models.actividades.Actividad import Actividad


class CamionetaRegresa(Actividad):

    def __init__(self, camioneta):
        self.camioneta = camioneta

    def _ejecutar(self, evento: CamionetaRegresaARestauranteEvent):
        self.camioneta.cargar_pizzas()