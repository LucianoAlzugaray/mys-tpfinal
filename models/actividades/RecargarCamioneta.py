from datetime import timedelta

from events.EventType import EventType
from models.actividades.Actividad import Actividad


class RecargarCamioneta(Actividad):

    def _ejecutar(self, evento):

        camioneta = evento.camioneta
        camioneta.remover_pizzas_vencidas()
        camioneta.cargar_pizzas()
        from Simulacion import Simulacion
        simulacion = Simulacion()
        # si el pedido en curso is none la camioneta tiene que estar vacía
        # si no no se pudo entregar una pizza
        if camioneta.pedido_en_curso is not None:
            simulacion.dispatch(EventType.ENVIAR_PEDIDO, {'pedido': camioneta.pedido_en_curso, 'hora': simulacion.time + timedelta(seconds=1), 'camioneta': camioneta})