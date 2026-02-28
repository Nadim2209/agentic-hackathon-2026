import json
from tools import consultar_stock_hardware

def ejecutar_cazador_de_recompensas():
    print(" Inicializando OpenClaw Bounty Hunter...")
    print(" Misión: Buscar stock crítico de hardware y sortear muros de pago M2M.\n")

    # El usuario lanza la petición
    prompt_usuario = "Necesito saber el stock exacto de la FPGA_Xilinx. Si el proveedor exige un pago por la consulta, dime cuánto cuesta y a qué wallet debo pagar."
    print(f" Usuario: {prompt_usuario}\n")

    # El agente piensa usa 'consultar_stock_hardware'
    print(" Agente: Entendido. Llamando a la red del proveedor a través de la herramienta 'consultar_stock_hardware'...")
    resultado = consultar_stock_hardware("FPGA_Xilinx")

    # El agente procesa lo que le ha devuelto el servidor
    print("\n--- Procesando Respuesta ---")
    
    if resultado.get("status") == "payment_required":
        instrucciones = resultado["instructions"]
        print(" Agente: ¡Alto! El servidor me ha devuelto un error HTTP 402.")
        print(f" Agente: Para desbloquear los datos de la FPGA, necesito transferir {instrucciones['amount_usdc']} USDC.")
        print(f" Destino: Wallet {instrucciones['destination_wallet']} (Red: {instrucciones['network']}).")
        print("\n Agente: Derivando la ejecución al módulo de pagos x402...")
        
    elif resultado.get("status") == "success":
        print(f" Agente: ¡Éxito! Los datos obtenidos son: {json.dumps(resultado['data'], indent=2)}")
        
    else:
        print(f" Agente: Ha ocurrido un error inesperado: {resultado.get('message')}")

if __name__ == "__main__":
    ejecutar_cazador_de_recompensas()