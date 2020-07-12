import paho.mqtt.client as mqtt
from datetime import datetime
import json

from Simulacion import Simulacion
from models.TipoPizza import TipoPizza

PIZZAS_POR_HORNO = 40
PEDIDOS_POR_HORA = 20
HORNOS_POR_CAMIONETA = 1
CANTIDAD_DE_CAMIONETAS = 4
VOLVER_AL_RESTAURANTE = False
CANTIDAD_DE_EXPERIMENTOS = 10
FIN = datetime.strptime('31/12/20 23:00:00', '%d/%m/%y %H:%M:%S')
INICIO = datetime.strptime('1/1/20 09:00:00', '%d/%m/%y %H:%M:%S')
TIPOS_PIZZA_DISPONIBLES = [TipoPizza.ANANA, TipoPizza.CALABRESA, TipoPizza.FUGAZZETA, TipoPizza.MOZZARELLA, TipoPizza.NAPOLITANA]

def iniciar_simulacion(configuraciones):
    tipos_de_pizza = []
    if configuraciones["anana"]:
        tipo_de_pizza = {'tipo': TipoPizza.ANANA, 'probabilidad': 0.05}
        tipos_de_pizza.append(tipo_de_pizza)
    elif configuraciones["napolitana"]:
        tipo_de_pizza = {'tipo': TipoPizza.CALABRESA, 'probabilidad': 0.20}
        tipos_de_pizza.append(tipo_de_pizza)
    elif configuraciones["fugazzeta"]:
        tipo_de_pizza = {'tipo': TipoPizza.NAPOLITANA, 'probabilidad': 0.20}
        tipos_de_pizza.append(tipo_de_pizza)
    elif configuraciones["mozzarella"]:
        tipo_de_pizza = {'tipo': TipoPizza.FUGAZZETA, 'probabilidad': 0.20}
        tipos_de_pizza.append(tipo_de_pizza)
    elif configuraciones["calabresa"]:
        tipo_de_pizza = {'tipo': TipoPizza.MOZZARELLA, 'probabilidad': 0.20}
        tipos_de_pizza.append(tipo_de_pizza)

    configuracion = {
        "inicio": datetime.fromtimestamp(configuraciones["inicio"] / 1000.0) if configuraciones["inicio"] is not None else INICIO,
        "fin": datetime.fromtimestamp(configuraciones["fin"] / 1000.0) if configuraciones["fin"] is not None else FIN,
        "volverAlRestaurante": True if configuraciones["volverAlRestaurante"] is not None and configuraciones["volverAlRestaurante"] == 2 else VOLVER_AL_RESTAURANTE,
        "pedidosPorHora": configuraciones["pedidosPorHora"] if configuraciones["pedidosPorHora"] is not None else PEDIDOS_POR_HORA,
        "hornosPorCamioneta": configuraciones["hornosPorCamioneta"] if configuraciones["hornosPorCamioneta"] is not None else HORNOS_POR_CAMIONETA,
        "pizzasPorHorno": configuraciones["pizzasPorHorno"] if configuraciones["pizzasPorHorno"] is not None else PIZZAS_POR_HORNO,
        "cantidadCamionetas": configuraciones["cantidadCamionetas"] if configuraciones["cantidadCamionetas"] is not None else CANTIDAD_DE_CAMIONETAS,
        "cantidadExperimentos": configuraciones["cantidadExperimentos"] if configuraciones["cantidadExperimentos"] is not None else CANTIDAD_DE_EXPERIMENTOS,
        "tipos_de_pizza": tipos_de_pizza
    }

    from Configuracion import Configuracion
    simulacion = Simulacion()
    simulacion.configurate(Configuracion.get_default_configuration())
    simulacion.run()


def on_message(client, user_data, msg):
    print("Llegó una petición de simulación")
    configuracion = json.loads(msg.payload.decode('utf-8'))
    iniciar_simulacion(configuracion)

def on_connect(client, user_data, flags, rc):
    print("conectado con el servidor")
    client.subscribe("control")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect("172.16.240.10", 1883, 60)
    client.loop_forever()