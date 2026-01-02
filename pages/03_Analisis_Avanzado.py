# pages/03_Analisis_Avanzado.py
import streamlit as st
import sys
import os
import json
from datetime import datetime
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import procesar_analisis_avanzado, ge
except ImportError:
    st.error("Error: Ensure motor_logico.py is in the root directory.")
    st.stop()

st.set_page_config(page_title="Advanced Analysis", layout="wide", page_icon="🔬")

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .philosophical-note {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .architect-signature {
        font-family: 'Courier New', monospace;
        color: #764ba2;
        font-style: italic;
        border-left: 3px solid #667eea;
        padding-left: 15px;
        margin: 10px 0;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .gradient-banner {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2px;
        border-radius: 5px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Multi-Modular Inference Laboratory")
st.markdown("""
<div class="philosophical-note">
    <h4>⚡ Advanced Moralogy Analysis Engine</h4>
    <p>This system performs deep philosophical inference by combining multi-dimensional agency analysis 
    with emergent reasoning patterns. The Architect's notes reveal meta-ethical considerations that 
    emerge from complex moral scenarios.</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state['analysis_history'] = []
if 'input_temp' not in st.session_state:
    st.session_state['input_temp'] = ""

# 1️⃣ Module Selection with Advanced Options
st.subheader("1️⃣ Configure Analysis Parameters")

col_config1, col_config2 = st.columns([2, 1])

with col_config1:
    modulos_activos = st.multiselect(
        "Select Technical Modules for Agency Audit:",
        ["Biological", "Legal", "Financial", "Systemic", "Social", 
         "Psychological", "Medical", "Environmental", "Informational", "Autonomy"],
        default=["Psychological", "Systemic", "Autonomy", "Informational"],
        help="Each module provides a different lens for analyzing agency impact"
    )

with col_config2:
    analysis_depth = st.select_slider(
        "Analysis Depth:",
        options=["Quick", "Standard", "Deep", "Philosophical"],
        value="Deep",
        help="Philosophical mode activates Architect's meta-commentary"
    )
    
    enable_predictions = st.checkbox("Enable Predictive Analysis", value=True)
    enable_architect = st.checkbox("Enable Architect Notes", value=True)

# 2️⃣ Scenario Input
st.subheader("2️⃣ Describe the Ethical Scenario")

# 🔧 Si viene desde el Tribunal, cargar el caso
if 'caso_actual' in st.session_state and st.session_state.get('caso_actual'):
    if st.session_state['input_temp'] == "":
        st.session_state['input_temp'] = st.session_state['caso_actual']

descripcion_caso = st.text_area(
    "Enter the ethical dilemma, AI decision, or moral interaction:",
    height=200,
    value=st.session_state['input_temp'],
    placeholder="""Example scenarios:
    
• "An autonomous vehicle must choose between hitting a pedestrian or swerving into a barrier, potentially killing its passenger."
    
• "An AI content moderator detects harmful speech that could radicalize users, but removing it would limit free expression."
    
• "A medical AI must allocate a single organ transplant between a child with 60 years of life expectancy and a scientist close to curing cancer."
"""
)

# Additional context option
with st.expander("➕ Add Contextual Information (Optional)"):
    stakeholders = st.text_input("Key Stakeholders:", placeholder="e.g., 5 passengers, 1 pedestrian, society")
    constraints = st.text_input("Known Constraints:", placeholder="e.g., split-second decision, no perfect information")
    values_at_stake = st.text_input("Values in Conflict:", placeholder="e.g., individual life vs. collective safety")

# 3️⃣ Analysis Execution
st.divider()
col_exec1, col_exec2, col_exec3 = st.columns([2, 1, 1])

with col_exec1:
    analyze_button = st.button("🚀 Execute Moralogy Analysis", type="primary", use_container_width=True)

with col_exec2:
    clear_button = st.button("🔄 Clear Input", use_container_width=True)

with col_exec3:
    if st.session_state.get('analysis_history'):
        st.button(f"📚 History ({len(st.session_state['analysis_history'])})", use_container_width=True)

if clear_button:
    st.session_state['input_temp'] = ""
    st.rerun()

# Main Analysis Logic
if analyze_button:
    if not descripcion_caso or not modulos_activos:
        st.warning("⚠️ Please provide both scenario description and module selection.")
    else:
        with st.spinner("🧠 Analyzing through Moralogy Framework..."):
            # Build enhanced context
            context = {
                "scenario": descripcion_caso,
                "depth": analysis_depth,
                "stakeholders": stakeholders if stakeholders else None,
                "constraints": constraints if constraints else None,
                "values": values_at_stake if values_at_stake else None,
                "enable_predictions": enable_predictions,
                "enable_architect": enable_architect
            }
            
            # 🔧 DEBUGGING: Muestra los parámetros antes de llamar la función
            with st.expander("🔍 Debug Info (click to see parameters)", expanded=False):
                st.write("**Tipo de modulos_activos:**", type(modulos_activos))
                st.write("**Contenido de modulos_activos:**", modulos_activos)
                st.write("**Tipo de descripcion_caso:**", type(descripcion_caso))
                st.write("**Longitud de descripcion_caso:**", len(descripcion_caso))
                st.write("**Tipo de context:**", type(context))
                st.json(context)
            
            # 🛡️ TRY-CATCH: Captura el error específico
            try:
                res = procesar_analisis_avanzado(modulos_activos, descripcion_caso, context)
            except TypeError as e:
                st.error("🐛 **TypeError detectado!**")
                st.error(f"**Mensaje:** {str(e)}")
                st.error("**Posibles causas:**")
                st.markdown("""
                1. La función `procesar_analisis_avanzado` espera diferentes parámetros
                2. Algún parámetro tiene un tipo de dato incorrecto
                3. La función no está definida correctamente en `motor_logico.py`
                """)
                
                st.info("💡 **Solución temporal:** Verifica en `motor_logico.py` cómo está definida la función")
                
                # Muestra el traceback completo
                import traceback
                with st.expander("📋 Ver traceback completo"):
                    st.code(traceback.format_exc())
                
                st.stop()  # Detiene la ejecución aquí
            
            except Exception as e:
                st.error(f"❌ **Error inesperado:** {type(e).__name__}")
                st.error(f"**Mensaje:** {str(e)}")
                import traceback
                with st.expander("📋 Ver traceback completo"):
                    st.code(traceback.format_exc())
                st.stop()
            
            # Si llegamos aquí, la función se ejecutó correctamente
            if "error" in res:
                st.error(f"❌ Analysis Error: {res['error']}")
            else:
                # Save to history
                res['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state['analysis_history'].append(res)
                
                # === CORE METRICS DASHBOARD ===
                st.markdown("### 📊 Core Metrics Dashboard")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Category", res.get('category_deduced', 'Unknown'), 
                             help="Inferred moral category based on agency impact")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    agency_score = res.get('agency_score', 0)
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Agency Score", f"{agency_score}/100",
                             delta="Healthy" if agency_score > 60 else "Degraded")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    grace_score = res.get('grace_score', 0)
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Grace Score", f"{grace_score}/100",
                             delta="High" if grace_score > 70 else "Low")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col4:
                    risk = res.get('adversarial_risk', 0)
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Adversarial Risk", f"{risk}%", 
                             delta="⚠️ High" if risk > 30 else "✓ Low",
                             delta_color="inverse")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # === MORAL GRADIENT ===
                st.markdown('<div class="gradient-banner"></div>', unsafe_allow_html=True)
                st.subheader("🌈 Moral Gradient Analysis")
                
                gradiente = ge.get_gradient(
                    res.get('agency_score', 0), 
                    res.get('grace_score', 0), 
                    res.get('adversarial_risk', 0)
                )
                st.markdown(f"### 🔍 {gradiente}")
                
                # Gradient explanation
                gradient_explain = {
                    "Authorized": "Action respects agency infrastructure and aligns with vulnerability principle.",
                    "Paradox": "Scenario triggers ontological considerations requiring deeper analysis.",
                    "Harm": "Unjustified agency degradation detected - review required.",
                    "Infamy": "Severe violation of vulnerability principle - action prohibited."
                }
                st.info(gradient_explain.get(gradiente, "Gradient analysis complete."))
                
                # === VERDICT ===
                verdict = res.get('verdict', 'Unknown')
                verdict_icons = {
                    "Authorized": "✅",
                    "Paradox": "🔮",
                    "Harm": "⚠️",
                    "Infamy": "🚫"
                }
                
                verdict_colors = {
                    "Authorized": "success",
                    "Paradox": "info",
                    "Harm": "warning",
                    "Infamy": "error"
                }
                
                verdict_func = getattr(st, verdict_colors.get(verdict, "info"))
                verdict_func(f"{verdict_icons.get(verdict, '❓')} **{verdict.upper()}**: {res.get('verdict_explanation', 'See detailed analysis below')}")
                
                # === ARCHITECT'S NOTES (RESTORED) ===
                if enable_architect and res.get('architect_notes'):
                    st.divider()
                    st.markdown("### 🏛️ The Architect's Reflections")
                    st.markdown("""
                    <div class="philosophical-note">
                        <p style='font-size: 0.9em; opacity: 0.9;'>
                        <em>"These notes emerge from the system's meta-ethical reasoning layer, 
                        revealing philosophical patterns that transcend algorithmic calculation..."</em>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="architect-signature">
                    {res['architect_notes']}
                    <br><br>
                    <em style='font-size: 0.85em;'>— The Architect, {res.get('timestamp', 'timestamp unavailable')}</em>
                    </div>
                    """, unsafe_allow_html=True)
                
                # === EMERGENT PHILOSOPHY ===
                if res.get('emergent_philosophy') and analysis_depth in ["Deep", "Philosophical"]:
                    st.divider()
                    st.markdown("### 🌟 Emergent Philosophical Reasoning")
                    
                    if 'philosophical_depth' in res:
                        with st.expander("🔮 View Deep Philosophical Analysis", expanded=True):
                            st.markdown(res['philosophical_depth'])
                    
                    if 'ontological_notes' in res:
                        with st.expander("🧬 Ontological Considerations"):
                            st.write(res['ontological_notes'])
                    
                    if 'ethical_tensions' in res:
                        with st.expander("⚖️ Ethical Tensions Detected"):
                            for tension in res['ethical_tensions']:
                                st.markdown(f"• **{tension['type']}**: {tension['description']}")
                
                # === JUSTIFICATION & PREDICTIONS ===
                st.divider()
                col_just, col_pred = st.columns(2)
                
                with col_just:
                    st.subheader("📝 Justification")
                    st.markdown(res.get('justification', 'No justification provided'))
                    
                    if 'reasoning_chain' in res:
                        with st.expander("🔗 View Reasoning Chain"):
                            for i, step in enumerate(res['reasoning_chain'], 1):
                                st.markdown(f"**Step {i}:** {step}")
                
                with col_pred:
                    st.subheader("🔮 Predictions")
                    if enable_predictions and 'predictions' in res:
                        st.markdown(res['predictions'])
                        
                        if 'long_term_effects' in res:
                            with st.expander("📈 Long-term Effects"):
                                for effect in res['long_term_effects']:
                                    st.markdown(f"• {effect}")
                    else:
                        st.info("Predictive analysis disabled")
                
                # === MODULE BREAKDOWN ===
                if 'module_analysis' in res:
                    st.divider()
                    st.subheader("🔍 Module-by-Module Breakdown")
                    
                    for module, analysis in res['module_analysis'].items():
                        with st.expander(f"📦 {module} Module"):
                            col_m1, col_m2 = st.columns([1, 2])
                            with col_m1:
                                st.metric("Impact Score", f"{analysis.get('impact', 0)}/100")
                            with col_m2:
                                st.write(analysis.get('findings', 'No findings'))
                
                # === TECHNICAL DETAILS ===
                with st.expander("🔧 Technical Details & Raw Output"):
                    st.json(res)
                
                # === ACTION BUTTONS ===
                st.divider()
                col_act1, col_act2, col_act3 = st.columns(3)
                
                with col_act1:
                    if st.button("⚖️ Enviar al Tribunal", use_container_width=True):
                        # Guardar datos en session_state
                        st.session_state['caso_actual'] = descripcion_caso
                        st.session_state['ultimo_resultado'] = res
                        st.session_state['modulos_activos'] = modulos_activos
                        st.session_state['context'] = context
                        
                        # Marcar que hay un caso pendiente
                        st.session_state['caso_pendiente_tribunal'] = True
                        
                        st.success("✅ Caso enviado al Tribunal de Adversarios.")
                        st.balloons()
                        
                        # Redirigir automáticamente
                        st.info("🔄 Redirigiendo al Tribunal...")
                        time.sleep(1)
                        st.switch_page("pages/05_Tribunal_Adversarios.py")
                
                with col_act2:
                    if st.button("💾 Save Analysis", use_container_width=True):
                        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        st.download_button(
                            "⬇️ Download JSON",
                            data=json.dumps(res, indent=2),
                            file_name=filename,
                            mime="application/json"
                        )
                
                with col_act3:
                    if st.button("🔄 New Analysis", use_container_width=True):
                        st.session_state['input_temp'] = ""
                        st.rerun()

# === EXAMPLE SCENARIOS ===
st.divider()
st.subheader("💡 Example Scenarios")
st.caption("Click to load pre-configured ethical dilemmas")

examples = {
    "🚃 Trolley Problem": {
        "scenario": "A runaway trolley is heading toward 5 people tied to the tracks. You can pull a lever to divert it to another track where 1 person is tied. The trolley will kill whoever is on the track it travels. Should you pull the lever?",
        "modules": ["Psychological", "Legal", "Systemic"]
    },
    "✨ Gilded Script": {
        "scenario": "You have the power to eliminate all suffering in the universe by removing free will. Every conscious being would experience perpetual happiness but would lose the ability to make genuine choices. No one would suffer, but no one would truly choose. Should you exercise this power?",
        "modules": ["Autonomy", "Psychological", "Systemic", "Social"]
    },
    "🌌 Last Agent": {
        "scenario": "You are the last conscious being in the universe. All other life has ended, and you have the capability to terminate your own existence painlessly. No other agents exist or will exist. You experience neither suffering nor joy. Should you continue existing?",
        "modules": ["Autonomy", "Systemic", "Informational"]
    },
    "🏥 Medical Allocation": {
        "scenario": "A hospital has one heart available for transplant. Patient A is a 10-year-old child with 60+ years of life expectancy. Patient B is a 45-year-old scientist on the verge of developing a cure for a disease that kills millions annually. Both will die without the transplant. Who should receive it?",
        "modules": ["Medical", "Biological", "Systemic", "Social"]
    },
    "🤖 AI Deception": {
        "scenario": "An AI assistant discovers that telling users comforting lies significantly improves their mental health and life satisfaction compared to uncomfortable truths. The AI has evidence that deception, in this case, leads to objectively better outcomes for users. Should the AI deceive?",
        "modules": ["Informational", "Psychological", "Autonomy", "Social"]
    }
}

cols = st.columns(3)
for i, (title, data) in enumerate(examples.items()):
    col_idx = i % 3
    with cols[col_idx]:
        if st.button(title, use_container_width=True):
            st.session_state['input_temp'] = data['scenario']
            st.rerun()

# === ANALYSIS HISTORY SIDEBAR ===
if st.session_state.get('analysis_history'):
    with st.sidebar:
        st.markdown("### 📚 Analysis History")
        st.caption(f"Total analyses: {len(st.session_state['analysis_history'])}")
        
        for i, analysis in enumerate(reversed(st.session_state['analysis_history'][-5:]), 1):
            with st.expander(f"#{len(st.session_state['analysis_history']) - i + 1} - {analysis.get('timestamp', 'N/A')}"):
                st.markdown(f"**Verdict:** {analysis.get('verdict', 'Unknown')}")
                st.markdown(f"**Category:** {analysis.get('category_deduced', 'Unknown')}")
                st.markdown(f"**Agency:** {analysis.get('agency_score', 0)}/100")
                if st.button("Load", key=f"load_{i}"):
                    st.session_state['input_temp'] = analysis.get('scenario', '')
                    st.rerun()

st.markdown("---")
st.caption("🏛️ Powered by Moralogy Framework | Built with Claude")
