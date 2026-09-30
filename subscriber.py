import json
import paho.mqtt.client as mqtt

TOPICO = "maulec/sms/send"


def on_message(client, userdata, msg):

    try:

        data = json.loads(
            msg.payload.decode()
        )

        print("\n================================")
        print("MENSAJE MQTT RECIBIDO")
        print("================================")
        print("ID :", data.get("id"))
        print("Telefono :", data.get("telefono"))
        print("Mensaje  :", data.get("mensaje"))
        print("Fecha    :", data.get("fecha"))
        print("Origen   :", data.get("origen"))
        print("================================\n")

    except Exception as e:

        print("\nERROR AL PROCESAR MENSAJE MQTT")
        print(str(e))
        print("Payload recibido:")
        print(msg.payload.decode())


client = mqtt.Client()

client.on_message = on_message

client.connect(
    "localhost",
    1883,
    60
)

client.subscribe(TOPICO)

print("Esperando mensajes MQTT...")

client.loop_forever()
