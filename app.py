import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from streamlit_option_menu import option_menu

# Importaciones de tus módulos
from modulos.ingesta_excel import cargar_inventario_excel
from modulos.motor_riesgo import MotorFinanciero
from modulos.cotizador import generar_cotizacion
from modulos.base_datos import inicializar_tablas, verificar_login, obtener_catalogo_completo, guardar_inventario_en_bd, registrar_usuario

# # ==========================================
# # 2. FUNCIÓN DEL BOT BCV AUTOMÁTICO
# # ==========================================
# @st.cache_data(ttl=43200) # Guarda el resultado en memoria por 12 horas (43200 segundos)
# def obtener_tasa_bcv_automatica():
#     url = "https://www.bcv.org.ve/"
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
#     try:
#         respuesta = requests.get(url, headers=headers, verify=False, timeout=3)
#         sopa = BeautifulSoup(respuesta.text, 'html.parser')
#         caja_dolar = sopa.find('div', id='dolar')
#         texto_tasa = caja_dolar.find('strong').text
#         tasa_limpia = float(texto_tasa.strip().replace(',', '.'))
#         return tasa_limpia
#     except Exception as e:
#         st.sidebar.error("Error de conexión con el BCV. Usando tasa de respaldo.")
#         return 600.0 # Tasa manual de emergencia por si la página del banco se cae

# # ==========================================
# # 3. INICIALIZACIÓN Y CONFIGURACIÓN
# # ==========================================
# st.set_page_config(page_title="Procurement VE", layout="wide")
# inicializar_tablas() 

# if 'usuario_activo' not in st.session_state:
#     st.session_state['usuario_activo'] = None
# if 'rol_activo' not in st.session_state:
#     st.session_state['rol_activo'] = None
# if 'id_usuario' not in st.session_state:
#     st.session_state['id_usuario'] = None
# if 'carrito' not in st.session_state:
#     st.session_state['carrito'] = {}
    
# # ==========================================
# # 4. BARRA DE NAVEGACIÓN SUPERIOR
# # ==========================================
# seleccion = option_menu(
#     menu_title=None, 
#     options=["Inicio", "Servicios", "Portafolio", "Acceso al Sistema"],
#     icons=["house", "briefcase", "book", "person-circle"], 
#     menu_icon="cast",
#     default_index=0,
#     orientation="horizontal",
#     styles={
#         "container": {"padding": "0!important", "background-color": "#575ec5"},
#         "icon": {"color": "orange", "font-size": "18px"}, 
#         "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
#         "nav-link-selected": {"background-color": "#02ab21"},
#     }
# )

# st.divider()

# # ==========================================
# # 5. ENRUTAMIENTO DE PÁGINAS
# # ==========================================

# if seleccion == "Inicio":
#     st.title("🏗️ Bienvenidos a Plataforma Procurement VE")
#     st.subheader("Optimizando la cadena de suministro para el sector construcción")
#     st.info("Aquí diseñaremos tu Landing Page de bienvenida.")

# elif seleccion == "Servicios":
#     st.title("💼 Nuestros Servicios")
#     st.write("Detalles de protección cambiaria, logística y B2B.")

# elif seleccion == "Portafolio":
#     st.title("📂 Portafolio y Aliados")
#     st.write("Casos de éxito y empresas que confían en nosotros.")

# elif seleccion == "Acceso al Sistema":

# # ==========================================
# # 6. PANTALLA DE ACCESO (LOGIN Y REGISTRO)
# # ==========================================
#  if st.session_state['usuario_activo'] is None:
#     st.title("🔐 Acceso a la Plataforma")
    
#     # Creamos dos pestañas visuales
#     tab_login, tab_registro = st.tabs(["Iniciar Sesión", "Crear Nueva Cuenta"])
    
#     # PESTAÑA 1: LOGIN
#     with tab_login:
#         with st.form("login_form"):
#             st.subheader("Ingresa tus credenciales")
#             user_log = st.text_input("Usuario")
#             pass_log = st.text_input("Contraseña", type="password")
#             submit_log = st.form_submit_button("Ingresar")
            
#             if submit_log:
#                 datos_usuario = verificar_login(user_log, pass_log)
#                 if datos_usuario:
#                     st.session_state['usuario_activo'] = datos_usuario['usuario']
#                     st.session_state['rol_activo'] = datos_usuario['rol']
#                     st.session_state['id_usuario'] = datos_usuario['id']
#                     st.rerun()
#                 else:
#                     st.error("Usuario o contraseña incorrectos.")

