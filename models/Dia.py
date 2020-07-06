import math
from models.Cliente import Cliente
import queue



class Dia:
    def __init__(self, minutos_maximo, camionetas):
        self.camionetas = camionetas
        self.minutos_maximo = minutos_maximo
        self.tiempo_actual = 0
        self.pedidos_rechazados = []
        self.desperdicios = 0
        self.desperdicio_por_fin_de_dia = 0
        self.fel = []

    # Metodo de ejecución principal.
    def correr(self):
        while not self.termino_dia():
            for evento in self.obtener_eventos_de_ahora():
                evento.notify()
            self.tiempo_actual += 1

        for camioneta in self.get_camionetas():
            camioneta.volver_a_pizzeria()

    def encolar_cliente(self, cliente):
        self.cola_espera_clientes.put(cliente)

    def obtener_cliente_de_cola(self):
        return self.cola_espera_clientes.get() if not self.cola_espera_clientes.empty() else None

    def get_tiempo_actual(self):
        return self.tiempo_actual

    def obtener_eventos_de_ahora(self):
        return list(filter(lambda x: math.trunc(x.time) == math.trunc(self.get_tiempo_actual()), self.fel))

    def rechazar_pedido(self, cliente: Cliente):
        self.pedidos_rechazados.append(cliente)
