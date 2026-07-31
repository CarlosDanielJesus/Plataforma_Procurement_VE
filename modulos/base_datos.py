import sqlite3
import pandas as pd

def conectar_db():
    # Crea un archivo 'plataforma.db' en la raíz de tu proyecto
    return sqlite3.connect('plataforma.db')

def inicializar_tablas():
    conn = sqlite3.connect('procurement.db')
    cursor = conn.cursor()
    
    # Tabla de Usuarios (La que ya tienes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            password TEXT,
            rol TEXT
        )
    ''')
    
    # Tabla de Inventario (¡Asegúrate de que tenga proveedor_id!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT,
            material TEXT,
            precio_usd REAL,
            stock INTEGER,
            proveedor_id INTEGER,
            FOREIGN KEY(proveedor_id) REFERENCES usuarios(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def verificar_login(usuario, password):
    """Busca al usuario en la base de datos y retorna su rol si la clave es correcta."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, rol FROM usuarios WHERE usuario=? AND password=?", (usuario, password))
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado:
        return {"id": resultado[0], "rol": resultado[1], "usuario": usuario}
    return None

def obtener_catalogo_completo():
    """Extrae todo el inventario de la base de datos para mostrarlo a los compradores."""
    conexion = conectar_db()
    df = pd.read_sql_query("SELECT sku AS SKU, material AS MATERIAL, precio_usd AS PRECIO_USD, stock AS STOCK FROM inventario", conexion)
    conexion.close()
    return df   

def guardar_inventario_en_bd(df_inventario, proveedor_id, actualizar=False):
    """
    Guarda o actualiza el inventario en la base de datos.
    - Si actualizar=False: Borra el inventario anterior de este proveedor y carga el nuevo de cero.
    - Si actualizar=True: Busca si el SKU existe. Si existe, actualiza precio y stock. Si no, lo añade.
    """
    # 1. Conexión a tu base de datos (Asegúrate de que el nombre del archivo .db sea el que ya usabas)
    conn = sqlite3.connect('procurement.db') 
    cursor = conn.cursor()

    if actualizar:
        # --- MODO 1: ACTUALIZAR INVENTARIO EXISTENTE ---
        for index, fila in df_inventario.iterrows():
            # Intentamos actualizar primero (por si el SKU ya existe para este proveedor)
            cursor.execute("""
                UPDATE inventario 
                SET material = ?, precio_usd = ?, stock = ?
                WHERE sku = ? AND proveedor_id = ?
            """, (fila['MATERIAL'], fila['PRECIO_USD'], fila['STOCK'], fila['SKU'], proveedor_id))
            
            # Si rowcount es 0, significa que no actualizó nada (el SKU es nuevo)
            # Entonces, procedemos a insertarlo como un material nuevo
            if cursor.rowcount == 0:
                cursor.execute("""
                    INSERT INTO inventario (sku, material, precio_usd, stock, proveedor_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (fila['SKU'], fila['MATERIAL'], fila['PRECIO_USD'], fila['STOCK'], proveedor_id))

    else:
        # --- MODO 2: CARGAR INVENTARIO NUEVO (Reemplazo total) ---
        # Borramos TODOS los materiales que pertenezcan a este proveedor
        cursor.execute("DELETE FROM inventario WHERE proveedor_id = ?", (proveedor_id,))
        
        # Insertamos el Excel nuevo completo
        for index, fila in df_inventario.iterrows():
            cursor.execute("""
                INSERT INTO inventario (sku, material, precio_usd, stock, proveedor_id)
                VALUES (?, ?, ?, ?, ?)
            """, (fila['SKU'], fila['MATERIAL'], fila['PRECIO_USD'], fila['STOCK'], proveedor_id))

    # Guardamos los cambios y cerramos la conexión
    conn.commit()
    conn.close()

def registrar_usuario(usuario, password, rol):
    """
    Intenta registrar un nuevo usuario en la base de datos.
    Retorna True si fue exitoso, o False si el usuario ya existe.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    try:
        # Intentamos insertar el nuevo registro
        cursor.execute("INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)", (usuario, password, rol))
        conexion.commit()
        exito = True
    except sqlite3.IntegrityError:
        # Si el usuario ya existe, SQLite lanza un IntegrityError porque la columna 'usuario' es UNIQUE
        exito = False
    finally:
        conexion.close()
        
    return exito