#     # PESTAÑA 2: REGISTRO
#     with tab_registro:
#         with st.form("registro_form"):
#             st.subheader("Regístrate en la plataforma")
#             user_reg = st.text_input("Crea un nombre de Usuario")
#             pass_reg = st.text_input("Crea una Contraseña", type="password")
#             rol_reg = st.selectbox("Selecciona tu perfil", ["Constructora", "Proveedor"])
#             submit_reg = st.form_submit_button("Registrarse")
            
#             if submit_reg:
#                 if user_reg and pass_reg: # Validamos que no envíen campos vacíos
#                     exito = registrar_usuario(user_reg, pass_reg, rol_reg)
#                     if exito:
#                         st.success("¡Cuenta creada exitosamente! Ahora puedes iniciar sesión en la otra pestaña.")
#                     else:
#                         st.error("Ese nombre de usuario ya está en uso. Intenta con otro.")
#                 else:
#                     st.warning("Debes llenar todos los campos.")

# # ==========================================
# # 7. PANTALLA PRINCIPAL
# # ==========================================
# else:
#     col_titulo, col_boton = st.columns([8, 2])
#     col_titulo.title(f"🏢 Bienvenido, {st.session_state['usuario_activo']} ({st.session_state['rol_activo']})")
    
#     if col_boton.button("Cerrar Sesión"):
#         st.session_state['usuario_activo'] = None
#         st.session_state['rol_activo'] = None
#         st.session_state['id_usuario'] = None
#         st.rerun()

#     st.divider()

#     # --- VISTA PROVEEDOR ---
#     if st.session_state['rol_activo'] == 'Proveedor':
#         st.subheader("📦 Panel de Gestión de Inventario")
#         st.write("Sube tu archivo de Excel para actualizar el catálogo disponible.")
#         archivo_subido = st.file_uploader("Actualiza tu inventario (.xlsx)", type=['xlsx'])
        
#         if archivo_subido is not None:
#             df_nuevo_inventario = cargar_inventario_excel(archivo_subido)
#             if df_nuevo_inventario is not None:
#                 st.success("Archivo verificado correctamente.")
#                 with st.expander("Ver vista previa del inventario"):
#                     st.dataframe(df_nuevo_inventario, use_container_width=True)
                
#                 if st.button("Guardar en Base de Datos Central"):
#                     guardar_inventario_en_bd(df_nuevo_inventario, st.session_state['id_usuario'])
#                     st.success("¡Inventario actualizado exitosamente en la bóveda digital!")
#             else:
#                 st.error("El archivo no tiene el formato correcto.")

#     # --- VISTA CONSTRUCTORA (COMPRADOR) ---
#     elif st.session_state['rol_activo'] == 'Constructora':
        
#         st.sidebar.header("⚙️ Variables Macroeconómicas")
        
#         # EL BOT EN ACCIÓN
#         tasa_oficial = obtener_tasa_bcv_automatica()
#         st.sidebar.success(f"Tasa BCV Automatizada: {tasa_oficial} Bs/USD")
        
#         # Permitimos sobreescribir la tasa manualmente si es estrictamente necesario
#         tasa_bcv_manual = st.sidebar.number_input("Tasa BCV a utilizar", value=tasa_oficial)
#         dias_pago = st.sidebar.slider("Días estimados para el pago", 0, 30, 5)
#         inflacion_mes = st.sidebar.number_input("Inflación mensual estimada USD (%)", value=3.0)

#         motor = MotorFinanciero(tasa_bcv_actual=tasa_bcv_manual, inflacion_mensual_estimada=inflacion_mes)

#         st.subheader("🛒 Catálogo Global y Cotizador Automático")
#         df_catalogo = obtener_catalogo_completo()
        
#         if df_catalogo.empty:
#             st.info("El catálogo está vacío actualmente. Los proveedores deben cargar mercancía.")
#         else:
#             st.dataframe(df_catalogo, use_container_width=True)
            
#             # --- SECCIÓN DE ARMAR PEDIDO ---
#             st.write("### 🛒 Armar Pedido (Carrito de Compras)")
            
#             # Input para añadir productos
#             col_input1, col_input2, col_input3 = st.columns([2, 1, 1])
#             with col_input1:
#                 sku_input = st.text_input("Código SKU del Material (Ej. CEM-01)")
#             with col_input2:
#                 cantidad_input = st.number_input("Cantidad", min_value=1, step=1)
#             with col_input3:
#                 st.write("") # Espaciador vertical
#                 st.write("")
#                 if st.button("➕ Añadir al Pedido"):
#                     if sku_input:
#                         sku_limpio = sku_input.strip().upper() 
                        
