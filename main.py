import datetime
import time
import paho.mqtt.client as mqtt
import json

def iniciar_simulacion(configuraciones):
    valores = {
        "inicio": time.ctime(configuraciones.inicio) if configuraciones.inicio is not None else datetime.strptime('1/1/20 09:00:00', '%d/%m/%y %H:%M:%S'),
        "fin": time.ctime(configuraciones.fin) if configuraciones.fin is not None else datetime.strptime('31/12/20 23:00:00', '%d/%m/%y %H:%M:%S'),
        "volverAlRestaurante": configuraciones.volverAlRestaurante if configuraciones.volverAlRestaurante is not None else 1,
        "pedidosPorHora": configuraciones.pedidosPorHora if configuraciones.pedidosPorHora is not None else 20,
        "hornosPorCamioneta": configuraciones.hornosPorCamioneta if configuraciones.hornosPorCamioneta is not None else 1,
        "pizzasPorHorno": configuraciones.pizzasPorHorno if configuraciones.pizzasPorHorno is not None else 40,
        "cantidadCamionetas": configuraciones.cantidadCamionetas if configuraciones.cantidadCamionetas is not None else 4,
        "anana": configuraciones.anana if configuraciones.anana is not None else True,
        "napolitana": configuraciones.napolitana if configuraciones.napolitana is not None else True,
        "fugazzeta": configuraciones.fugazzeta if configuraciones.fugazzeta is not None else True,
        "mozzarella": configuraciones.mozzarella if configuraciones.mozzarella is not None else True,
        "calabresa": configuraciones.calabresa if configuraciones.calabresa is not None else True,
        "experimentos": configuraciones.experimentos if configuraciones.experimentos is not None else 10,
    }

    from Simulacion import Simulacion
    simulacion = Simulacion(valores)

def on_message(client, user_data, msg):
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