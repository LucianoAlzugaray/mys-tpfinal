from events.LlamoClienteEvent import LlamoClienteEvent
from exeptions import CamionetaNoPuedeAtenderPedidoException
from .Actividad import Actividad
from ..Pedido import Pedido
from events.EventType import EventType
from ..TipoPizza import TipoPizza


class EncolarCliente(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        from Simulacion import Simulacion
        simulacion = Simulacion()

        # Rechazar cliente
        if not simulacion.cliente_esta_en_rango(evento.cliente) or \
           not evento.tipo_pizza in simulacion.tipos_de_pizza_disponibles:

            simulacion.clientes_rechazados.append(evento)
            return

        # asignar pedido a camioneta
        camioneta = simulacion.seleccionar_camioneta(evento.cliente, evento.tipo_pizza)
        if camioneta is not None:
            self.asignar_pedido_a_camioneta(camioneta, evento)
            return

        # convencer al cliente
        if simulacion.utils.convencer_al_cliente():

            # no hay camionetas disponibles
            if len(simulacion.camionetas_disponibles) == 0:
                simulacion.pedidos_en_espera.append(Pedido(evento.cliente, evento.hora, None, evento.tipo_pizza))
                return

            # hay tipo en camioneta
            tipos_disponibles = simulacion.get_tipos_disponibles_en_camionetas()
            evento.tipo_pizza = tipos_disponibles[0]
            camioneta = simulacion.seleccionar_camioneta(evento.cliente, evento.tipo_pizza)
            self.regresar_a_restaurante(evento) if camioneta is None else self.asignar_pedido_a_camioneta(camioneta, evento)
            return

        self.regresar_a_restaurante(evento)

    def asignar_pedido_a_camioneta(self, camioneta, evento):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        pedido = Pedido(evento.cliente, evento.hora, camioneta, evento.tipo_pizza)
        simulacion.add_pedido(pedido)
        camioneta.asignar_pedido(pedido)

    def regresar_a_restaurante(self, evento):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        camioneta = simulacion.obtener_camioneta_a_volver_al_restaurante()
        pedido = Pedido(evento.cliente, evento.hora, camioneta, evento.tipo_pizza)

        if camioneta is None:
            simulacion.pedidos_en_espera.append(pedido)
        else:
            simulacion.add_pedido(pedido)
            camioneta.disponible = False
            camioneta.pedidos.append(pedido)
            simulacion.dispatch(EventType.CAMIONETA_REGRESA_A_BUSCAR_PEDIDO, {'pedido': pedido, 'camioneta': camioneta})