#                         # Validar si existe en el catálogo
#                         if sku_limpio in df_catalogo['SKU'].values:
#                             # Validar que no supere el stock disponible (Opcional pero recomendado)
#                             stock_actual = df_catalogo.loc[df_catalogo['SKU'] == sku_limpio, 'STOCK'].values[0]
                            
#                             if cantidad_input <= stock_actual:
#                                 if sku_limpio in st.session_state['carrito']:
#                                     st.session_state['carrito'][sku_limpio] += cantidad_input
#                                 else:
#                                     st.session_state['carrito'][sku_limpio] = cantidad_input
#                                 st.success(f"Añadido: {cantidad_input}x {sku_limpio}")
#                             else:
#                                 st.error(f"Stock insuficiente. Solo hay {stock_actual} unidades de {sku_limpio}.")
#                         else:
#                             st.error("Ese SKU no existe en el catálogo disponible.")
#                     else:
#                         st.warning("Por favor, ingresa un código SKU.")

#             # --- MOSTRAR EL CARRITO MEJORADO ---
#             if st.session_state['carrito']:
#                 st.divider()
#                 st.write("#### 📦 Tu Pedido Actual")
                
#                 # 1. Creamos los encabezados visuales del carrito
#                 col_h1, col_h2, col_h3, col_h4, col_h5, col_h6 = st.columns([1.5, 3, 1.5, 1.5, 1.5, 1])
#                 col_h1.write("**SKU**")
#                 col_h2.write("**Descripción**")
#                 col_h3.write("**Precio Unit. (USD)**")
#                 col_h4.write("**Cantidad**")
#                 col_h5.write("**Subtotal**")
#                 col_h6.write("**Acción**")
                
#                 st.markdown("---") # Línea divisoria sutil
                
#                 # 2. Iteramos sobre cada elemento del carrito para dibujarlo
#                 # Usamos list() para evitar errores si el diccionario cambia de tamaño durante el ciclo
#                 for sku, cantidad in list(st.session_state['carrito'].items()):
                    
#                     # Extraemos los datos cruzando con el catálogo
#                     datos_item = df_catalogo[df_catalogo['SKU'] == sku].iloc[0]
#                     material = datos_item['MATERIAL']
#                     precio_unitario = datos_item['PRECIO_USD']
#                     subtotal = precio_unitario * cantidad
                    
#                     # Dibujamos la fila
#                     col1, col2, col3, col4, col5, col6 = st.columns([1.5, 3, 1.5, 1.5, 1.5, 1])
#                     col1.write(f"`{sku}`")
#                     col2.write(material)
#                     col3.write(f"${precio_unitario:.2f}")
#                     col4.write(str(cantidad))
#                     col5.write(f"**${subtotal:.2f}**")
                    
#                     # Botón de eliminación individual
#                     # Importante: El 'key' debe ser único para cada botón, por eso usamos el SKU
#                     if col6.button("❌", key=f"eliminar_{sku}", help=f"Eliminar {sku} del carrito"):
#                         del st.session_state['carrito'][sku] # Borramos solo este ítem
#                         st.rerun() # Recargamos para actualizar la vista
                
#                 st.divider()
                
#                 # --- BOTONES DE ACCIÓN FINAL ---
#                 col_facturar, col_limpiar = st.columns(2)
                
#                 with col_facturar:
#                     if st.button("✅ Generar Factura Proforma Protegida", type="primary", use_container_width=True):
                        
#                         # 1. Generamos los cálculos matemáticos con tu motor
#                         resultados = generar_cotizacion(df_catalogo, st.session_state['carrito'], motor, dias_pago)
                        
#                         st.divider()
#                         st.subheader("🧾 Factura Proforma Detallada")
                        
#                         # 2. Dibujamos el encabezado de la factura sin tablas aburridas
#                         h1, h2, h3, h4, h5 = st.columns([3, 1, 1.5, 1.5, 1.5])
#                         h1.write("**🧱 Material**")
#                         h2.write("**📦 Cant.**")
#                         h3.write("**💲 Unit. (USD)**")
#                         h4.write("**💵 Subtotal (USD)**")
#                         h5.write("**🇻🇪 Subtotal (VES)**")
#                         st.markdown("---")
                        
#                         # 3. Calculamos la base cruda sin inflación para sacar la diferencia después
#                         total_base_usd = 0
                        
#                         # Dibujamos cada ítem de la factura
#                         for sku, cantidad in st.session_state['carrito'].items():
#                             datos_item = df_catalogo[df_catalogo['SKU'] == sku].iloc[0]
#                             material = datos_item['MATERIAL']
#                             precio_usd = datos_item['PRECIO_USD']
                            
#                             subtotal_usd = precio_usd * cantidad
#                             subtotal_ves = subtotal_usd * tasa_bcv_manual # Usamos la tasa que esté en el panel lateral
                            
