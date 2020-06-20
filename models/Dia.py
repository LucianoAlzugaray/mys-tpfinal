from events.LlamoClienteEvent import LlamoClienteEvent
from utils.utils import *
from models.Camioneta import Camioneta
import queue


# TODO: se agrega referencia faltante.
def limpiar_pizzas_en_camionetas(camionetas):
    pass

class Dia:
    def __init__(self, camionetas, minutos_maximo):
        # TODO: ver valor de minutos_maximo, se agregó la referencia porque faltaba
        self.camionetas = [Camioneta(), Camioneta(), Camioneta(), Camioneta()]
        self.minutos_maximo = minuto_maximo
        self.camionetas = camionetas
        self.tiempo_actual = 0
        self.pedidos_rechazado = 0
        self.cola_espera_clientes = queue.Queue()
        self.desperdicios = 0
        self.desperdicio_por_fin_de_dia = 0
        self.fel = []

    def iniciar_dia(self):
        self.fel = self.generar_pedidos()
        self.ubicar_camionetas()
        self.cargar_camionetas()

    def ubicar_camionetas(self):
        for camioneta in self.camionetas:
            camioneta.volver_a_pizzeria()

    def correr(self):
        while not self.termino_dia():
            pass
            # obtener los eventos del fel que ocurran en este minuto
            # ejecutarlos hsta que no haya más
            # si hay clientes en cola de espera y hay camioneta disponible
                # mandar la pizza al cliente.
            # sumar un minuto más en minuto_actual
        for camioneta in camionetas:
            camioneta.volver_a_pizzeria()
            self.desperdicio_por_fin_de_dia += camioneta.descargarse()
        #Ver si se necesita guardar algun estado o hacer algun calculo.


    ##TODO: Refactorizar
    def generar_pedidos_en_hora(self, hora):
        eventos_de_pedidos = []
        for i in range(pedidos_generados()):
            llama_cliente_event = LlamoClienteEvent()
            eventos_de_pedidos.append(llama_cliente_event)
        return eventos_de_pedidos

    ##TODO: Refactorizar usando listas por compresion
    ##TODO: Revisar horas repetidas
    def generar_pedidos(self):
        fel = []
        for i in range(12):
            fel += self.generar_pedidos_en_hora(i)
        return fel

    def cargar_camionetas(self):
        for camioneta in self.camionetas:
            camioneta.cargar_pizzas(self.tiempo_actual, self.fel)

    def encolar_cliente(self, cliente):
        self.cola_espera_clientes.put(cliente)

    def termino_dia(self):
        return self.tiempo_actual > self.minutos_maximo

    def acciones_finales_del_dia(self):
        limpiar_pizzas_en_camionetas(self.camionetas)

    ## OBTENER CLIENTE CON ESTA FUNCION
    def obtener_cliente_de_cola(self):
        if not self.cola_espera_clientes.empty():
            return self.cola_espera_clientes.get()
        else:
            return None
    def hay_camionetas_disponibles(self):
        #implementar
        pass