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

    def cargar_pizzas(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        cantidad_de_pizzas_a_cargar = self.tamanio_hornos - len(self.pizzas)
        if simulacion.pedidos_en_espera:
            self.atender_pedidos_en_espera(cantidad_de_pizzas_a_cargar)
        else:
            self.carga_por_defecto(cantidad_de_pizzas_a_cargar)

        if self.tiempo_ultima_recarga is not None:
            self.tiempo_entre_recargas.append(simulacion.get_diferencia_hora_actual(self.tiempo_ultima_recarga))
        self.tiempo_ultima_recarga = simulacion.time
        self.disponible = True

    def carga_por_defecto(self, cantidad_de_pizzas_a_cargar):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        pizzas_por_tipo = divmod(cantidad_de_pizzas_a_cargar, len(simulacion.tipos_de_pizza_disponibles))
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

    def asignar_pedidos_pendientes(self):
        pedidos = self.pedidos
        from Simulacion import Simulacion
        simulacion = Simulacion()
        if self.pedido_en_curso is not None:
            pedidos.append(self.pedido_en_curso)

        pedidos_sin_pizza = list(filter(lambda x: x.pizza is None, pedidos))
        for pedido in pedidos_sin_pizza:
            self.pizzas.append(simulacion.generar_pizza(pedido.tipo_pizza))
            self.reservar_pizza(pedido)

        pedidos_con_pizza = list(filter(lambda x: x not in pedidos_sin_pizza, pedidos))
        pedidos_con_pizza_vencida = list(filter(lambda x: x.pizza.vencida, pedidos_con_pizza))

        for pedido in pedidos_con_pizza_vencida:
            self.pizzas.append(simulacion.generar_pizza(pedido.tipo_pizza))
            self.reservar_pizza(pedido)

        self.pedido_en_curso = self.pedidos[0]

    def quitar_pizza(self, pizza):
        if pizza in self.pizzas:
            self.pizzas.remove(pizza)

    def entregar_pedido(self, pedido: Pedido):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        self.quitar_pizza(pedido.pizza)
        self.ubicacion = pedido.cliente.ubicacion
        self.pedido_en_curso = None
        pedido.entregado = True
        pedido.hora_entrega = simulacion.time

        if len(self.pedidos) > 0 and self.disponible:
            self.generar_evento_enviar_pedido(self.pedidos[0])

        if len(self.pizzas) == 0 or len(list(filter(lambda x: x.vencida, self.pizzas))) == len(self.pizzas) and self.disponible:
            self.generar_evento_volver_a_restaurante()

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
        simulacion.dispatch(EventType.ENVIAR_PEDIDO, {'hora': simulacion.time + timedelta(minutes=1), 'pedido': pedido})

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

    def asignar_pedido(self, pedido: Pedido):
        pedido.camioneta = self
        self.reservar_pizza(pedido)
        self.pedidos.append(pedido)
        if self.pedido_en_curso is None:
            self.generar_evento_enviar_pedido(pedido)

    def get_ubicacion_pedido_en_curso(self):
        return self.ubicacion if self.pedido_en_curso is None else self.pedido_en_curso.ubicacion

    def get_ubicacion_ultimo_pedido(self):
        return self.pedidos[len(self.pedidos) - 1].ubicacion

    def get_ubicacion(self):
        return self.ubicacion

    def enviar_pedido(self):
        if len(self.pedidos) > 0:
            self.pedido_en_curso = self.pedidos[0]
            self.pedido_en_curso.ubicacion_origen = self.ubicacion
            self.pedidos.remove(self.pedido_en_curso)

    def obtener_tiempo_demora_en_volver(self):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        ubicacion = self.ubicacion if self.pedido_en_curso is None else self.pedido_en_curso.ubicacion
        distancia = simulacion.obtener_distancia([0, 0], ubicacion)
        velocidad = 20

        tiempo = (distancia / velocidad) * 60
        return simulacion.dia + timedelta(minutes=tiempo)

    def finalizar_dia(self):
        self.volver_a_pizzeria()
        self.pizzas = []

    def atender_pedidos_en_espera(self, cantidad_de_pizzas_a_cargar):
        from Simulacion import Simulacion
        simulacion = Simulacion()
        pedidos_en_espera = simulacion.pedidos_en_espera[0: cantidad_de_pizzas_a_cargar]

        for pedido in pedidos_en_espera:
            pedido.camioneta = self
            self.pizzas.append(simulacion.generar_pizza(pedido.tipo_pizza))
            self.reservar_pizza(pedido)
            self.pedidos.append(pedido)
            simulacion.add_pedido(pedido)
            simulacion.pedidos_en_espera.remove(pedido)




