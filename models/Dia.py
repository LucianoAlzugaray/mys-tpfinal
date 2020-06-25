from events.EntregarPizzaEvent import EntregarPizzaEvent
from events.LlamoClienteEvent import LlamoClienteEvent
from utils.utils import *
from models.Camioneta import Camioneta
import queue
import itertools
from models.actividades.RechazarPedido import RechazarPedido
from models.actividades.EncolarCliente import EncolarCliente


# TODO: se agrega referencia faltante.
def limpiar_pizzas_en_camionetas(camionetas):
    pass


class Dia:
    def __init__(self, minutos_maximo, cantidad_camionetas):
        camionetas = []
        for i in range(cantidad_camionetas):
            camionetas.append(Camioneta())
        self.camionetas = camionetas
        self.minutos_maximo = minutos_maximo
        self.tiempo_actual = 0
        self.pedidos_rechazados = 0
        self.cola_espera_clientes = queue.Queue()
        self.desperdicios = 0
        self.desperdicio_por_fin_de_dia = 0
        self.fel = []

    # Metodo para setup.
    def iniciar_dia(self):
        self.fel = self.generar_pedidos()
        self.ubicar_camionetas()
        self.cargar_camionetas()

    def ubicar_camionetas(self):
        list(map(lambda x: x.volver_a_pizzeria(), self.camionetas))

    # Metodo de ejecución principal.
    def correr(self):
        while not self.termino_dia():
            tiempo_actual = self.get_tiempo_actual()
            # Obtenemos los eventos que se deben realizar en este momento.
            eventos_de_este_minuto = self.obtener_eventos_de_ahora()
            for evento in eventos_de_este_minuto:
                # evento.notify()
                evento.ejecutar_actividad()
            # Si hay clientes esperando y hay camionetas disponibles.
            if self.get_cola_de_espera().qsize() > 0 and self.hay_camionetas_disponibles():
                print("Log -----      mandare una pizza a un cliente")
                # [TODO] mandar la pizza al cliente
            # Aplicamos el paso del reloj
            self.tiempo_actual += 1

            # [HECHO] obtener los eventos del fel que ocurran en este minuto
            # [HECHO] ejecutarlos hsta que no haya más
            # [HECHO] si hay clientes en cola de espera y hay camioneta disponible
            # mandar la pizza al cliente.
            # [HECHO] sumar un minuto más en minuto_actual

        for camioneta in self.get_camionetas():
            camioneta.volver_a_pizzeria()
            self.desperdicio_por_fin_de_dia += camioneta.descargarse()
        # Ver si se necesita guardar algun estado o hacer algun calculo.

    @staticmethod
    def generar_pedidos_en_hora(hora):
        eventos = []
        for i in range(pedidos_generados()):
            evento = LlamoClienteEvent(hora)
            evento.attach(EncolarCliente())
            evento.attach(RechazarPedido())
            eventos.append(evento)

        return eventos
        # return [LlamoClienteEvent(hora) for i in range(pedidos_generados())]

    # TODO: Revisar horas repetidas
    def generar_pedidos(self):
        return list(itertools.chain(*[self.generar_pedidos_en_hora(i) for i in range(12)]))

    def cargar_camionetas(self):
        list(map(lambda camioneta: camioneta.cargar_pizzas(self.tiempo_actual, self.fel), self.camionetas))

    def encolar_cliente(self, cliente):
        self.cola_espera_clientes.put(cliente)

    def termino_dia(self):
        return self.tiempo_actual > self.minutos_maximo

    def acciones_finales_del_dia(self):
        limpiar_pizzas_en_camionetas(self.camionetas)

    def obtener_cliente_de_cola(self):
        return self.cola_espera_clientes.get() if not self.cola_espera_clientes.empty() else None

    def hay_camionetas_disponibles(self):
        return len(list(filter(lambda x: x.esta_disponible(), self.get_camionetas()))) > 0

    def get_tiempo_actual(self):
        return self.tiempo_actual

    def get_fel(self):
        return self.fel

    def get_cola_de_espera(self):
        return self.cola_espera_clientes

    def get_camionetas(self):
        return self.camionetas

    def obtener_eventos_de_ahora(self):
        return list(filter(lambda x: x.get_hora() == self.get_tiempo_actual(), self.fel))

    def enviar_pedido(self, camioneta, pizza):
        self.fel.append(EntregarPizzaEvent(tiempo_entrega(), camioneta, pizza))

    def rechazar_pedido(self):
        self.pedidos_rechazados += 1
