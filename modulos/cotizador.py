import pandas as pd
from modulos.motor_riesgo import MotorFinanciero

def generar_cotizacion(df_inventario, requerimientos, motor_financiero, dias_pago):
    """
    Cruza los requerimientos del cliente con el inventario del proveedor y aplica el riesgo cambiario.
    
    df_inventario: DataFrame de Pandas con el inventario del proveedor.
    requerimientos: Diccionario con formato {'SKU_MATERIAL': Cantidad_Necesitada}.
    motor_financiero: Instancia de la clase MotorFinanciero.
    """
    if df_inventario is None or df_inventario.empty:
        return {"error": "El inventario proporcionado está vacío o es inválido."}

    resultados_cotizacion = []
    costo_total_obra_usd = 0.0

    for sku_requerido, cantidad_requerida in requerimientos.items():
        # Buscamos el material en el DataFrame del proveedor
        material_encontrado = df_inventario[df_inventario['SKU'] == sku_requerido]
        
        if not material_encontrado.empty:
            datos_material = material_encontrado.iloc[0]
            stock_disponible = datos_material['STOCK']
            
            if stock_disponible >= cantidad_requerida:
                precio_unitario_usd = datos_material['PRECIO_USD']
                
                # Pasamos el precio por nuestro motor de riesgo
                calculo_financiero = motor_financiero.proyectar_costo_real(precio_unitario_usd, dias_pago)
                
                costo_total_item = calculo_financiero["precio_ajustado_usd"] * cantidad_requerida
                costo_total_obra_usd += costo_total_item
                
                resultados_cotizacion.append({
                    "SKU": sku_requerido,
                    "Material": datos_material['MATERIAL'],
                    "Cantidad": cantidad_requerida,
                    "Precio_Unitario_Ajustado_USD": calculo_financiero["precio_ajustado_usd"],
                    "Subtotal_USD": round(costo_total_item, 2)
                })
            else:
                resultados_cotizacion.append({
                    "SKU": sku_requerido,
                    "Error": f"Stock insuficiente. Requerido: {cantidad_requerida}, Disponible: {stock_disponible}"
                })
        else:
             resultados_cotizacion.append({
                 "SKU": sku_requerido,
                 "Error": "Material no encontrado en el inventario del proveedor."
             })

    return {
        "Detalles_Materiales": resultados_cotizacion,
        "Gran_Total_Obra_USD": round(costo_total_obra_usd, 2),
        "Gran_Total_Obra_VES": round(costo_total_obra_usd * motor_financiero.tasa_bcv, 2)
    }