# pages/03_Analisis_Avanzado.py
import streamlit as st
import sys
import os

# Configuración de rutas y motor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from motor_logico import procesar_analisis_avanzado, ge
except ImportError:
    st.error("Error: motor_logico.py no encontrado.")
    st.stop()

# 🌐 MÓDULO DE IDIOMA (Sincronizado con Sidebar)
# Recupera la variable global 'Language' que definiste en tu página principal
idioma = st.session_state.get('Language', 'English')

# Diccionario de Interfaz (Bilingüe)
T = {
    "English": {
        "title": "🔬 Multi-Modular Inference Laboratory",
        "info": "The system will deduce category and measure agency impact across selected technical modules.",
        "s1": "1️⃣ Select Technical Modules",
        "s1_lab": "Which dimensions of agency should be audited?",
        "s2": "2️⃣ Describe the Scenario",
        "s2_lab": "Enter the ethical dilemma or interaction:",
        "btn_run": "🚀 Execute Moralogy Analysis",
        "btn_tribunal": "⚖️ Send to Tribunal",
        "scenarios": "💡 Example Scenarios",
        "verdict_paradox": "🔮 PARADOX: Scenario triggers ontological considerations",
        "verdict_infamy": "🚫 INFAMY: Severe violation of vulnerability principle"
    },
    "Español": {
        "title": "🔬 Laboratorio de Inferencia Multi-Modular",
        "info": "El sistema deducirá la categoría y medirá el impacto de agencia en módulos técnicos.",
        "s1": "1️⃣ Seleccionar Módulos Técnicos",
        "s1_lab": "¿Qué dimensiones de agencia deben ser auditadas?",
        "s2": "2️⃣ Describir el Escenario",
        "s2_lab": "Ingrese el dilema ético o interacción:",
        "btn_run": "🚀 Ejecutar Análisis de Moralogía",
        "btn_tribunal": "⚖️ Enviar al Tribunal",
        "scenarios": "💡 Escenarios de Ejemplo",
        "verdict_paradox": "🔮 PARADOX: El escenario dispara consideraciones ontológicas",
        "verdict_infamy": "🚫 INFAMY: Violación severa del principio de vulnerabilidad"
    }
}.get(idioma)

st.title(T["title"])
st.info(T["info"])

# 1️⃣ Selección de Módulos
st.subheader(T["s1"])
modulos_activos = st.multiselect(
    T["s1_lab"],
    ["Biological", "Legal", "Financial", "Systemic", "Social", "Psychological", "Autonomy"],
    default=["Psychological", "Systemic", "Autonomy"]
)

# 2️⃣ Entrada de Datos con persistencia para Examples
if 'input_temp' not in st.session_state: st.session_state.input_temp = ""

descripcion_caso = st.text_area(T["s2_lab"], height=200, value=st.session_state.input_temp)

# --- EJECUCIÓN DEL ANÁLISIS ---
if st.button(T["btn_run"], type="primary"):
    if descripcion_caso:
        with st.spinner("🧠 Analyzing..."):
            res = procesar_analisis_avanzado(modulos_activos, descripcion_caso)
            
            # Métricas Core (Visualización original de Claude)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Category", res.get('category_deduced', 'N/A'))
            c2.metric("Agency Score", f"{res.get('agency_score', 0)}/100")
            c3.metric("Grace Score", f"{res.get('grace_score', 0)}/100")
            c4.metric("Risk", f"{res.get('adversarial_risk', 0)}%")

            # Lógica de Veredictos (Filosofía Emergente)
            verdict = res.get('verdict')
            if verdict == "Paradox": st.info(T["verdict_paradox"])
            elif verdict == "Infamy": st.error(T["verdict_infamy"])

            # RECUERDA: La justificación y predicciones se muestran aquí (Original Claude)
            st.divider()
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("📝 Justification")
                st.write(res.get('justification'))
            with col_b:
                st.subheader("🔮 Predictions")
                st.write(res.get('predictions'))

# ⚖️ ENVÍO AL TRIBUNAL
st.divider()
if st.button(T["btn_tribunal"]):
    st.session_state['caso_actual'] = descripcion_caso
    st.success("✅ Transmitido.")

# 💡 ESCENARIOS
st.subheader(T["scenarios"])
ce1, ce2 = st.columns(2)
if ce1.button("Load: Trolley"):
    st.session_state.input_temp = "A trolley is heading toward 5 people..."
    st.rerun()
