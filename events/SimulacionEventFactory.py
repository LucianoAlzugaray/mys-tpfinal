from events.CamionetaRegresaABuscarPedidoEvent import CamionetaRegresaABuscarPedidoEvent
from events.CamionetaRegresaAVacia import CamionetaRegresaVaciaEvent
from events.EntregarPedidoEvent import EntregarPedidoEvent
from events.EnviarPedidoEvent import EnviarPedidoEvent
from events.LlamoClienteEvent import LlamoClienteEvent
from events.PizzaVenceEvent import PizzaVenceEvent
from events.EventType import EventType
from models.actividades.EncolarCliente import EncolarCliente
from models.actividades.EntregarPedido import EntregarPedido
from models.actividades.EnviarPedido import EnviarPedido
from models.actividades.RecargarCamioneta import RecargarCamioneta
from models.actividades.RechazarCliente import RechazarCliente
from models.actividades.RechazarPedido import RechazarPedido
from models.actividades.VencerPizza import VencerPizza


class SimulacionEventFactory(object):

    def get_event(self, event_key, kwargs=None):

        if event_key == EventType.LLAMO_CLIENTE:
            evento = LlamoClienteEvent(kwargs['hora'], kwargs['cliente'], kwargs['tipo_pizza'])
            evento.attach(EncolarCliente())
            evento.attach(RechazarCliente())
            return evento

        elif event_key == EventType.ENVIAR_PEDIDO:
            evento = EnviarPedidoEvent(kwargs['hora'], kwargs['pedido'], kwargs['camioneta'])
            evento.attach(EnviarPedido())
            return evento

        elif event_key == EventType.ENTREGAR_PEDIDO:
            evento = EntregarPedidoEvent(kwargs['hora'], kwargs['pedido'])
            evento.attach(EntregarPedido())
            evento.attach(RechazarPedido())
            return evento

        elif event_key == EventType.CAMIONETA_REGRESA_A_BUSCAR_PEDIDO:
            pedido = kwargs['pedido']
            hora = pedido.camioneta.obtener_tiempo_demora_en_volver()
            evento = CamionetaRegresaABuscarPedidoEvent(pedido, hora)
            evento.attach(RecargarCamioneta())
            return evento

        elif event_key == EventType.CAMIONETA_REGRESA_VACIA:
            camioneta = kwargs['camioneta']
            hora = camioneta.obtener_tiempo_demora_en_volver()
            evento = CamionetaRegresaVaciaEvent(camioneta, hora)
            evento.attach(RecargarCamioneta())
            return evento

        elif event_key == EventType.PIZZA_VENCE:
            evento = PizzaVenceEvent(kwargs['pizza'])
            evento.attach(VencerPizza())
            return evento