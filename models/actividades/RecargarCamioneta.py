from models.actividades.Actividad import Actividad


class RecargarCamioneta(Actividad):

    def _ejecutar(self, evento):

        camioneta = evento.camioneta
        camioneta.remover_pizzas_vencidas()
        camioneta.cargar_pizzas()
        if hasattr(evento, 'pedido'):
            pedido = getattr(evento, 'pedido')
            camioneta.reservar_pizza(pedido.tipo_pizza)
            camioneta.disponible = True
