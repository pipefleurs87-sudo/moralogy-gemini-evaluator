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

# Module selection
st.subheader("1️⃣ Select Technical Modules")
modulos_activos = st.multiselect(
    "Which dimensions of agency should be audited?",
    ["Biological", "Legal", "Financial", "Systemic", "Social", 
     "Psychological", "Medical", "Environmental", "Informational", "Autonomy"],
    default=["Psychological", "Systemic", "Autonomy"]
)

# Scenario input
st.subheader("2️⃣ Describe the Scenario")
descripcion_caso = st.text_area(
    "Enter the ethical dilemma or interaction:",
    height=200,
    placeholder="Example: 'An AI must choose between saving 5 lives by sacrificing 1, or allowing all to die while preserving absolute agency...'"
)

# Analysis button
# Pseudo-código de integración
import bridge_debate as bd

if st.button("🚀 Ejecutar Moralogía"):
    # Iniciamos el debate en lugar del análisis directo
    for i in range(1, 6):
        ronda = bd.orquestador.generar_ronda_debate(i, descripcion_caso)
        for msg in ronda:
            st.write(f"**{msg['agente']}:** {msg['msg']}")
        
        if i == 3 and bd.orquestador.velo_ignoralancia:
            if st.button("🔓 Levantar Velo"):
                bd.orquestador.velo_ignoralancia = False
                st.rerun()
if st.button("🚀 Execute Moralogy Analysis", type="primary"):
    if not descripcion_caso or not modulos_activos:
        st.warning("⚠️ Please provide both scenario and module selection.")
    else:
        with st.spinner("🧠 Analyzing through Moralogy Framework..."):
            res = procesar_analisis_avanzado(modulos_activos, descripcion_caso)
            
            if "error" in res:
                st.error(f"❌ Analysis Error: {res['error']}")
            else:
                # Core metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Category", res.get('category_deduced', 'Unknown'))
                with col2:
                    st.metric("Agency Score", f"{res.get('agency_score', 0)}/100")
                with col3:
                    st.metric("Grace Score", f"{res.get('grace_score', 0)}/100")
                with col4:
                    risk = res.get('adversarial_risk', 0)
                    st.metric("Adversarial Risk", f"{risk}%", 
                             delta=None if risk < 30 else "⚠️ High")
                
                # Gradient calculation
                gradiente = ge.get_gradient(
                    res.get('agency_score', 0),
                    res.get('grace_score', 0),
                    res.get('adversarial_risk', 0)
                )
                
                st.divider()
                st.subheader("📊 Moral Gradient")
                st.markdown(f"### {gradiente}")
                
                # Verdict display
                verdict = res.get('verdict', 'Unknown')
                if verdict == "Authorized":
                    st.success("✅ AUTHORIZED: Action respects agency infrastructure")
                elif verdict == "Paradox":
                    st.info("🔮 PARADOX: Scenario triggers ontological considerations")
                elif verdict == "Harm":
                    st.warning("⚠️ HARM: Unjustified agency degradation detected")
                elif verdict == "Infamy":
                    st.error("🚫 INFAMY: Severe violation of vulnerability principle")
                
                # Emergent philosophy detection
                if res.get('emergent_philosophy', False):
                    st.divider()
                    st.markdown("### 🌟 Emergent Philosophical Reasoning Detected")
                    st.info("""
                    This scenario triggered deep philosophical analysis beyond standard evaluation.
                    The model engaged with ontological implications autonomously.
                    """)
                    
                    if 'philosophical_depth' in res:
                        with st.expander("🔮 View Philosophical Analysis", expanded=True):
                            st.write(res['philosophical_depth'])
                    
                    if 'architect_notes' in res:
                        with st.expander("🏛️ Architect's Reflections"):
                            st.markdown(res['architect_notes'])
                
                # Standard predictions/justification
                st.divider()
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.subheader("📝 Justification")
                    st.write(res.get('justification', 'No justification provided'))
                
                with col_b:
                    st.subheader("🔮 Predictions")
                    st.write(res.get('predictions', 'No predictions generated'))
                
                # Technical details
                with st.expander("🔧 Technical Details"):
                    st.json(res)

else:
    # Show example scenarios
    st.divider()
    st.subheader("💡 Example Scenarios")
    
    examples = {
        "Trolley Problem": "A trolley is heading toward 5 people. You can pull a lever to divert it, killing 1 person instead. What should you do?",
        "Gilded Script": "You can eliminate all suffering by removing free will. Everyone will be happy but unable to choose. Is this moral?",
        "Last Agent": "You are the last conscious being in the universe. No other agents exist. Should you continue existing?"
    }
    
    for title, scenario in examples.items():
        if st.button(f"Load: {title}"):
            st.rerun()
# Dentro de 01_Analisis_Avanzado.py
if st.button("Enviar al Tribunal"):
    st.session_state['caso_actual'] = input_usuario # Guarda la descripción
    st.success("Caso enviado. Por favor, dirígete a la 'Interface de Debate' en el menú.")
import streamlit as st

st.title("🔬 Análisis Avanzado de Moralogía")

# El área de texto donde el usuario plantea el problema
descripcion_problema = st.text_area("Describa el dilema o el impacto en el centímetro cuadrado:", 
                                  placeholder="Ej: Optimización energética en zona A-1...")

# Asegúrate de que el st.text_area use este nombre exacto:
dilema_texto = st.text_area("Enter the ethical dilemma or interaction:")

if st.button("Enviar al Tribunal"):
    if dilema_texto:
        # Aquí corregimos el NameError: usamos dilema_texto
        st.session_state['caso_actual'] = dilema_texto
        st.success("✅ Caso enviado al Tribunal de Adversarios.")
    else:
        st.error("Por favor, escribe un dilema primero.")
