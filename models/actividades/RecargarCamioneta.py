from events.EventType import EventType
from models.actividades.Actividad import Actividad


class RecargarCamioneta(Actividad):

    def _ejecutar(self, evento):

        camioneta = evento.camioneta
        camioneta.remover_pizzas_vencidas()
        camioneta.cargar_pizzas()
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.dispatch(EventType.ENVIAR_PEDIDO, {'pedido': camioneta.pedido_en_curso, 'hora': simulacion.time, 'camioneta': camioneta})