#                             total_base_usd += subtotal_usd
                            
#                             # Imprimimos la fila de la factura
#                             f1, f2, f3, f4, f5 = st.columns([3, 1, 1.5, 1.5, 1.5])
#                             f1.write(f"{material} `({sku})`")
#                             f2.write(str(cantidad))
#                             f3.write(f"${precio_usd:.2f}")
#                             f4.write(f"${subtotal_usd:.2f}")
#                             f5.write(f"Bs. {subtotal_ves:.2f}")
                            
#                         st.divider()
                        
#                         # 4. Cálculos del Margen de Riesgo Inflacionario
#                         total_base_ves = total_base_usd * tasa_bcv_manual
#                         margen_riesgo_usd = resultados['Gran_Total_Obra_USD'] - total_base_usd
#                         margen_riesgo_ves = resultados['Gran_Total_Obra_VES'] - total_base_ves
                        
#                         # 5. Mostramos los Totales con sus "Deltas" (El indicador rojo/verde)
#                         st.write("### 📊 Resumen Financiero con Cobertura")
                        
#                         m1, m2 = st.columns(2)
                        
#                         # Usamos delta_color="inverse" para que el aumento (costo extra) salga en rojo
#                         m1.metric(
#                             label="Total Inversión Protegida (USD)", 
#                             value=f"${resultados['Gran_Total_Obra_USD']:.2f}", 
#                             delta=f"+ ${margen_riesgo_usd:.2f} (Margen de Riesgo a {dias_pago} días)",
#                             delta_color="inverse" 
#                         )
                        
#                         m2.metric(
#                             label="Total a Transferir (VES)", 
#                             value=f"Bs. {resultados['Gran_Total_Obra_VES']:.2f}", 
#                             delta=f"+ Bs. {margen_riesgo_ves:.2f} (Margen de Riesgo a {dias_pago} días)",
#                             delta_color="inverse"
#                         )
                        
#                         st.info("💡 Los subtotales en la lista muestran el precio base actual. Los totales generales incluyen la proyección financiera para proteger la operación.")
                        
# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA (Única al inicio)
# ==========================================
st.set_page_config(
    page_title="Procurement VE", 
    page_icon="🏗️",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. INYECCIÓN DE CSS (Ajuste al tope y diseño)
# ==========================================
st.markdown("""
    <style>
    /* Reducir el espacio superior en blanco al mínimo */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Ocultar/minimizar el encabezado nativo para pegar la barra al tope */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        height: 2rem !important;
    }
    
    /* Estilos visuales para las pestañas de Login */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 4px 4px 0px 0px;
    }
    </style>
""", unsafe_allow_html=True)

# Importaciones de tus módulos locales
from modulos.ingesta_excel import cargar_inventario_excel
from modulos.motor_riesgo import MotorFinanciero
from modulos.cotizador import generar_cotizacion
from modulos.base_datos import (
    inicializar_tablas, 
    verificar_login, 
    obtener_catalogo_completo, 
    guardar_inventario_en_bd, 
    registrar_usuario
)

# ==========================================
# 3. INICIALIZACIÓN DE BASE DE DATOS Y SESIÓN
# ==========================================
inicializar_tablas() 

if 'usuario_activo' not in st.session_state:
    st.session_state['usuario_activo'] = None
if 'rol_activo' not in st.session_state:
    st.session_state['rol_activo'] = None
if 'id_usuario' not in st.session_state:
    st.session_state['id_usuario'] = None
if 'carrito' not in st.session_state:
    st.session_state['carrito'] = {}

# ==========================================
# 4. FUNCIÓN DEL BOT BCV AUTOMÁTICO
# ==========================================
@st.cache_data(ttl=43200) # Guarda en memoria por 12 horas
def obtener_tasa_bcv_automatica():
    url = "https://www.bcv.org.ve/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        respuesta = requests.get(url, headers=headers, verify=False, timeout=3)
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        caja_dolar = sopa.find('div', id='dolar')
        texto_tasa = caja_dolar.find('strong').text
        tasa_limpia = float(texto_tasa.strip().replace(',', '.'))
        return tasa_limpia
    except Exception as e:
        st.sidebar.error("Error de conexión con el BCV. Usando tasa de respaldo.")
        return 600.0 # Tasa manual de emergencia

# ==========================================
# 5. BARRA DE NAVEGACIÓN SUPERIOR (Personalizada)
# ==========================================
# Cambiamos dinámicamente la última pestaña según si hay usuario logeado
texto_menu_acceso = f"Mi Panel ({st.session_state['usuario_activo']})" if st.session_state['usuario_activo'] else "Acceso al Sistema"

seleccion = option_menu(
    menu_title=None, 
    options=["Inicio", "Servicios", "Portafolio", texto_menu_acceso],
    icons=["house", "briefcase", "book", "person-circle"], 
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "3px!important", 
            "background-color": "#1E293B",  # Color azul oscuro corporativo / Slate
            "border-radius": "8px"
        },
        "icon": {"color": "#F59E0B", "font-size": "18px"},  # Iconos acento dorado
        "nav-link": {
            "font-size": "15px", 
            "text-align": "center", 
            "margin": "0px 4px", 
            "color": "#FFFFFF",
            "--hover-color": "#334155"
        },
        "nav-link-selected": {
            "background-color": "#2563EB",  # Azul activo al seleccionar
            "color": "white",
            "font-weight": "bold"
        },
    }
)

