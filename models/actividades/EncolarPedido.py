from events.CamionetaRegresaARestauranteEvent import CamionetaRegresaARestauranteEvent
from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad


class EncolarPedido(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        from Simulacion import Simulacion
        simulacion = Simulacion()

        if simulacion.cliente_esta_en_rango(evento.pedido):
            camioneta = simulacion.seleccionar_camioneta(evento.pedido, evento.tipo_pizza)

            if camioneta is not None:
                self.asignar_pedido_a_camioneta(camioneta, evento)
                return True

            if simulacion.utils.convencer_al_cliente():
                tipo_pizza = simulacion.get_tipos_disponibles_en_camionetas()[0]
                evento.tipo_pizza = tipo_pizza
                camioneta = simulacion.seleccionar_camioneta(evento.pedido.cliente, evento.tipo_pizza)
                self.asignar_pedido_a_camioneta(camioneta, evento)
                return True

            camioneta = simulacion.obtener_camioneta_a_volver_al_restaurante()
            simulacion.add_event(CamionetaRegresaARestauranteEvent(camioneta, 10))

    def asignar_pedido_a_camioneta(self, camioneta, evento):
        from Simulacion import Simulacion
        evento.pedido.camioneta = camioneta
        Simulacion().pedidos.append(evento.pedido)
        camioneta.asignar_pedido(evento.pedido)

