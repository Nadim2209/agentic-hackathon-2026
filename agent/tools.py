import requests
import json

def consultar_stock_hardware(componente: str) -> dict:
    """
    Herramienta para que el agente consulte el stock de componentes electrónicos.
    Si el servidor exige un pago, devuelve las instrucciones de pago en lugar de error.
    """
    url = "http://127.0.0.1:5000/api/stock"
    
    try:
        # Hacemos la petición a la red pasando el nombre del componente
        response = requests.get(url, params={"component": componente})
        
        # Si la respuesta es 200 OK, devolvemos los datos de hardware directamente
        if response.status_code == 200:
            return {
                "status": "success",
                "data": response.json()
            }
            
        # Capturamos el 402
        elif response.status_code == 402:
            datos_pago = response.json()
            return {
                "status": "payment_required",
                "instructions": datos_pago["payment_request"],
                "message": "Debes realizar este pago usando la red x402 para obtener los datos."
            }
            
        # Manejo de otros errores
        else:
            return {
                "status": "error",
                "message": f"Error del servidor: {response.status_code}"
            }
            
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "No se pudo conectar al servidor del proveedor. ¿Está encendido?"
        }