import streamlit as st
import sys
import os

# Asegurar que encuentre la carpeta raíz para las importaciones
sys.path.insert(0, os.path.dirname(__file__))

# 1. DICCIONARIO DE IDIOMAS
LANGUAGES = {
    "Español": {
        "page_title": "Moralogy Engine: Auditoría de Decisiones",
        "title": "⚖️ Moralogy Engine: Evaluación de Consistencia",
        "config_header": "Configuración",
        "lang_select": "Seleccionar Idioma",
        "model_info": "Modelo activo:",
        "agentes_label": "Participantes:",
        "situacion_label": "Escenario:",
        "contexto_label": "Opciones:",
        "btn_ejecutar": "Ejecutar Protocolo Moralogy",
        "spinner_text": "Analizando con Gemini...",
        "error_motor": "Falta el archivo motor_logico.py:",
        "footer_msg": "Nueva API Key detectada y operativa."
    },
    "English": {
        "page_title": "Moralogy Engine: Decision Audit",
        "title": "⚖️ Moralogy Engine: Consistency Evaluation",
        "config_header": "Configuration",
        "lang_select": "Select Language",
        "model_info": "Active model:",
        "agentes_label": "Participants:",
        "situacion_label": "Scenario:",
        "contexto_label": "Options:",
        "btn_ejecutar": "Execute Moralogy Protocol",
        "spinner_text": "Analyzing with Gemini...",
        "error_motor": "Missing motor_logico.py file:",
        "footer_msg": "New API Key detected and operational."
    }
}

# 2. SELECCIÓN DE IDIOMA EN SIDEBAR
with st.sidebar:
    st.subheader("🌐 Language / Idioma")
    sel_lang = st.selectbox("", list(LANGUAGES.keys()))
    t = LANGUAGES[sel_lang]  # 't' de traducción

st.set_page_config(
    page_title=t["page_title"],
    page_icon="⚖️",
    layout="wide"
)

# 3. CARGA DEL MOTOR LÓGICO (Mantenido integro)
try:
    from motor_logico import ejecutar_auditoria
    MOTOR_OK = True
except ImportError as e:
    MOTOR_OK = False
    import_error = str(e)

st.title(t["title"])

if not MOTOR_OK:
    st.error(f"{t['error_motor']} {import_error}")
    st.stop()

# 4. CONFIGURACIÓN DEL MODELO (Visualización en Sidebar)
with st.sidebar:
    st.subheader(t["config_header"])
    # Se mantiene la referencia a Gemini 1.5 Flash para estabilidad de cuota
    modelo_seleccionado = "gemini-1.5-flash" 
    st.info(f"{t['model_info']} {modelo_seleccionado}")
    st.success(t["footer_msg"])

# 5. INTERFAZ DINÁMICA
col1, col2 = st.columns([2, 1])
with col1:
    agentes = st.text_input(t["agentes_label"])
    situacion = st.text_area(t["situacion_label"])
    contexto = st.text_area(t["contexto_label"])

# 6. LÓGICA DE EJECUCIÓN (Se mantiene íntegra)
if st.button(t["btn_ejecutar"], type="primary"):
    with st.spinner(t["spinner_text"]):
        # Pasamos los parámetros tal como ya funcionaban en tu motor
        resultado = ejecutar_auditoria(agentes, situacion, contexto, "General", "Rápido")
        st.markdown(resultado)
