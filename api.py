from flask import Flask, request, jsonify
from datetime import datetime
from uuid import uuid4
import os

app = Flask(__name__)

# COLA DE MENSAJES


mensajes_pendientes = []

# HOME

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "estado": "ok",
        "mensajes_pendientes": len([
            m for m in mensajes_pendientes
            if m["estado"] == "PENDIENTE"
        ])
    })

# RECIBIR MENSAJE DESDE POWER AUTOMATE

@app.route("/enviar_sms", methods=["POST"])
def enviar_sms():

    try:

        data = request.get_json()

        mensaje = {
            "id": str(uuid4()),
            "telefono": data.get("Telefono"),
            "mensaje": data.get("Mensaje"),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origen": "PowerApps",
            "estado": "PENDIENTE"
        }

        mensajes_pendientes.append(mensaje)

        print("\n================================")
        print("NUEVO MENSAJE RECIBIDO")
        print(mensaje)
        print("================================\n")

        return jsonify({
            "success": True,
            "id": mensaje["id"],
            "mensaje": "SMS agregado a la cola"
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# OBTENER MENSAJES PENDIENTES

@app.route("/mensajes", methods=["GET"])
def obtener_mensajes():

    pendientes = [
        mensaje
        for mensaje in mensajes_pendientes
        if mensaje["estado"] == "PENDIENTE"
    ]

    return jsonify(pendientes)

# CONFIRMAR ENVIO
@app.route("/confirmar", methods=["POST"])
def confirmar():

    try:

        data = request.get_json()

        mensaje_id = data.get("id")

        for mensaje in mensajes_pendientes:

            if mensaje["id"] == mensaje_id:

                mensaje["estado"] = "ENVIADO"

                print(f"SMS confirmado: {mensaje_id}")

                return jsonify({
                    "success": True,
                    "id": mensaje_id
                })

        return jsonify({
            "success": False,
            "error": "Mensaje no encontrado"
        }), 404

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# VER TODOS LOS MENSAJES

@app.route("/mensajes_todos", methods=["GET"])
def mensajes_todos():

    return jsonify(mensajes_pendientes)

# LIMPIAR COLA

@app.route("/limpiar", methods=["POST"])
def limpiar():

    mensajes_pendientes.clear()

    return jsonify({
        "success": True,
        "mensaje": "Cola limpiada"
    })

# ESTADISTICAS

@app.route("/estadisticas", methods=["GET"])
def estadisticas():

    pendientes = len([
        m for m in mensajes_pendientes
        if m["estado"] == "PENDIENTE"
    ])

    enviados = len([
        m for m in mensajes_pendientes
        if m["estado"] == "ENVIADO"
    ])

    return jsonify({
        "total": len(mensajes_pendientes),
        "pendientes": pendientes,
        "enviados": enviados
    })
# INICIO
if __name__ == "__main__":

    print("==============================")
    print("API SMS INICIADA")
    print("==============================")

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )