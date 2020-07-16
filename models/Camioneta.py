import math
from datetime import timedelta

from events.EventType import EventType
from models.Pedido import Pedido


class Camioneta:

    def __init__(self, cantidad_hornos=1, tamanio_hornos=40):
        self.ubicacion = [0, 0]
        self.pizzas = []
        self.disponible = True
        self.pedidos = []
        self.distancia_recorrida = 0
        self.tiempo_entre_recargas = []
        self.tiempo_ultima_recarga = None
        self.cantidad_hornos = cantidad_hornos
        self.tamanio_hornos = tamanio_hornos

    # Lógica de asignación, envío, entrega y rechazo de pedidos
    def asignar_pedido(self, pedido: Pedido):

        self.pedidos.append(pedido)
        if self.siguiente_pedido == pedido:
            self.generar_evento_enviar_pedido(pedido)

    def enviar_pedido(self, pedido: Pedido):
        self.distancia_recorrida += self.obtener_distancia(self.ubicacion, pedido.cliente.ubicacion)
        self.ubicacion = pedido.cliente.ubicacion
        if not self._tengo_pizzas_para_entregar(pedido):
            self.generar_evento_volver_a_restaurante(pedido)
        else:
            pedido.ubicacion_origen = self.ubicacion
            from Simulacion import Simulacion
            simulacion = Simulacion()
            simulacion.dispatch(EventType.ENTREGAR_PEDIDO, {'hora': simulacion.time + timedelta(minutes=simulacion.utils.tiempo_entrega()), 'pedido': pedido})

    def entregar_pedido(self, pedido: Pedido):
        if self._tengo_pizzas_para_entregar(pedido):
            self._entregar_pedido(pedido)
            self._enviar_siguiente_pedido()
        else:
            self._volver_a_restaurante_a_buscar_pedido(pedido)

    def rechazar_pedido(self, pedido):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        pedido.entregado = False
        pedido.hora_entrega = simulacion.time
        if pedido in self.pedidos:
            self.pedidos.remove(pedido)
        self._enviar_siguiente_pedido()

    def _entregar_pedido(self, pedido):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.remover_evento_vencimiento_pizza(pedido.pizza)
        pedido.entregado = True
        pedido.hora_entrega = simulacion.time
        pedido.pizza = self._tomar_pizza(pedido.tipo_pizza)
        if pedido in self.pedidos:
            self.pedidos.remove(pedido)

    def _tomar_pizza(self, tipo_pizza):
        pizza = sorted(list(filter(lambda x: x.tipo == tipo_pizza, self.pizzas)), key=lambda pizza: pizza.hora)[0]
        self.pizzas.remove(pizza)
        return pizza

    def _enviar_siguiente_pedido(self):
        if not self.tengo_pedidos():
            return
        elif not self.tengo_pizzas_para_el_siguiente_pedido():
            self.generar_evento_volver_a_restaurante()
        else:
            self.generar_evento_enviar_pedido(self.siguiente_pedido)

    def _volver_a_restaurante_a_buscar_pedido(self, pedido):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.dispatch(EventType.CAMIONETA_REGRESA_A_BUSCAR_PEDIDO, {'pedido': pedido, 'camioneta': self})

    def recargarse(self, pedido=None):
        self.remover_pizzas_vencidas()
        self.cargar_pizzas()

        if pedido is not None:
            self._enviar_pedido(pedido)
        else:
            self._enviar_siguiente_pedido()

    def _enviar_pedido(self, pedido: Pedido):
        pedido.ubicacion_origen = self.ubicacion
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.dispatch(EventType.ENTREGAR_PEDIDO, {'hora': simulacion.time + timedelta(minutes=simulacion.utils.tiempo_entrega()), 'pedido': pedido})

    def volver_a_pizzeria(self):
        self.distancia_recorrida += self.obtener_distancia(self.ubicacion, [0, 0])
        self.ubicacion = [0, 0]

    # generacion de eventos
    def generar_evento_volver_a_restaurante(self, pedido=None):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        self.disponible = False
        if pedido is not None:
            simulacion.dispatch(EventType.CAMIONETA_REGRESA_A_BUSCAR_PEDIDO, {'pedido': pedido, 'camioneta': self})
        else:
            simulacion.dispatch(EventType.CAMIONETA_REGRESA_VACIA, {'camioneta': self})

    def generar_evento_enviar_pedido(self, pedido):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.dispatch(EventType.ENVIAR_PEDIDO, {'hora': simulacion.time + timedelta(seconds=1), 'pedido': pedido, 'camioneta': self})

    # Lógica de carga de la camioneta

    def cargar_pizzas(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        if simulacion.pedidos_en_espera:
            self.cargar_pedidos_en_espera()
        else:
            self.carga_por_defecto()

        if self.tiempo_ultima_recarga is not None:
            self.tiempo_entre_recargas.append(simulacion.get_diferencia_hora_actual(self.tiempo_ultima_recarga))

        self.tiempo_ultima_recarga = simulacion.time
        self.disponible = True

    def carga_por_defecto(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        pizzas_por_tipo = divmod(self.cantidad_de_pizzas_a_cargar, len(simulacion.tipos_de_pizza_disponibles))
        for tipo_de_pizza in simulacion.tipos_de_pizza_disponibles:
            self.pizzas += [simulacion.generar_pizza(tipo_de_pizza) for i in range(pizzas_por_tipo[0])]
        k = 0
        for i in range(pizzas_por_tipo[1]):
            self.pizzas.append(simulacion.generar_pizza(simulacion.tipos_de_pizza_disponibles[k]))
            k += 1
            if i > len(simulacion.tipos_de_pizza_disponibles):
                k = 0

    def cargar_pedidos_en_espera(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.atender_pedidos_en_espera(self)

    def remover_pizzas_vencidas(self):
        self.pizzas = list(filter(lambda x: not x.vencida, self.pizzas))

    # condiciones
    def tiene_tipo(self, tipo):
        return len(list(filter(lambda x: x.tipo == tipo, self.pizzas_no_vencidas))) > 0

    def tengo_pizzas_para_el_siguiente_pedido(self):
        return self.tengo_pedidos() and len(list(filter(lambda x: x.tipo == self.siguiente_pedido.tipo_pizza, self.pizzas))) > 0

    def tengo_pedidos(self):
        return len(self.pedidos) > 0

    def _tengo_pizzas_para_entregar(self, pedido):
        return len(list(filter(lambda x: not x.vencida and x.tipo == pedido.tipo_pizza, self.pizzas))) > 0

    def tengo_pizzas(self):
        return len(self.pizzas) > 0 and not self.todas_mis_pizzas_estan_vencidas()

    def todas_mis_pizzas_estan_vencidas(self):
        return len(list(filter(lambda x: x.vencida, self.pizzas))) == len(self.pizzas) > 0

    def no_estoy_volviendo_a_restaurante(self):
        return self.disponible

    def puedo_atender_pedido(self, pedido):
        pedidos = list(filter(lambda x: x.tipo_pizza == pedido.tipo_pizza, self.pedidos))
        pizzas_de_tipo = list(filter(lambda x: x.tipo == pedido.tipo_pizza, self.pizzas))
        return len(pizzas_de_tipo) > len(pedidos)

    # Lógica de manejo de las distancias
    def obtener_distancia(self, punto1, punto2):
        cateto1 = punto2[0] - punto1[0]
        cateto2 = punto2[1] - punto1[1]
        return math.trunc(math.sqrt(math.pow(cateto1, 2) + math.pow(cateto2, 2)))

    def obtener_tiempo_demora_en_volver(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        tiempo = simulacion.utils.velocidad_carga_pizza()
        return simulacion.dia + timedelta(minutes=tiempo)

    # estos metodos se llaman por reflection para ordenar las camionetas (horrible)
    def get_ubicacion_pedido_en_curso(self):
        return self.ubicacion if not self.tengo_pedidos() else self.siguiente_pedido.ubicacion

    def get_ubicacion_ultimo_pedido(self):
        return self.pedidos[len(self.pedidos) - 1].ubicacion

    def get_ubicacion(self):
        return self.ubicacion

    def finalizar_dia(self):
        self.pedidos = []
        self.volver_a_pizzeria()
        self.pizzas = []

    @property
    def siguiente_pedido(self):
        return self.pedidos[0]

    @property
    def pizzas_no_vencidas(self):
        return list(filter(lambda x: not x.vencida, self.pizzas))

    @property
    def pizzas_disponibles(self):
        return list(filter(lambda x: not x.vencida, self.pizzas))

    @property
    def cantidad_de_pizzas_a_cargar(self):
        return self.tamanio_hornos - len(self.pizzas_no_vencidas)

    # Estos métodos solo se están usando en los tests
    def get_pizza(self, pizza):
        pizzas = list(filter(lambda x: x == pizza, self.pizzas))
        return None if len(pizzas) == 0 else pizzas[0]

