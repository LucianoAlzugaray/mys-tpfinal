import math
from events.SimulacionEvent import SimulacionEvent


class LlamoClienteEvent(SimulacionEvent):
    limite = 2000

    def __init__(self, hora, cliente, dia=None):
        super().__init__(hora)
        self.dia = dia
        self.cliente = cliente
        from Simulacion import Simulacion
        self.hora = hora
        self.tipo_pizza = Simulacion().utils.generar_tipo_de_pizza()

    def cliente_esta_en_rango(self):
        return self.obtener_distancia([0, 0], self.cliente.ubicacion) <= self.limite

    @staticmethod
    def obtener_distancia(punto1, punto2):
        cateto1 = punto2[0] - punto1[0]
        cateto2 = punto2[1] - punto1[1]
        return math.sqrt(math.pow(cateto1, 2) + math.pow(cateto2, 2))

    @staticmethod
    def obtener_camionetas_disponibles(camionetas):
        return list(filter(lambda x: x.disponible, camionetas))

    @staticmethod
    def camionetas_con_pizza_pedida(tipo, camionetas):
        return list(filter(lambda x: x.tiene_tipo(tipo), camionetas))

    def obtener_camioneta_mas_cercana(self, camionetas):
        # obtenemos distancia entre las camionetas y la ubicacion del pedido
        distancias = map(lambda camioneta: (self.obtener_distancia(camioneta.ubicacion, self.cliente.ubicacion), camioneta),
                         camionetas)
        # obtenemos la minima distanc
        distancia_minima = min(distancias, key=lambda distancia: distancia[0])
        # obtenemos camioneta
        return distancia_minima[1]

    # Getter de la hora
    def get_hora(self):
        return self.hora
