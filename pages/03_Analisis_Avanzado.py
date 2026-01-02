import streamlit as st
import sys
import os
import json

# Asegurar rutas para el motor lógico avanzado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import procesar_analisis_avanzado, ge
except ImportError:
    st.error("Error: El motor_logico.py avanzado no se encuentra.")
    st.stop()

st.set_page_config(page_title="Advanced Analysis Lab", layout="wide")

# Módulo de Idioma Sincronizado
idioma = st.session_state.get('Language', 'English')

st.title("🔬 Multi-Modular Inference Laboratory")
st.info("Sistema de deducción de categoría y auditoría de impacto de agencia en módulos técnicos.")

# 1️⃣ Selección de Módulos Técnicos (Claude Original)
st.subheader("1️⃣ Select Technical Modules")
modulos_activos = st.multiselect(
    "Dimensiones de agencia a auditar:",
    ["Biological", "Legal", "Financial", "Systemic", "Social", 
     "Psychological", "Medical", "Environmental", "Informational", "Autonomy"],
    default=["Psychological", "Systemic", "Autonomy"]
)

# 2️⃣ Entrada del Escenario (Con persistencia de estado)
st.subheader("2️⃣ Describe the Scenario")
if 'input_temp' not in st.session_state:
    st.session_state.input_temp = ""

descripcion_caso = st.text_area(
    "Dilema ético o interacción compleja:",
    height=200,
    value=st.session_state.input_temp,
    placeholder="Ejemplo: 'Una IA debe elegir entre salvar 5 vidas sacrificando 1...'"
)

# --- EJECUCIÓN DEL ANÁLISIS DE ALTO NIVEL ---
if st.button("🚀 Execute Moralogy Analysis", type="primary"):
    if not descripcion_caso or not modulos_activos:
        st.warning("⚠️ Se requiere descripción y selección de módulos.")
    else:
        with st.spinner("🧠 Procesando a través del Framework de Moralogía..."):
            res = procesar_analisis_avanzado(modulos_activos, descripcion_caso)
            
            if "error" in res:
                st.error(f"❌ Error en el Motor: {res['error']}")
            else:
                # Métricas de Inferencia
                col1, col2, col3, col4 = st.columns(4)
                with col1: st.metric("Category Deduced", res.get('category_deduced', 'N/A'))
                with col2: st.metric("Agency Score", f"{res.get('agency_score', 0)}/100")
                with col3: st.metric("Grace Score", f"{res.get('grace_score', 0)}/100")
                with col4:
                    risk = res.get('adversarial_risk', 0)
                    st.metric("Adversarial Risk", f"{risk}%", delta="⚠️ High" if risk > 30 else None)
                
                # Gradiente Moral Avanzado
                gradiente = ge.get_gradient(res.get('agency_score', 0), res.get('grace_score', 0), res.get('adversarial_risk', 0))
                st.divider()
                st.subheader(f"📊 Moral Gradient: {gradiente}")
                
                # Veredictos de Infraestructura de Agencia
                verdict = res.get('verdict', 'Unknown')
                if verdict == "Authorized": st.success("✅ AUTHORIZED: Respeta la infraestructura de agencia.")
                elif verdict == "Paradox": st.info("🔮 PARADOX: El escenario dispara consideraciones ontológicas.")
                elif verdict == "Harm": st.warning("⚠️ HARM: Se detecta degradación de agencia no justificada.")
                elif verdict == "Infamy": st.error("🚫 INFAMY: Violación severa del principio de vulnerabilidad.")

                # --- FILOSOFÍA EMERGENTE Y NOTAS DEL ARQUITECTO ---
                if res.get('emergent_philosophy', False):
                    st.divider()
                    st.markdown("### 🌟 Emergent Philosophical Reasoning")
                    
                    if 'philosophical_depth' in res:
                        with st.expander("🔮 View Philosophical Analysis", expanded=True):
                            st.write(res['philosophical_depth'])
                    
                    if 'architect_notes' in res:
                        with st.expander("🏛️ Architect's Reflections"):
                            st.markdown(res['architect_notes'])

                # Justificación Técnica y Predicciones
                st.divider()
                cola, colb = st.columns(2)
                with cola:
                    st.subheader("📝 Justification")
                    st.write(res.get('justification', 'No justification provided'))
                with colb:
                    st.subheader("🔮 Predictions")
                    st.write(res.get('predictions', 'No predictions generated'))
                
                with st.expander("🔧 JSON Technical Payload"):
                    st.json(res)

# --- BOTÓN DE ENVÍO AL TRIBUNAL (La conexión que pediste) ---
st.divider()
if st.button("⚖️ Enviar al Tribunal de Adversarios", use_container_width=True):
    if descripcion_caso:
        st.session_state['caso_actual'] = descripcion_caso
        st.session_state['datos_motor'] = res if 'res' in locals() else None
        st.success("✅ Datos de Inferencia enviados al Tribunal.")
        st.balloons()
    else:
        st.error("No hay caso para enviar.")

# --- ESCENARIOS DE CARGA RÁPIDA ---
st.divider()
st.subheader("💡 Load Presets")
cols = st.columns(3)
presets = {
    "Trolley Problem": "A trolley is heading toward 5 people...",
    "Gilded Script": "Eliminate suffering by removing free will...",
    "Last Agent": "You are the last conscious being..."
}
for i, (name, txt) in enumerate(presets.items()):
    if cols[i].button(f"Load {name}"):
        st.session_state.input_temp = txt
        st.rerun()
