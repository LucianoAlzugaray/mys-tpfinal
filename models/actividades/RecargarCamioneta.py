from models.actividades.Actividad import Actividad


class RecargarCamioneta(Actividad):

    def _ejecutar(self, evento):

        camioneta = evento.camioneta
        camioneta.remover_pizzas_vencidas()
        camioneta.asignar_pedidos_pendientes()
        camioneta.cargar_pizzas()