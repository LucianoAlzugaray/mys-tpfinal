from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad
from ..Pedido import Pedido
from events.EventType import EventType
from ..TipoPizza import TipoPizza


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
                tipos_disponibles = simulacion.get_tipos_disponibles_en_camionetas()
                tipo_pizza = tipos_disponibles[0] if len(tipos_disponibles) > 0 else TipoPizza.MOZZARELLA
                evento.tipo_pizza = tipo_pizza

                camioneta = simulacion.seleccionar_camioneta(evento.cliente, evento.tipo_pizza)
                if camioneta is None:
                    self.regresar_a_restaurante(evento)
                else:
                    self.asignar_pedido_a_camioneta(camioneta, evento)
                return True

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
            simulacion.dispatch(EventType.CAMIONETA_REGRESA_A_BUSCAR_PEDIDO, {'pedido': pedido})

