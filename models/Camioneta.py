import math
from datetime import timedelta
from exeptions.NoHayTipoPizzaEnCamionetaException import NoHayTipoPizzaEnCamionetaException
from events.EventType import EventType
from models.Pedido import Pedido


class Camioneta:

    def __init__(self, cantidad_hornos=1, tamanio_hornos=40):
        self.ubicacion = [0, 0]
        self.pizzas = []
        self.disponible = True
        self.pedido_en_curso = None
        self.pedidos = []
        self.distancia_recorrida = 0
        self.tiempo_entre_recargas = []
        self.tiempo_ultima_recarga = None
        self.cantidad_hornos = cantidad_hornos
        self.tamanio_hornos = tamanio_hornos

    @property
    def cantidad_de_pizzas_a_cargar(self):
        return self.tamanio_hornos - len(self.pizzas_no_vencidas)

    def cargar_pizzas(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        if simulacion.pedidos_en_espera:
            self.atender_pedidos_en_espera()
        else:
            self.carga_por_defecto()

        if self.tiempo_ultima_recarga is not None:
            self.tiempo_entre_recargas.append(simulacion.get_diferencia_hora_actual(self.tiempo_ultima_recarga))

        self.tiempo_ultima_recarga = simulacion.time
        self.disponible = True

    @property
    def pizzas_no_vencidas(self):
        return list(filter(lambda x: not x.vencida, self.pizzas))

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

    def remover_pizzas_vencidas(self):
        self.pizzas = list(filter(lambda x: not x.vencida, self.pizzas))

    def entregar_pizza(self):
        return sorted(list(filter(lambda x: x.tipo == self.pedido_en_curso.tipo_pizza, self.pizzas)), key=lambda pizza: pizza.hora)[0]

    def _entregar_pedido(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.remover_evento_vencimiento_pizza(self.pedido_en_curso.pizza)
        self.pedido_en_curso.entregado = True
        self.pedido_en_curso.hora_entrega = simulacion.time
        self.pedido_en_curso.pizza = self.entregar_pizza()
        self.pizzas.remove(self.pedido_en_curso.pizza)
        self.pedido_en_curso = None

    def _enviar_siguiente_pedido(self):

        if self.tengo_pizzas_para_el_siguiente_pedido() and self.no_estoy_volviendo_a_restaurante():
            from Simulacion import Simulacion
            simulacion = Simulacion()
            if len(self.pedidos) > 0:
                self.generar_evento_enviar_pedido(self.pedidos[0])

        if not self.tengo_pizzas():
            self.generar_evento_volver_a_restaurante()
        elif self.tengo_pedidos() and not self.tengo_pizzas_para_el_siguiente_pedido():
            self.pedido_en_curso = self.pedidos[0]
            self.pedidos.remove(self.pedido_en_curso)
            self._volver_a_restaurante()

    def tengo_pizzas_para_el_siguiente_pedido(self):
        return self.tengo_pedidos() and len(list(filter(lambda x: x.tipo == self.pedidos[0].tipo_pizza, self.pizzas))) > 0

    def tengo_pedidos(self):
        return len(self.pedidos) > 0

    def enviar_pedido(self):
        if self.pedido_en_curso is None:
            pedido = self.pedidos[0]
            self.pedido_en_curso = pedido
            self.pedido_en_curso.ubicacion_origen = self.ubicacion
            self.pedidos.remove(pedido)

    def entregar_pedido(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        self.ubicacion = self.pedido_en_curso.cliente.ubicacion if self.pedido_en_curso is not None else self.ubicacion
        if self._tengo_pizzas_para_entregar():
            self._entregar_pedido()
            self._enviar_siguiente_pedido()
        else:
            self._volver_a_restaurante()

    def _volver_a_restaurante(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        if self.pedido_en_curso is not None:
            simulacion.dispatch(EventType.CAMIONETA_REGRESA_A_BUSCAR_PEDIDO, {'pedido': self.pedido_en_curso, 'camioneta': self})

    def _tengo_pizzas_para_entregar(self):
        if self.pedido_en_curso is None:
            return False
        return len(list(filter(lambda x: not x.vencida and x.tipo == self.pedido_en_curso.tipo_pizza, self.pizzas))) > 0

    def tengo_pizzas(self):
        return len(self.pizzas) > 0 and not self.todas_mis_pizzas_estan_vencidas()

    def todas_mis_pizzas_estan_vencidas(self):
        return len(list(filter(lambda x: x.vencida, self.pizzas))) == len(self.pizzas) > 0

    def no_estoy_volviendo_a_restaurante(self):
        return self.disponible

    def generar_evento_volver_a_restaurante(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.dispatch(EventType.CAMIONETA_REGRESA_VACIA, {'camioneta': self})

    def obtener_distancia(self, punto1, punto2):
        cateto1 = punto2[0] - punto1[0]
        cateto2 = punto2[1] - punto1[1]
        return math.sqrt(math.pow(cateto1, 2) + math.pow(cateto2, 2))

    def generar_evento_enviar_pedido(self, pedido):
        self.distancia_recorrida += self.obtener_distancia(self.ubicacion, pedido.cliente.ubicacion)
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.dispatch(EventType.ENVIAR_PEDIDO, {'hora': simulacion.time + timedelta(seconds=1), 'pedido': self.pedido_en_curso, 'camioneta': self})

    def tiene_tipo(self, tipo):
        return len(list(filter(lambda x: x.tipo == tipo, self.pizzas_no_vencidas))) > 0

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
        pizzas = list(filter(lambda x: x == pizza, self.pizzas))
        return None if len(pizzas) == 0 else pizzas[0]

    def reservar_pizza(self, pedido: Pedido) -> None:
        pizzas_disponibles = self.get_pizzas_disponibles()
        pizza_del_tipo = list(filter(lambda x: x.tipo == pedido.tipo_pizza, pizzas_disponibles))

        if len(pizza_del_tipo) == 0:
            raise NoHayTipoPizzaEnCamionetaException(f"reservar_pizza: No hay pizza del tipo {pedido.tipo_pizza}")

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

    def puedo_atender_pedido(self, pedido):
        pedidos = list(filter(lambda x: x.tipo_pizza == pedido.tipo_pizza, self.pedidos))
        pizzas_de_tipo = list(filter(lambda x: x.tipo == pedido.tipo_pizza, self.pizzas))
        return len(pedidos) == len(pizzas_de_tipo)


    def asignar_pedido(self, pedido: Pedido):

        self.pedidos.append(pedido)
        if self.pedido_en_curso is None:
            self.generar_evento_enviar_pedido(pedido)

    def get_ubicacion_pedido_en_curso(self):
        return self.ubicacion if self.pedido_en_curso is None else self.pedido_en_curso.ubicacion

    def get_ubicacion_ultimo_pedido(self):
        return self.pedidos[len(self.pedidos) - 1].ubicacion

    def get_ubicacion(self):
        return self.ubicacion

    def obtener_tiempo_demora_en_volver(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        tiempo = simulacion.utils.tiempo_entrega()
        return simulacion.dia + timedelta(minutes=tiempo)

    def finalizar_dia(self):
        self.volver_a_pizzeria()
        self.pizzas = []

    def atender_pedidos_en_espera(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        simulacion.atender_pedidos_en_espera(self)




