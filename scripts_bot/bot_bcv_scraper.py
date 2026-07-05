import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def actualizar_tasa_bcv():
    """
    Entra a la web del BCV, extrae el precio del dólar y lo guarda en un historial.
    """
    url = "https://www.bcv.org.ve/"
    
    # Le decimos al banco que somos un navegador real (Mozilla), no un robot malicioso, 
    # para que no nos bloquee el acceso.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        print("[BOT] Conectando con el Banco Central de Venezuela...")
        # Entramos a la página (verify=False evita errores si el candado de seguridad del banco falla)
        respuesta = requests.get(url, headers=headers, verify=False, timeout=10)
        
        # Parseamos (traducimos) el código fuente de la página
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Buscamos específicamente la caja que contiene el dólar (Esta es la etiqueta HTML del BCV)
        caja_dolar = sopa.find('div', id='dolar')
        texto_tasa = caja_dolar.find('strong').text
        
        # Limpiamos el texto: quitamos espacios y cambiamos la coma por un punto matemático
        tasa_limpia = float(texto_tasa.strip().replace(',', '.'))
        fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[BOT] Éxito. Tasa encontrada: {tasa_limpia} Bs/$")
        
        # --- GUARDAR EN LA LIBRETA (CSV) ---
        ruta_csv = "datos/historico_bcv.csv"
        nuevo_dato = pd.DataFrame({"Fecha": [fecha_hoy], "Tasa_USD": [tasa_limpia]})
        
        # Si el archivo ya existe, lo abrimos y le agregamos la fila abajo. Si no, lo creamos.
        if os.path.exists(ruta_csv):
            nuevo_dato.to_csv(ruta_csv, mode='a', header=False, index=False)
        else:
            nuevo_dato.to_csv(ruta_csv, index=False)
            
        print("[BOT] Tasa guardada en el historial correctamente.")
        return tasa_limpia

    except Exception as e:
        print(f"[BOT ERROR] Hubo un problema al leer el BCV: {e}")
        return None

# Ordenamos al bot ejecutar la función al correr el script
if __name__ == "__main__":
    actualizar_tasa_bcv()