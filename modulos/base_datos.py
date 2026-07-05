import sqlite3
import pandas as pd

def conectar_db():
    # Crea un archivo 'plataforma.db' en la raíz de tu proyecto
    return sqlite3.connect('plataforma.db')

def inicializar_tablas():
    """Crea las tablas si no existen en la primera ejecución."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL -- Puede ser 'Proveedor' o 'Constructora'
        )
    ''')
    
    # Tabla de Inventario Global
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            sku TEXT PRIMARY KEY,
            proveedor_id INTEGER,
            material TEXT NOT NULL,
            precio_usd REAL NOT NULL,
            stock INTEGER NOT NULL,
            FOREIGN KEY(proveedor_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Insertar usuarios de prueba por defecto si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (usuario, password, rol) VALUES ('epa', '1234', 'Proveedor')")
        cursor.execute("INSERT INTO usuarios (usuario, password, rol) VALUES ('constructora_alfa', '1234', 'Constructora')")
    
    conexion.commit()
    conexion.close()

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

def guardar_inventario_en_bd(df_inventario, proveedor_id):
    """
    Recibe un DataFrame de Pandas y lo guarda en la tabla 'inventario' de SQLite.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Recorremos cada fila del Excel
    for indice, fila in df_inventario.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO inventario (sku, proveedor_id, material, precio_usd, stock)
            VALUES (?, ?, ?, ?, ?)
        ''', (fila['SKU'], proveedor_id, fila['MATERIAL'], fila['PRECIO_USD'], fila['STOCK']))
        
    conexion.commit()
    conexion.close()

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