st.divider()

# ==========================================
# 6. ENRUTAMIENTO DE PÁGINAS
# ==========================================


if seleccion == "Inicio":
    # --- HERO SECTION (Banner principal) ---
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0rem;">
            <h1 style="color: #2563EB; font-size: 3.5rem; margin-bottom: 0;">Procurement VE</h1>
            <h3 style="color: #64748B; font-weight: 300;">El Sistema Operativo Logístico y Financiero para la Construcción en Venezuela.</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # --- PROPUESTA DE VALOR EN 3 PILARES ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h2 style='text-align: center;'>🛡️</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Riesgo Cero</h4>", unsafe_allow_html=True)
        st.write("Eliminamos la incertidumbre cambiaria. Congelamos precios y protegemos el capital mediante nuestro sistema de Custodia Inteligente (Escrow) hasta que el material llega a la obra.")
        
    with col2:
        st.markdown("<h2 style='text-align: center;'>⚡</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Fricción Cero</h4>", unsafe_allow_html=True)
        st.write("Cotiza, compara y compra en 3 clics. Sin llamadas interminables, sin PDFs desactualizados. Un ecosistema 100% digitalizado, transparente y auditable.")
        
    with col3:
        st.markdown("<h2 style='text-align: center;'>📈</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Futuro Cero Límites</h4>", unsafe_allow_html=True)
        st.write("Diseñados para escalar. Integramos IA para cálculos de materiales y trazabilidad logística en tiempo real. Construye hoy con la tecnología de la próxima década.")

    st.divider()

    # --- LLAMADO A LA ACCIÓN (CTA) ---
    st.markdown("### ¿Cómo funciona?")
    paso1, paso2, paso3, paso4 = st.columns(4)
    paso1.info("**1. Regístrate**\n\nCrea tu perfil como Proveedor (sube tu catálogo) o Constructora (accede a los precios).")
    paso2.warning("**2. Cotiza**\n\nArma tu carrito. El motor calcula tasas, inflación y tiempos de pago al instante.")
    paso3.error("**3. Paga Seguro**\n\nEl dinero se retiene de forma segura hasta que se confirma la entrega.")
    paso4.success("**4. Construye**\n\nRecibe los materiales y califica al proveedor. Todo centralizado.")


elif seleccion == "Servicios":
    st.title("💼 Ecosistema de Servicios Integrados")
    st.markdown("Hemos desglosado los problemas históricos del sector construcción venezolano y creado soluciones desde los **primeros principios**.")
    
    st.write("") # Espaciador
    
    # Usamos Pestañas (Tabs) para no saturar la pantalla con texto
    tab_escrow, tab_cobertura, tab_ia, tab_logistica = st.tabs([
        "🛡️ Smart Escrow B2B", 
        "💱 Cobertura Cambiaria", 
        "🤖 Cotizador IA", 
        "🚚 Logística Predictiva"
    ])
    
    with tab_escrow:
        st.subheader("Smart Escrow: Confianza Criptográfica en la Vida Real")
        col_text, col_img = st.columns([2, 1])
        col_text.write("""
        **El problema:** El comprador teme pagar por adelantado y no recibir el material. El proveedor teme despachar y no recibir el pago.
        
        **Nuestra solución:** Actuamos como un árbitro neutral automatizado. 
        1. La constructora transfiere los fondos a la bóveda de Procurement VE.
        2. El proveedor visualiza los fondos garantizados y despacha la mercancía.
        3. Cuando el material llega a la obra, el receptor valida la entrega con un código único y el sistema libera automáticamente el pago al proveedor.
        
        *Confianza total, sin burocracia.*
        """)
        col_img.info("### 🔒 100%\nFondos Garantizados para ambas partes.")
        
    with tab_cobertura:
        st.subheader("Motor de Riesgo y Cobertura Inflacionaria")
        st.write("En un entorno multimoneda, un día de retraso en el pago puede significar pérdidas masivas. Nuestro Motor Financiero analiza en tiempo real:")
        st.markdown("""
        *   Tasa BCV del día sincronizada automáticamente.
        *   Proyecciones de inflación mensual parametrizables.
        *   Cálculo automático del **Margen de Riesgo** según los días de crédito otorgados.
        
        Tus facturas proforma salen "blindadas". Sabes exactamente cuántos Bolívares transferir hoy para garantizar el valor en Dólares mañana.
        """)
        
    with tab_ia:
        st.subheader("Siri para tu Obra: Asistente de Cómputos (Próximamente)")
        st.write("En el futuro cercano, no buscarás 'Sacos de Cemento'. Le dirás a la plataforma: *'Necesito construir un muro perimetral de 50 metros de largo por 2 de alto'*.")
        st.write("Nuestra IA cruzará la física de materiales con nuestro catálogo en vivo para generar tu carrito de compras exacto, minimizando desperdicios y optimizando tu presupuesto.")
        
    with tab_logistica:
        st.subheader("Trazabilidad Visual")
        st.write("Adiós al 'el camión ya va en camino'. Integraremos visibilidad de despachos en tiempo real. Sabrás qué material viene, quién lo trae y a qué hora llega, reduciendo los tiempos muertos de tus cuadrillas en obra.")


