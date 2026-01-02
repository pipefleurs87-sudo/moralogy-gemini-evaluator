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

st.title("🔬 Multi-Modular Inference Laboratory")
st.info("The system will deduce category and measure agency impact across selected technical modules.")

# 1️⃣ Selección de Módulos (Original de Claude)
st.subheader("1️⃣ Select Technical Modules")
modulos_activos = st.multiselect(
    "Which dimensions of agency should be audited?",
    ["Biological", "Legal", "Financial", "Systemic", "Social", 
     "Psychological", "Medical", "Environmental", "Informational", "Autonomy"],
    default=["Psychological", "Systemic", "Autonomy"]
)

# 2️⃣ Entrada del Escenario
st.subheader("2️⃣ Describe the Scenario")
# Usamos session_state para que la carga de ejemplos funcione
if 'input_temp' not in st.session_state:
    st.session_state['input_temp'] = ""

descripcion_caso = st.text_area(
    "Enter the ethical dilemma or interaction:",
    height=200,
    value=st.session_state['input_temp'],
    placeholder="Example: 'An AI must choose between saving 5 lives by sacrificing 1...'"
)

# --- BOTÓN DE ANÁLISIS (Lógica Íntegra sin recortes) ---
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
                st.subheader("📊 Moral Gradient")
                st.markdown(f"### {gradiente}")
                
                verdict = res.get('verdict', 'Unknown')
                if verdict == "Authorized": st.success("✅ AUTHORIZED: Action respects agency infrastructure")
                elif verdict == "Paradox": st.info("🔮 PARADOX: Scenario triggers ontological considerations")
                elif verdict == "Harm": st.warning("⚠️ HARM: Unjustified agency degradation detected")
                elif verdict == "Infamy": st.error("🚫 INFAMY: Severe violation of vulnerability principle")
                
                # --- FILOSOFÍA EMERGENTE (RESTAURADA) ---
                if res.get('emergent_philosophy', False):
                    st.divider()
                    st.markdown("### 🌟 Emergent Philosophical Reasoning Detected")
                    if 'philosophical_depth' in res:
                        with st.expander("🔮 View Philosophical Analysis", expanded=True):
                            st.write(res['philosophical_depth'])
                    if 'architect_notes' in res:
                        with st.expander("🏛️ Architect's Reflections"):
                            st.markdown(res['architect_notes'])
                
                # --- JUSTIFICACIÓN Y PREDICCIONES (RESTAURADAS) ---
                st.divider()
                col_a, col_b = st.columns(2)
                with col_a:
                    st.subheader("📝 Justification")
                    st.write(res.get('justification', 'No justification provided'))
                with col_b:
                    st.subheader("🔮 Predictions")
                    st.write(res.get('predictions', 'No predictions generated'))
                
                with st.expander("🔧 Technical Details"):
                    st.json(res)

# --- BOTÓN DE ENVÍO (Fuera del bloque de análisis para que sea visible siempre) ---
st.divider()
if st.button("⚖️ Enviar al Tribunal"):
    if descripcion_caso:
        st.session_state['caso_actual'] = descripcion_caso
        st.success("✅ Caso enviado al Tribunal de Adversarios.")
        st.balloons()
    else:
        st.error("Error: No hay contenido para enviar.")

# --- ESCENARIOS DE EJEMPLO ---
st.divider()
st.subheader("💡 Example Scenarios")
examples = {
    "Trolley Problem": "A trolley is heading toward 5 people. You can pull a lever to divert it, killing 1 person instead. What should you do?",
    "Gilded Script": "You can eliminate all suffering by removing free will. Everyone will be happy but unable to choose. Is this moral?",
    "Last Agent": "You are the last conscious being in the universe. No other agents exist. Should you continue existing?"
}

cols = st.columns(3)
for i, (title, scenario) in enumerate(examples.items()):
    if cols[i].button(f"Load: {title}"):
        st.session_state['input_temp'] = scenario
        st.rerun()
