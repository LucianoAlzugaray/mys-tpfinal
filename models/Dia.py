from events.EntregarPizzaEvent import EntregarPizzaEvent
from events.LlamoClienteEvent import LlamoClienteEvent
from models.Cliente import Cliente
import queue
import itertools
from models.actividades.RechazarPedido import RechazarPedido
from models.actividades.EncolarCliente import EncolarCliente


# TODO: se agrega referencia faltante.
def limpiar_pizzas_en_camionetas(camionetas):
    pass


class Dia:
    def __init__(self, minutos_maximo, camionetas):
        self.camionetas = camionetas
        self.minutos_maximo = minutos_maximo
        self.tiempo_actual = 0
        self.pedidos_rechazados = []
        self.cola_espera_clientes = queue.Queue()
        self.desperdicios = 0
        self.desperdicio_por_fin_de_dia = 0
        self.fel = []

    # Metodo para setup.
    def iniciar_dia(self):
        # TODO: generar eventos de pedido
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
                evento.notify()
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
        from Simulacion import Simulacion
        for i in range(Simulacion().utils.pedidos_generados()):
            evento = LlamoClienteEvent(hora, None)
            evento.attach(EncolarCliente())
            evento.attach(RechazarPedido())
            eventos.append(evento)

        return eventos
        # return [LlamoClienteEvent(hora) for i in range(pedidos_generados())]

    # TODO: Revisar horas repetidas
    def generar_pedidos(self):
        return list(itertools.chain(*[self.generar_pedidos_en_hora(i) for i in range(12)]))

    def cargar_camionetas(self):
        list(map(lambda camioneta: camioneta.cargar_pizzas(), self.camionetas))

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
        return list(filter(lambda x: x.hora == self.get_tiempo_actual(), self.fel))

    def rechazar_pedido(self, cliente: Cliente):
        self.pedidos_rechazados.append(cliente)
