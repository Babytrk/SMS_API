from flask import Flask, request, jsonify
from datetime import datetime
import json
import paho.mqtt.client as mqtt
import os
# ======================================
# CONFIGURACION MQTT
# ======================================

BROKER = "localhost"
PUERTO = 1883
TOPICO = "maulec/sms/send"

# ======================================
# FLASK
# ======================================

app = Flask(__name__)


# ======================================
# PUBLICAR MQTT
# ======================================

def publicar_mqtt(payload):

    client = mqtt.Client()

    client.connect(
        BROKER,
        PUERTO,
        60
    )

    resultado = client.publish(
        TOPICO,
        json.dumps(payload)
    )

    client.disconnect()

    return resultado.rc


# ======================================
# ENDPOINT ENVIAR SMS
# ======================================

@app.route("/enviar_sms", methods=["POST"])
def enviar_sms():

    try:

        data = request.get_json()

        print("\n================================")
        print("NUEVA PETICION RECIBIDA")
        print("================================")
        print(data)

        telefono = data.get("Telefono")
        mensaje = data.get("Mensaje")

        payload = {
            "telefono": telefono,
            "mensaje": mensaje,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origen": "PowerApps"
        }

        print("\nPUBLICANDO MQTT...")
        print(payload)

        resultado = publicar_mqtt(payload)

        print(f"Resultado MQTT: {resultado}")

        if resultado == 0:
            print("MENSAJE PUBLICADO CORRECTAMENTE")
        else:
            print("ERROR AL PUBLICAR MQTT")

        return jsonify({
            "success": True,
            "telefono": telefono,
            "mensaje": mensaje
        })

    except Exception as e:

        print("\nERROR:")
        print(str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ======================================
# ENDPOINT DE PRUEBA
# ======================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "estado": "ok",
        "broker": BROKER,
        "topico": TOPICO
    })


# ======================================
# INICIO
# ======================================

import os

if __name__ == "__main__":

    print("==============================")
    print("API MQTT INICIADA")
    print(f"Broker : {BROKER}")
    print(f"Puerto : {PUERTO}")
    print(f"Topico : {TOPICO}")
    print("==============================")

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
