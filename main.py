import paho.mqtt.client as mqtt


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