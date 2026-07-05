import pandas as pd

def cargar_inventario_excel(ruta_archivo):
    """
    Lee un archivo Excel y verifica que tenga la estructura correcta.
    Retorna un DataFrame de Pandas o None si hay un error.
    """
    columnas_requeridas = ['SKU', 'Material', 'Precio_USD', 'Stock']
    
    try:
        # Intentamos leer el archivo Excel
        df = pd.read_excel(ruta_archivo)
        
        # Limpiamos los nombres de las columnas (quitamos espacios y ponemos en mayúsculas)
        df.columns = df.columns.str.strip().str.upper()
        columnas_requeridas_upper = [col.upper() for col in columnas_requeridas]
        
        # Validamos que todas las columnas necesarias existan
        for col in columnas_requeridas_upper:
            if col not in df.columns:
                # Si falta una columna, forzamos un error a propósito
                raise ValueError(f"Falta la columna obligatoria: {col}")
        
        # Si todo está bien, aseguramos que los números sean números y no texto
        df['PRECIO_USD'] = pd.to_numeric(df['PRECIO_USD'], errors='coerce')
        df['STOCK'] = pd.to_numeric(df['STOCK'], errors='coerce').fillna(0)
        
        return df

    except FileNotFoundError:
        print(f"[Error] No se encontró el archivo en la ruta: {ruta_archivo}")
        return None
    except ValueError as error_valor:
        print(f"[Error de Formato] El Excel no tiene la estructura correcta. Detalles: {error_valor}")
        return None
    except Exception as e:
        print(f"[Error Inesperado] Ocurrió un problema al leer el Excel: {e}")
        return None 
    
