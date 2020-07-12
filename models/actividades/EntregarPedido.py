from events.EntregarPedidoEvent import EntregarPedidoEvent
from models.actividades.Actividad import Actividad


class EntregarPedido(Actividad):

    def _ejecutar(self, evento: EntregarPedidoEvent):

        if evento.pedido.entregado:
            raise Exception("[ EXCEPCION ] - PEDIDO YA ENTREGADO")
        evento.pedido.camioneta.entregar_pedido()


















            # evento.pedido.camioneta.entregar_pedido(evento.pedido)

# SITUACIONES EN QUE LA CAMIONETA VUELVE AL RESTAURANTE

# 1) ES VACÍA (TRIVIAL)

# 2) VUELVE A BUSCAR PIZZAS PORQUE HAY UN PEDIDO CON UN TIPO DE PIZZA QUE NO EXISTE EN LAS CAMIONETAS CIRCULAND

# queda no disponible
# con pedido_en_curso = None

    # -- CamionetaResgresaArestaurante:
    #
    #     -> recarga la camioneta
    #     -> genera evento enviar pedido

    # queda disponible
    # con pedido_en_curso = None   [YA QUE ES EL ESCUCHADOR DEL EVENTO ENVIAR EL QUE SETEA EL PEDIDO EN CURSO]

# 3) VUELVE A BUSCAR PIZZA DEL PEDIDO EN CURSO PORQUE SE VENCIÓ

# queda no disponible
# con pedido en curso seteado


