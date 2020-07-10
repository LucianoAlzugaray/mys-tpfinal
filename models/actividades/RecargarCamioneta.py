from events.CamionetaRegresaARestauranteEvent import CamionetaRegresaARestauranteEvent
from models.actividades.Actividad import Actividad


class RecargarCamioneta(Actividad):

    def _ejecutar(self, evento: CamionetaRegresaARestauranteEvent):
        evento.camioneta.cargar_pizzas()
