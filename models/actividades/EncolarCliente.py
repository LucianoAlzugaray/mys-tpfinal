from events.CamionetaRegresaABuscarPedidoEvent import CamionetaRegresaABuscarPedidoEvent
from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad
from ..Pedido import Pedido
from models.EventTypeEnum import EventTypeEnum


class EncolarCliente(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        from Simulacion import Simulacion
        simulacion = Simulacion()

        if simulacion.cliente_esta_en_rango(evento.cliente) and evento.tipo_pizza in simulacion.tipos_de_pizza_disponibles:
            camioneta = simulacion.seleccionar_camioneta(evento.cliente, evento.tipo_pizza)

            if camioneta is not None:
                self.asignar_pedido_a_camioneta(camioneta, evento)
                return True

            if simulacion.utils.convencer_al_cliente():
                # TODO : BUG - aveces no hay elementos en la lista.
                tipo_pizza = simulacion.get_tipos_disponibles_en_camionetas()[0]
                evento.tipo_pizza = tipo_pizza
                camioneta = simulacion.seleccionar_camioneta(evento.cliente, evento.tipo_pizza)
                self.asignar_pedido_a_camioneta(camioneta, evento)
                return True

            camioneta = simulacion.obtener_camioneta_a_volver_al_restaurante()
            pedido = Pedido(evento.cliente, evento.hora, camioneta, evento.tipo_pizza)
            simulacion.add_pedido(pedido)

            camioneta.disponible = False
            camioneta.pedidos.append(pedido)
            simulacion.add_event(EventTypeEnum.CAMIONETA_REGRESA_A_BUSCAR_PEDIDO, {'pedido': pedido})

    def asignar_pedido_a_camioneta(self, camioneta, evento):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        pedido = Pedido(evento.cliente, evento.hora, camioneta, evento.tipo_pizza)
        simulacion.add_pedido(pedido)
        camioneta.asignar_pedido(pedido)

