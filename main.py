import paho.mqtt.client as mqtt
import datetime
import time

from Simulacion import Simulacion


def iniciar_simulacion(configuraciones):

    tipos_de_pizza = {
        "anana": configuraciones.anana if configuraciones.anana is not None else True,
        "napolitana": configuraciones.napolitana if configuraciones.napolitana is not None else True,
        "fugazzeta": configuraciones.fugazzeta if configuraciones.fugazzeta is not None else True,
        "mozzarella": configuraciones.mozzarella if configuraciones.mozzarella is not None else True,
        "calabresa": configuraciones.calabresa if configuraciones.calabresa is not None else True
    }

    configuracion = {
        "inicio": time.ctime(configuraciones.inicio) if configuraciones.inicio is not None else datetime.strptime('1/1/20 09:00:00', '%d/%m/%y %H:%M:%S'),
        "fin": time.ctime(configuraciones.fin) if configuraciones.fin is not None else datetime.strptime('31/12/20 23:00:00', '%d/%m/%y %H:%M:%S'),
        "volverAlRestaurante": configuraciones.volverAlRestaurante if configuraciones.volverAlRestaurante is not None else 1,
        "pedidosPorHora": configuraciones.pedidosPorHora if configuraciones.pedidosPorHora is not None else 20,
        "hornosPorCamioneta": configuraciones.hornosPorCamioneta if configuraciones.hornosPorCamioneta is not None else 1,
        "pizzasPorHorno": configuraciones.pizzasPorHorno if configuraciones.pizzasPorHorno is not None else 40,
        "cantidadCamionetas": configuraciones.cantidadCamionetas if configuraciones.cantidadCamionetas is not None else 4,
        "tipos_de_pizza": tipos_de_pizza
    }

    simulacion = Simulacion()
    simulacion.configurate(configuracion)


def on_message(client, user_data, msg):
    print(msg.topic + " " + str(msg.payload))

def on_connect(client, user_data, flags, rc):
    client.subscribe("topic_control")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect("172.16.240.10", 1883, 60)
    print("conectado con el servidor")
    client.loop_forever()