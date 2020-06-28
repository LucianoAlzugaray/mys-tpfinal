from events.CamionetaRegresaARestauranteEvent import CamionetaRegresaARestauranteEvent
from events.EntregarPizzaEvent import EntregarPizzaEvent
from events.LlamoClienteEvent import LlamoClienteEvent
from .Actividad import Actividad
from ..Pedido import Pedido


class EncolarCliente(Actividad):

    def _ejecutar(self, evento: LlamoClienteEvent):
        if evento.cliente_esta_en_rango():
            from Simulacion import Simulacion

            camioneta = Simulacion().seleccionar_camioneta(evento.cliente, evento.tipo_pizza)

            if camioneta is not None:
                self.asignar_pedido_a_camioneta(camioneta, evento)
                return True

            if Simulacion().utils.convencer_al_cliente():
                tipos_de_pizza_disponibles_en_camionetas = Simulacion().get_tipos_disponibles_en_camionetas()
                tipo_pizza = tipos_de_pizza_disponibles_en_camionetas[0]
                evento.tipo_pizza = tipo_pizza
                camioneta = Simulacion().seleccionar_camioneta(evento.cliente, evento.tipo_pizza)
                self.asignar_pedido_a_camioneta(camioneta, evento)
                return True

            camioneta = Simulacion().obtener_camioneta_a_volver_al_restaurante()
            Simulacion().add_event(CamionetaRegresaARestauranteEvent(camioneta, 10))

    def asignar_pedido_a_camioneta(self, camioneta, evento):
        pedido = Pedido(evento.cliente, evento.hora, camioneta, evento.tipo_pizza)
        from Simulacion import Simulacion
        Simulacion().add_pedido(pedido)
        camioneta.asignar_pedido(pedido)
        evento.dia.encolar_cliente(evento)