elif seleccion == "Portafolio":
    st.title("🤝 El Ecosistema de Confianza")
    st.write("Plataforma Procurement VE no es solo software, es una red de los actores más serios y profesionales del sector.")
    
    # --- MÉTRICAS DE IMPACTO (Simuladas para el diseño visual) ---
    st.markdown("### El Impacto de Digitalizar las Compras")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tiempo de Cotización", "15 min", "-72 hrs de espera", delta_color="inverse")
    m2.metric("Riesgo Cambiario Asumido", "0%", "-15% promedio", delta_color="inverse")
    m3.metric("Proveedores Verificados", "24+", "+3 este mes")
    m4.metric("Precisión de Despachos", "99.8%", "+12%")
    
    st.divider()
    
    # --- ALIADOS / CASOS DE ÉXITO ---
    st.markdown("### ¿Quiénes construyen con nosotros?")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.info("""
        **🏗️ "Constructora Visión 2030"**
        
        *"Antes perdíamos hasta 3 días comparando presupuestos por WhatsApp que vencían en horas por el tipo de cambio. Con Procurement VE, armamos el pedido, bloqueamos el precio y despachan al día siguiente. Revolucionaron nuestra operatividad administrativa."*
        """)
        
    with col_a2:
        st.success("""
        **🧱 "Agregados y Cementos del Centro" (Proveedor)**
        
        *"El sistema de pagos protegidos nos permitió abrir líneas de crédito a constructoras nuevas sin riesgo. Sabemos que si despachamos, el dinero ya está garantizado en la plataforma. Hemos aumentado nuestras ventas corporativas un 40%."*
        """)

