from utils.utils import *


# TODO: se agregó referencia faltante
def enviar_pedido(camioneta, dia):
    pass


# TODO: se agregó referencia faltante
def cargar_camioneta(camioneta):
    pass


# TODO: Generar ubicacion
class LlamoClienteEvent:
    limite = 2000

    def __init__(self, hora):
        self.hora = pedido_en_hora() + hora * 60
        self.tipo = generar_tipo_de_pizza()
        self.ubicacion = generar_ubicacion_cliente()

    def cliente_esta_en_rango(self):
        cateto1 = self.ubicacion[0]
        cateto2 = self.ubicacion[1]
        # calculamos hipotenusa
        hipotenusa = math.sqrt(math.pow(cateto1) + math.pow(cateto2))
        return hipotenusa <= self.limite

    @staticmethod
    def obtener_camionetas_disponibles(camionetas):
        return [camioneta for camioneta in camionetas if camioneta.disponible]

    @staticmethod
    def camionetas_con_pizza_pedida(tipo, camionetas):
        return [camioneta for camioneta in camionetas if camioneta.tiene_tipo(tipo)]

    @staticmethod
    def obtener_distancia(punto1, punto2):
        cateto1 = punto2[0] - punto1[0]
        cateto2 = punto2[1] - punto1[1]
        # calculamos distancia
        return math.sqrt(math.pow(cateto1) + math.pow(cateto2))

    def obtener_camioneta_mas_cercana(self, ubicacion, camionetas):
        # obtenemos distancia entre las camionetas y la ubicacion del pedido
        distancias = map(lambda camioneta: (self.obtener_distancia(camioneta.ubicacion, self.ubicacion), camioneta),
                         camionetas)
        # obtenemos la minima distancia
        distancia_minima = min(distancias, key=lambda distancia: distancia[0])
        # obtenemos camioneta
        return distancia_minima[1]

    # TODO: refactorizar
    def ejecutar_actividad(self, dia):
        if self.cliente_esta_en_rango():
            camionetas_disponibles = self.obtener_camionetas_disponibles(dia.camionetas)
            if len(camionetas_disponibles) == 0:
                dia.encolar_cliente(self)
            else:
                camionetas_posibles_de_envio = self.camionetas_con_pizza_pedida(self.tipo, camionetas_disponibles)
                if len(camionetas_posibles_de_envio) > 0:
                    camioneta = self.obtener_camioneta_mas_cercana(self.ubicacion, camionetas_posibles_de_envio)
                    enviar_pedido(camioneta, dia)
                else:
                    if cliente_convencido():

                        # TODO: mirar TODO de generar_pizza
                        tipo_pizza = generar_tipo_de_pizza()
                    else:
                        camioneta = self.obtener_camioneta_mas_cercana([0, 0], camionetas_disponibles)
                        cargar_camioneta(camioneta)
        else:
            self.rechazar_pedido(dia)

    # TODO: revisar
    def rechazar_pedido(self, dia):
        dia.pedidos_rechazados += 1
