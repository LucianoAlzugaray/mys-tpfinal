from events.CamionetaRegresaARestauranteEvent import CamionetaRegresaARestauranteEvent
from events.EntregarPizzaEvent import EntregarPizzaEvent
from events.EnviarPedidoEvent import EnviarPedidoEvent
from events.LlamoClienteEvent import LlamoClienteEvent
from events.PizzaVenceEvent import PizzaVenceEvent
from models.EventTypeEnum import EventTypeEnum
from models.actividades.EncolarCliente import EncolarCliente
from models.actividades.EntregarPizza import EntregarPizza
from models.actividades.EnviarPedido import EnviarPedido
from models.actividades.RecargarCamioneta import RecargarCamioneta
from models.actividades.RechazarCliente import RechazarCliente
from models.actividades.RechazarPizza import RechazarPizza
from models.actividades.VencerPizza import VencerPizza


class SimulacionEventFactory(object):

    def get_event(self, event_key, kwargs=None):

        if event_key == EventTypeEnum.LLAMO_CLIENTE:
            evento = LlamoClienteEvent(kwargs['hora'], kwargs['cliente'], kwargs['tipo_pizza'])
            evento.attach(EncolarCliente())
            evento.attach(RechazarCliente())
            return evento

        elif event_key == EventTypeEnum.ENVIAR_PEDIDO:
            evento = EnviarPedidoEvent(kwargs['hora'], kwargs['pedido'])
            evento.attach(EnviarPedido())
            return evento

        elif event_key == EventTypeEnum.ENTREGAR_PIZZA:
            evento = EntregarPizzaEvent(kwargs['hora'], kwargs['pedido'])
            evento.attach(EntregarPizza())
            evento.attach(RechazarPizza())
            return evento

        elif event_key == EventTypeEnum.CAMIONETA_REGRESA_A_RESTAURANTE:
            camioneta = kwargs['camioneta']
            hora = camioneta.obtener_tiempo_demora_en_volver()
            evento = CamionetaRegresaARestauranteEvent(camioneta, hora)
            evento.attach(RecargarCamioneta())
            return evento

        elif event_key == EventTypeEnum.PIZZA_VENCE:
            evento = PizzaVenceEvent(kwargs['pizza'])
            evento.attach(VencerPizza())
            return evento
        else:
            pass