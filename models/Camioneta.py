import math
from datetime import timedelta

from exeptions.NoHayTipoPizzaEnCamionetaException import NoHayTipoPizzaEnCamionetaException
from events.EnviarPedidoEvent import EnviarPedidoEvent
from models.EventTypeEnum import EventTypeEnum
from models.Pedido import Pedido
from models.actividades.EnviarPedido import EnviarPedido
from models.Pizza import Pizza


class Camioneta:
    cantidad_hornos = 1
    tamanio_hornos = 40

    def __init__(self):
        self.ubicacion = [0, 0]
        self.pizzas = []
        self.disponible = True
        self.pedido_en_curso = None
        self.pedidos = []
        self.distancia_recorrida = 0
        self.tiempo_entre_recargas = []
        self.tiempo_ultima_recarga = None

    def cargar_pizzas(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        for i in range(self.tamanio_hornos - len(self.pizzas)):
            self.pizzas.append(Pizza(simulacion.utils.generar_tipo_de_pizza(), simulacion.dia))

        if self.tiempo_ultima_recarga is not None:
            self.tiempo_entre_recargas.append(Simulacion().get_diferencia_hora_actual(self.tiempo_ultima_recarga))
        self.tiempo_ultima_recarga = Simulacion().time


    def quitar_pizza(self, pizza):
        self.pizzas.remove(pizza)

    def entregar_pedido(self, pedido: Pedido):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        self.quitar_pizza(pedido.pizza)
        self.ubicacion = pedido.cliente.ubicacion
        self.pedido_en_curso = None
        pedido.entregado = True
        pedido.hora_entrega = simulacion.time
        if len(self.pedidos) > 0:
            self.generar_evento_enviar_pedido(self.pedidos[0])

    def obtener_distancia(self, punto1, punto2):
        cateto1 = punto2[0] - punto1[0]
        cateto2 = punto2[1] - punto1[1]
        return math.sqrt(math.pow(cateto1, 2) + math.pow(cateto2, 2))

    def generar_evento_enviar_pedido(self, pedido):
        self.distancia_recorrida += self.obtener_distancia(self.ubicacion, pedido.cliente.ubicacion)
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.add_event(EventTypeEnum.ENVIAR_PEDIDO, {'hora': simulacion.time + timedelta(minutes=1), 'pedido': pedido})

    def tiene_tipo(self, tipo):
        return len(list(filter(lambda x: x.tipo == tipo, self.get_pizzas_disponibles()))) > 0

    def volver_a_pizzeria(self):
        self.ubicacion = [0, 0]

    def descargarse(self):
        pizzas_descargadas = len(self.pizzas)
        self.pizzas = []
        return pizzas_descargadas

    def get_pizzas_maximas(self):
        return self.cantidad_hornos * self.tamanio_hornos

    def esta_disponible(self):
        return self.disponible

    def get_pizza(self, pizza):
        pizzas = list(filter(lambda x: x.pizza == pizza, self.pizzas))
        return None if len(pizzas) == 0 else pizzas[0]

    def reservar_pizza(self, pedido: Pedido) -> None:
        pizzas_disponibles = self.get_pizzas_disponibles()
        pizza_del_tipo = list(filter(lambda x: x.tipo == pedido.tipo_pizza, pizzas_disponibles))

        if len(pizza_del_tipo) == 0:
            raise NoHayTipoPizzaEnCamionetaException(f"No hay pizza del tipo {pedido.tipo_pizza}")

        pizza = pizza_del_tipo[0]
        pizza.reservada = True
        pedido.pizza = pizza

    def get_pizzas_disponibles(self):
        return list(filter(lambda x: not x.vencida and not x.reservada, self.pizzas))

    @property
    def pizzas_reservadas(self):
        return list(filter(lambda x: x.reservada, self.pizzas))

    def get_pedido_by_cliente(self, cliente):
        pedidos = list(filter(lambda x: x.cliente == cliente, self.pedidos))
        if self.pedido_en_curso is not None and self.pedido_en_curso.cliente == cliente:
            pedidos.append(self.pedido_en_curso)

        return None if len(pedidos) == 0 else pedidos[0]

    def get_siguiente_pedido(self):
        return self.pedidos[0]

    def asignar_pedido(self, pedido: Pedido):
        self.reservar_pizza(pedido)
        self.pedidos.append(pedido)
        if self.pedido_en_curso is None:
            self.generar_evento_enviar_pedido(pedido)

    def get_ubicacion_pedido_en_curso(self):
        return self.pedido_en_curso if self.pedido_en_curso is None else self.pedido_en_curso.ubicacion

    def get_ubicacion_ultimo_pedido(self):
        return self.pedidos[len(self.pedidos) - 1].ubicacion

    def get_ubicacion(self):
        return self.ubicacion

    def enviar_pedido(self):
        pedido = self.get_siguiente_pedido()
        pedido.ubicacion_origen = self.ubicacion
        self.pedidos.remove(pedido)
        self.pedido_en_curso = pedido


    def obtener_tiempo_demora_en_volver(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        distancia = simulacion.obtener_distancia([0, 0], self.ubicacion)
        velocidad = 20

        tiempo = (distancia / velocidad) * 60

        return simulacion.dia + timedelta(minutes=tiempo)





        # setear el pedio en curso
        # calcular variable aleatoria de tiempo de entrega
        # generar un evento de pizza entregada
        #
        #     cuando se produce un evento de pizza entregada
        #         hay que decirle a la camioneta enviar_siguiente_pedido
        #             si no tiene pedidos que entregar debe se queda donde está