elif seleccion == texto_menu_acceso:

    # --------------------------------------
    # A. SI NO HA INICIADO SESIÓN (LOGIN Y REGISTRO)
    # --------------------------------------
    if st.session_state['usuario_activo'] is None:
        st.title("🔐 Acceso a la Plataforma")
        
        tab_login, tab_registro = st.tabs(["Iniciar Sesión", "Crear Nueva Cuenta"])
        
        # PESTAÑA 1: LOGIN
        with tab_login:
            with st.form("login_form"):
                st.subheader("Ingresa tus credenciales")
                user_log = st.text_input("Usuario")
                pass_log = st.text_input("Contraseña", type="password")
                submit_log = st.form_submit_button("Ingresar")
                
                if submit_log:
                    datos_usuario = verificar_login(user_log, pass_log)
                    if datos_usuario:
                        st.session_state['usuario_activo'] = datos_usuario['usuario']
                        st.session_state['rol_activo'] = datos_usuario['rol']
                        st.session_state['id_usuario'] = datos_usuario['id']
                        st.success("¡Acceso correcto! Redirigiendo...")
                        st.rerun() # Descongela y recarga la interfaz
                    else:
                        st.error("Usuario o contraseña incorrectos.")

        # PESTAÑA 2: REGISTRO
        with tab_registro:
            with st.form("registro_form"):
                st.subheader("Regístrate en la plataforma")
                user_reg = st.text_input("Crea un nombre de Usuario")
                pass_reg = st.text_input("Crea una Contraseña", type="password")
                rol_reg = st.selectbox("Selecciona tu perfil", ["Constructora", "Proveedor"])
                submit_reg = st.form_submit_button("Registrarse")
                
                if submit_reg:
                    if user_reg and pass_reg:
                        exito = registrar_usuario(user_reg, pass_reg, rol_reg)
                        if exito:
                            st.success("¡Cuenta creada exitosamente! Ahora puedes iniciar sesión en la otra pestaña.")
                        else:
                            st.error("Ese nombre de usuario ya está en uso. Intenta con otro.")
                    else:
                        st.warning("Debes llenar todos los campos.")

    # --------------------------------------
    # B. SI YA INICIÓ SESIÓN (PANEL PRINCIPAL)
    # --------------------------------------
    else:
        col_titulo, col_boton = st.columns([8, 2])
        col_titulo.title(f"🏢 Bienvenido, {st.session_state['usuario_activo']} ({st.session_state['rol_activo']})")
        
        if col_boton.button("🚪 Cerrar Sesión"):
            st.session_state['usuario_activo'] = None
            st.session_state['rol_activo'] = None
            st.session_state['id_usuario'] = None
            st.session_state['carrito'] = {}
            st.rerun()

        st.divider()

        # --- VISTA PROVEEDOR ---
        if st.session_state['rol_activo'] == 'Proveedor':
            st.subheader("📦 Panel de Gestión de Inventario")
            st.write("Sube tu archivo de Excel para actualizar el catálogo disponible.")
            archivo_subido = st.file_uploader("Actualiza tu inventario (.xlsx)", type=['xlsx'])
            
            if archivo_subido is not None:
                df_nuevo_inventario = cargar_inventario_excel(archivo_subido)
                if df_nuevo_inventario is not None:
                    st.success("Archivo verificado correctamente.")
                    with st.expander("Ver vista previa del inventario"):
                        st.dataframe(df_nuevo_inventario, use_container_width=True)
                    
                    if st.button("Guardar en Base de Datos Central"):
                        guardar_inventario_en_bd(df_nuevo_inventario, st.session_state['id_usuario'])
                        st.success("¡Inventario actualizado exitosamente en la bóveda digital!")
                else:
                    st.error("El archivo no tiene el formato correcto.")

        # --- VISTA CONSTRUCTORA (COMPRADOR) ---
        elif st.session_state['rol_activo'] == 'Constructora':
            
            st.sidebar.header("⚙️ Variables Macroeconómicas")
            
            tasa_oficial = obtener_tasa_bcv_automatica()
            st.sidebar.success(f"Tasa BCV Automatizada: {tasa_oficial} Bs/USD")
            
            tasa_bcv_manual = st.sidebar.number_input("Tasa BCV a utilizar", value=tasa_oficial)
            dias_pago = st.sidebar.slider("Días estimados para el pago", 0, 30, 5)
            inflacion_mes = st.sidebar.number_input("Inflación mensual estimada USD (%)", value=3.0)

            motor = MotorFinanciero(tasa_bcv_actual=tasa_bcv_manual, inflacion_mensual_estimada=inflacion_mes)

            st.subheader("🛒 Catálogo Global y Cotizador Automático")
            df_catalogo = obtener_catalogo_completo()
            
            if df_catalogo.empty:
                st.info("El catálogo está vacío actualmente. Los proveedores deben cargar mercancía.")
            else:
                st.dataframe(df_catalogo, use_container_width=True)
                
                # --- SECCIÓN DE ARMAR PEDIDO ---
                st.write("### 🛒 Armar Pedido (Carrito de Compras)")
                
                col_input1, col_input2, col_input3 = st.columns([2, 1, 1])
                with col_input1:
                    sku_input = st.text_input("Código SKU del Material (Ej. CEM-01)")
                with col_input2:
                    cantidad_input = st.number_input("Cantidad", min_value=1, step=1)
                with col_input3:
                    st.write("") 
                    st.write("")
                    if st.button("➕ Añadir al Pedido"):
                        if sku_input:
                            sku_limpio = sku_input.strip().upper() 
                            
                            if sku_limpio in df_catalogo['SKU'].values:
                                stock_actual = df_catalogo.loc[df_catalogo['SKU'] == sku_limpio, 'STOCK'].values[0]
                                
                                if cantidad_input <= stock_actual:
                                    if sku_limpio in st.session_state['carrito']:
                                        st.session_state['carrito'][sku_limpio] += cantidad_input
                                    else:
                                        st.session_state['carrito'][sku_limpio] = cantidad_input
                                    st.success(f"Añadido: {cantidad_input}x {sku_limpio}")
                                else:
                                    st.error(f"Stock insuficiente. Solo hay {stock_actual} unidades de {sku_limpio}.")
                            else:
                                st.error("Ese SKU no existe en el catálogo disponible.")
                        else:
                            st.warning("Por favor, ingresa un código SKU.")

                # --- MOSTRAR EL CARRITO MEJORADO ---
                if st.session_state['carrito']:
                    st.divider()
                    st.write("#### 📦 Tu Pedido Actual")
                    
                    col_h1, col_h2, col_h3, col_h4, col_h5, col_h6 = st.columns([1.5, 3, 1.5, 1.5, 1.5, 1])
                    col_h1.write("**SKU**")
                    col_h2.write("**Descripción**")
                    col_h3.write("**Precio Unit. (USD)**")
                    col_h4.write("**Cantidad**")
                    col_h5.write("**Subtotal**")
                    col_h6.write("**Acción**")
                    
                    st.markdown("---")
                    
                    for sku, cantidad in list(st.session_state['carrito'].items()):
                        datos_item = df_catalogo[df_catalogo['SKU'] == sku].iloc[0]
                        material = datos_item['MATERIAL']
                        precio_unitario = datos_item['PRECIO_USD']
                        subtotal = precio_unitario * cantidad
                        
                        col1, col2, col3, col4, col5, col6 = st.columns([1.5, 3, 1.5, 1.5, 1.5, 1])
                        col1.write(f"`{sku}`")
                        col2.write(material)
                        col3.write(f"${precio_unitario:.2f}")
                        col4.write(str(cantidad))
                        col5.write(f"**${subtotal:.2f}**")
                        
                        if col6.button("❌", key=f"eliminar_{sku}", help=f"Eliminar {sku} del carrito"):
                            del st.session_state['carrito'][sku]
                            st.rerun()
                    
                    st.divider()
                    
                    # --- BOTONES DE ACCIÓN FINAL ---
                    col_facturar, col_limpiar = st.columns(2)
                    
                    with col_facturar:
                        if st.button("✅ Generar Factura Proforma Protegida", type="primary", use_container_width=True):
                            resultados = generar_cotizacion(df_catalogo, st.session_state['carrito'], motor, dias_pago)
                            
                            st.divider()
                            st.subheader("🧾 Factura Proforma Detallada")
                            
                            h1, h2, h3, h4, h5 = st.columns([3, 1, 1.5, 1.5, 1.5])
                            h1.write("**🧱 Material**")
                            h2.write("**📦 Cant.**")
                            h3.write("**💲 Unit. (USD)**")
                            h4.write("**💵 Subtotal (USD)**")
                            h5.write("**🇻🇪 Subtotal (VES)**")
                            st.markdown("---")
                            
                            total_base_usd = 0
                            
                            for sku, cantidad in st.session_state['carrito'].items():
                                datos_item = df_catalogo[df_catalogo['SKU'] == sku].iloc[0]
                                material = datos_item['MATERIAL']
                                precio_usd = datos_item['PRECIO_USD']
                                
                                subtotal_usd = precio_usd * cantidad
                                subtotal_ves = subtotal_usd * tasa_bcv_manual
                                
                                total_base_usd += subtotal_usd
                                
                                f1, f2, f3, f4, f5 = st.columns([3, 1, 1.5, 1.5, 1.5])
                                f1.write(f"{material} `({sku})`")
                                f2.write(str(cantidad))
                                f3.write(f"${precio_usd:.2f}")
                                f4.write(f"${subtotal_usd:.2f}")
                                f5.write(f"Bs. {subtotal_ves:.2f}")
                                
                            st.divider()
                            
                            total_base_ves = total_base_usd * tasa_bcv_manual
                            margen_riesgo_usd = resultados['Gran_Total_Obra_USD'] - total_base_usd
                            margen_riesgo_ves = resultados['Gran_Total_Obra_VES'] - total_base_ves
                            
                            st.write("### 📊 Resumen Financiero con Cobertura")
                            
                            m1, m2 = st.columns(2)
                            
                            m1.metric(
                                label="Total Inversión Protegida (USD)", 
                                value=f"${resultados['Gran_Total_Obra_USD']:.2f}", 
                                delta=f"+ ${margen_riesgo_usd:.2f} (Margen de Riesgo a {dias_pago} días)",
                                delta_color="inverse" 
                            )
                            
                            m2.metric(
                                label="Total a Transferir (VES)", 
                                value=f"Bs. {resultados['Gran_Total_Obra_VES']:.2f}", 
                                delta=f"+ Bs. {margen_riesgo_ves:.2f} (Margen de Riesgo a {dias_pago} días)",
                                delta_color="inverse"
                            )
                            
                            st.info("💡 Los subtotales en la lista muestran el precio base actual. Los totales generales incluyen la proyección financiera para proteger la operación.")