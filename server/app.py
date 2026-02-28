from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos simulada
INVENTARIO = {
    "STM32": {"stock": 450, "precio_ud": 4.50},
    "FPGA_Xilinx": {"stock": 12, "precio_ud": 120.00},
    "Antena_RF_5GHz": {"stock": 89, "precio_ud": 15.20}
}

@app.route('/api/stock', methods=['GET'])
def obtener_stock():
    componente = request.args.get('component')
    
    if not componente or componente not in INVENTARIO:
        return jsonify({"error": "Componente no especificado o fuera de catálogo"}), 404

    # Simulamos la comprobación del protocolo x402
    # El servidor busca un comprobante de pago en las cabeceras (headers) HTTP
    recibo_pago = request.headers.get('X-Payment-Receipt')

    if not recibo_pago:
        # Devolvemos el estado 402 y el JSON con las instrucciones de cobro.
        return jsonify({
            "error": "Payment Required",
            "message": "Acceso denegado. Se requiere un micropago para consultar el inventario en tiempo real.",
            "payment_request": {
                "amount_usdc": 0.05,
                "destination_wallet": "0xOpenfortHackathonWalletAddress123",
                "network": "base-sepolia"
            }
        }), 402
    
    # Si la petición incluye el recibo (el agente ha pagado), le damos los datos
    return jsonify({
        "success": True,
        "component": componente,
        "data": INVENTARIO[componente]
    }), 200

if __name__ == '__main__':
    # Arrancamos el servidor en el puerto 5000
    app.run(debug=True, port=5000)