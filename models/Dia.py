from events.LlamoClienteEvent import LlamoClienteEvent
from utils.utils import *
from models.Camioneta import Camioneta
import queue


# TODO: se agrega referencia faltante.
def limpiar_pizzas_en_camionetas(camionetas):
    pass


class EntregarPizzaEvent(object):
    pass


class Dia:
    def __init__(self, minutos_maximo, cantidad_camionetas):
        camionetas = []
        for i in range(cantidad_camionetas):
            camionetas.append(Camioneta())
        self.camionetas = camionetas
        self.minutos_maximo = minutos_maximo
        self.tiempo_actual = 0
        self.pedidos_rechazado = 0
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
        for camioneta in self.camionetas:
            camioneta.volver_a_pizzeria()

# Metodo de ejecución principal.
    def correr(self):
        while not self.termino_dia():
            tiempoActual = self.get_tiempo_actual()
            # Obtenemos los eventos que se deben realizar en este momento.
            eventosDeEsteMinuto = self.obtener_eventos_de_ahora(tiempoActual)
            for evento in eventosDeEsteMinuto:
                evento.ejecutar_actividad()
            # Si hay clientes esperando y hay camionetas disponibles.
            if ((len(self.get_cola_de_espera())>0) and self.hay_camionetas_disponibles()):
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
        for camioneta in self.get_camionetas():
            if (camioneta.esta_disponible()):
                return True
        return False

    #Getter del tiempo actual.
    def get_tiempo_actual(self):
        return self.tiempo_actual

    #Getter de la fel.
    def get_fel(self):
        return self.fel

    #Getter de la cola de espera de clientes.
    def get_cola_de_espera(self):
        return self.cola_espera_clientes
    
    #Getter de las camionetas del dia
    def get_camionetas(self):
        return self.camionetas


    def obtener_eventos_de_ahora(self, fel):
        nuevaLista = []
        for evento in fel:
            if evento.get_hora() == self.get_tiempo_actual():
                nuevaLista.append(evento)
        return nuevaLista

    def enviar_pedido(self, camioneta, pizza):
        self.fel.append(EntregarPizzaEvent(tiempo_entrega(), camioneta, pizza)) 
