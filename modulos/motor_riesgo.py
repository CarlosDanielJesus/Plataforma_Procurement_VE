class MotorFinanciero:
    def __init__(self, tasa_bcv_actual, inflacion_mensual_estimada):
        """
        Inicializa el motor con los datos macroeconómicos del momento.
        """
        self.tasa_bcv = tasa_bcv_actual
        # Calculamos la inflación diaria estimada
        self.inflacion_diaria = inflacion_mensual_estimada / 30.0

    def calcular_factor_cobertura(self, dias_para_pago):
        """
        Calcula un multiplicador para proteger el precio base en dólares.
        """
        if dias_para_pago <= 0:
            return 1.0  # Pago de contado inmediato, no hay riesgo.
        
        # Aplicamos la fórmula de interés compuesto para el riesgo diario
        factor = (1 + (self.inflacion_diaria / 100)) ** dias_para_pago
        return round(factor, 4)

    def proyectar_costo_real(self, precio_base_usd, dias_para_pago):
        """
        Retorna un diccionario con el precio ajustado al riesgo y su equivalente en Bolívares.
        """
        factor = self.calcular_factor_cobertura(dias_para_pago)
        precio_ajustado_usd = precio_base_usd * factor
        precio_en_bolivares = precio_ajustado_usd * self.tasa_bcv
        
        return {
            "precio_base_usd": round(precio_base_usd, 2),
            "precio_ajustado_usd": round(precio_ajustado_usd, 2),
            "precio_total_ves": round(precio_en_bolivares, 2),
            "margen_cobertura_usd": round(precio_ajustado_usd - precio_base_usd, 2)
        }