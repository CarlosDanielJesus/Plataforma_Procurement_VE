
from modulos.ingesta_excel import cargar_inventario_excel
from modulos.motor_riesgo import MotorFinanciero
from modulos.cotizador import generar_cotizacion

print("\n" + "="*40)
print("INICIANDO PRUEBA DEL CEREBRO DEL SISTEMA")
print("="*40)

# --- 1. PROBANDO EL MÓDULO DE INGESTA DE EXCEL ---
ruta_excel = "datos/inventarios_ejemplo/prov_prueba.xlsx"
print(f"\n[1] Intentando leer el archivo de inventario: {ruta_excel}")

df_inventario = cargar_inventario_excel(ruta_excel)

if df_inventario is not None:
    print("    ¡Éxito! El Excel se leyó correctamente. Así se ve por dentro:")
    print(df_inventario) # Esto imprimirá la tabla en la consola
else:
    print("    [ERROR CRÍTICO] No se pudo leer el Excel. Deteniendo la prueba.")
    exit() # Si falla aquí, apagamos el programa.

# --- 2. PROBANDO EL MOTOR FINANCIERO Y DE RIESGO ---
print("\n[2] Encendiendo el Motor de Riesgo Cambiario...")
tasa_oficial_hoy = 41.50   # Simulamos que fuimos a la página del BCV
inflacion_mensual = 3.0    # Estimado de inflación en USD
dias_para_pago = 5         # Simulamos que la constructora pagará el viernes (en 5 días)

# Creamos al "matemático" del programa
motor = MotorFinanciero(tasa_bcv_actual=tasa_oficial_hoy, inflacion_mensual_estimada=inflacion_mensual)
print(f"    Tasa BCV del día fijada en: {tasa_oficial_hoy} Bs/$")
print(f"    Riesgo calculado para {dias_para_pago} días: {motor.calcular_factor_cobertura(dias_para_pago)}")

# --- 3. PROBANDO EL COTIZADOR AUTOMÁTICO ---
print("\n[3] Cruzando datos (Lista de compras del cliente vs Inventario del proveedor)...")

# Simulamos lo que pediría el ingeniero de la obra en la página web
lista_de_compras_obra = {
    "CEM-01": 100,  # Quiere 100 sacos de cemento (Sí hay stock)
    "VIG-01": 100,  # Quiere 100 vigas (¡Ojo! En el Excel solo pusimos 50, debe dar error)
    "TUBO-X": 20    # Quiere un tubo que NO existe en el Excel (Debe dar error)
}

# Ejecutamos la función final
factura_final = generar_cotizacion(
    df_inventario=df_inventario,
    requerimientos=lista_de_compras_obra,
    motor_financiero=motor,
    dias_pago=dias_para_pago
)

# --- 4. IMPRIMIENDO LA FACTURA FINAL ---
print("\n" + "="*40)
print("        FACTURA PROFORMA PROTEGIDA")
print("="*40)

# Recorremos la lista de resultados para mostrarlos bonitos
for articulo in factura_final["Detalles_Materiales"]:
    if "Error" in articulo:
         print(f"[ALERTA] Material {articulo['SKU']}: {articulo['Error']}")
    else:
         print(f"[COMPRA] {articulo['Cantidad']}x {articulo['Material']}")
         print(f"         Precio Protegido: ${articulo['Precio_Unitario_Ajustado_USD']} c/u | Subtotal: ${articulo['Subtotal_USD']}")

print("-" * 40)
print(f"TOTAL INVERSIÓN (Protegida en USD): ${factura_final['Gran_Total_Obra_USD']}")
print(f"TOTAL A TRANSFERIR (En Bolívares): Bs. {factura_final['Gran_Total_Obra_VES']}")
print("="*40 + "\n")

#.\venv\Scripts\activate