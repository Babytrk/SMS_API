import json
import paho.mqtt.client as mqtt

payload = {
    "telefono": "2221234567",
    "mensaje": "Hola desde Python"
}

client = mqtt.Client()

client.connect(
    "localhost",
    1883
)

client.publish(
    "maulec/sms/send",
    json.dumps(payload)
)

client.disconnect()

print("Mensaje enviado.")