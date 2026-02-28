import json
from tools import consultar_stock_hardware
from payments import procesar_pago_x402

def ejecutar_cazador_de_recompensas():
    print(" Inicializando OpenClaw Bounty Hunter...")
    print(" Misión: Buscar stock crítico de hardware y sortear muros de pago M2M.\n")


    # El agente piensa usa 'consultar_stock_hardware'
    print(" Agente: Entendido. Llamando a la red del proveedor a través de la herramienta 'consultar_stock_hardware'...")
    resultado = consultar_stock_hardware("FPGA_Xilinx")

    # El agente procesa lo que le ha devuelto el servidor
    print("\n--- Procesando Respuesta ---")
    
    if resultado.get("status") == "payment_required":
        instrucciones = resultado["instructions"]

        # El servidor ha denegado el acceso
        print(" Agente: ¡Alto! El servidor me ha devuelto un error HTTP 402.")
        print(f" Agente: Para desbloquear los datos de la FPGA, necesito transferir {instrucciones['amount_usdc']} USDC.")

        # Delegamos la firma y el envío del micropago a la capa de transacciones
        resultado_pago = procesar_pago_x402(instrucciones)
        if resultado_pago.get("status") == "success":
            
            # Tenemos el token de acceso
            recibo_cripto = resultado_pago["receipt"]
            print(f"\n Agente: Reintentando la petición inyectando el recibo en la cabecera HTTP...")
            
            # Reintento de la petición inyectando el recibo en las cabeceras HTTP
            resultado_final = consultar_stock_hardware("FPGA_Xilinx", recibo=recibo_cripto)
            
            # Evaluación final del payload recuperado
            if resultado_final.get("status") == "success":
                print("\n Agente: ¡Muro superado! Datos de hardware recuperados:")
                print(json.dumps(resultado_final['data']['data'], indent=2))
                print("\n MISIÓN CUMPLIDA. Devolviendo control al usuario.")
            else:
                print(f" Agente: Fallo en el segundo intento - {resultado_final.get('message')}")
    elif resultado.get("status") == "success":
        # El recurso era público o el servidor no exigió pago
        print(f" Agente: Datos recuperados a la primera: {json.dumps(resultado['data'], indent=2)}")
        
    else:
        # Manejo de excepciones de red no controladas
        print(f" Agente: Excepción capturada - {resultado.get('message')}")

if __name__ == "__main__":
    ejecutar_cazador_de_recompensas()