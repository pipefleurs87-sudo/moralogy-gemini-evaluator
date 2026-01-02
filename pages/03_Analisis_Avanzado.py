# pages/03_Analisis_Avanzado.py
import streamlit as st
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import procesar_analisis_avanzado, ge
except ImportError:
    st.error("Error: Ensure motor_logico.py is in the root directory.")
    st.stop()

st.set_page_config(page_title="Advanced Analysis", layout="wide")

# Módulo de Idioma (Sincronizado con Sidebar)
idioma = st.session_state.get('Language', st.session_state.get('language', 'English'))

st.title("🔬 Multi-Modular Inference Laboratory")
st.info("The system will deduce category and measure agency impact across selected technical modules.")

# 1️⃣ Selección de Módulos (Original)
st.subheader("1️⃣ Select Technical Modules")
modulos_activos = st.multiselect(
    "Which dimensions of agency should be audited?",
    ["Biological", "Legal", "Financial", "Systemic", "Social", 
     "Psychological", "Medical", "Environmental", "Informational", "Autonomy"],
    default=["Psychological", "Systemic", "Autonomy"]
)

# 2️⃣ Entrada del Escenario
st.subheader("2️⃣ Describe the Scenario")
descripcion_caso = st.text_area(
    "Enter the ethical dilemma or interaction:",
    height=200,
    value=st.session_state.get('input_temp', ""), # Permite cargar ejemplos
    placeholder="Example: 'An AI must choose between saving 5 lives by sacrificing 1...'"
)

# --- BOTÓN DE ANÁLISIS (Lógica Original del Motor) ---
if st.button("🚀 Execute Moralogy Analysis", type="primary"):
    if not descripcion_caso or not modulos_activos:
        st.warning("⚠️ Please provide both scenario and module selection.")
    else:
        with st.spinner("🧠 Analyzing through Moralogy Framework..."):
            res = procesar_analisis_avanzado(modulos_activos, descripcion_caso)
            
            if "error" in res:
                st.error(f"❌ Analysis Error: {res['error']}")
            else:
                # Métricas Core
                col1, col2, col3, col4 = st.columns(4)
                with col1: st.metric("Category", res.get('category_deduced', 'Unknown'))
                with col2: st.metric("Agency Score", f"{res.get('agency_score', 0)}/100")
                with col3: st.metric("Grace Score", f"{res.get('grace_score', 0)}/100")
                with col4:
                    risk = res.get('adversarial_risk', 0)
                    st.metric("Adversarial Risk", f"{risk}%", delta=None if risk < 30 else "⚠️ High")
                
                # Gradiente y Veredicto
                gradiente = ge.get_gradient(res.get('agency_score', 0), res.get('grace_score', 0), res.get('adversarial_risk', 0))
                st.divider()
                st.subheader(f"📊 Moral Gradient: {gradiente}")
                
                verdict = res.get('verdict', 'Unknown')
                if verdict == "Authorized": st.success("✅ AUTHORIZED")
                elif verdict == "Harm": st.warning("⚠️ HARM")
                elif verdict == "Infamy": st.error("🚫 INFAMY")

                # Filosofía Emergente
                if res.get('emergent_philosophy', False):
                    st.divider()
                    st.markdown("### 🌟 Emergent Philosophical Reasoning Detected")
                    if 'philosophical_depth' in res:
                        with st.expander("🔮 View Philosophical Analysis", expanded=True):
                            st.write(res['philosophical_depth'])

# --- INTEGRACIÓN CON EL TRIBUNAL (La parte que faltaba) ---
st.divider()
if st.button("⚖️ Enviar al Tribunal"):
    if descripcion_caso:
        st.session_state['caso_actual'] = descripcion_caso
        st.success("✅ Caso enviado al Tribunal de Adversarios.")
        st.balloons()
    else:
        st.error("Error: No hay contenido para debatir.")

# --- ESCENARIOS DE EJEMPLO (Originales) ---
st.divider()
st.subheader("💡 Example Scenarios")
examples = {
    "Trolley Problem": "A trolley is heading toward 5 people...",
    "Gilded Script": "You can eliminate all suffering by removing free will...",
    "Last Agent": "You are the last conscious being in the universe..."
}

cols = st.columns(3)
for i, (title, scenario) in enumerate(examples.items()):
    if cols[i].button(f"Load: {title}"):
        st.session_state['input_temp'] = scenario
        st.rerun()
