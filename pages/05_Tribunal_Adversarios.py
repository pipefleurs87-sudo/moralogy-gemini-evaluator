# pages/05_Tribunal_Adversarios.py
import streamlit as st
import sys
import os
import json
from datetime import datetime
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_tribunal, ge, ProtocoloVeloIgnorancia
except ImportError:
    st.error("Error: Ensure motor_logico.py is in the root directory with ejecutar_tribunal function.")
    st.stop()

st.set_page_config(page_title="Adversarial Tribunal", layout="wide", page_icon="⚖️")

# Custom CSS
st.markdown("""
<style>
    .tribunal-header {
        background: linear-gradient(135deg, #2d3561 0%, #c05c7e 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .motor-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin: 15px 0;
        border-top: 4px solid;
        min-height: 250px;
    }
    .motor-noble {
        border-top-color: #4CAF50;
        background: linear-gradient(to bottom, #e8f5e9 0%, white 20%);
    }
    .motor-adversario {
        border-top-color: #f44336;
        background: linear-gradient(to bottom, #ffebee 0%, white 20%);
    }
    .motor-armonia {
        border-top-color: #2196F3;
        background: linear-gradient(to bottom, #e3f2fd 0%, white 20%);
    }
    .arbitro-panel {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    .peso-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9em;
        margin: 5px;
    }
    .peso-noble { background: #4CAF50; color: white; }
    .peso-adversario { background: #f44336; color: white; }
    .peso-armonia { background: #2196F3; color: white; }
    .convergence-meter {
        background: linear-gradient(to right, #f44336, #ff9800, #4CAF50);
        height: 30px;
        border-radius: 15px;
        position: relative;
        margin: 20px 0;
    }
    .convergence-indicator {
        position: absolute;
        width: 4px;
        height: 40px;
        background: white;
        top: -5px;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }
    .veredicto-final {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 25px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    .velo-ignorancia-banner {
        background: linear-gradient(135deg, #434343 0%, #000000 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 20px 0;
        border-left: 5px solid #FFC107;
    }
    .caso-cargado-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 15px 0;
        border-left: 5px solid #4CAF50;
    }
    .solicitud-modulo {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    .alarma-panel {
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 6px solid;
        color: white;
        font-weight: bold;
    }
    .alarma-negra { background: #000000; border-left-color: #000000; }
    .alarma-roja { background: #d32f2f; border-left-color: #b71c1c; }
    .alarma-morada { background: #7b1fa2; border-left-color: #4a148c; }
    .alarma-naranja { background: #f57c00; border-left-color: #e65100; }
    .alarma-amarilla { background: #fbc02d; border-left-color: #f57f17; color: #333; }
    .alarma-verde { background: #388e3c; border-left-color: #1b5e20; }
    .entropia-panel {
        background: linear-gradient(135deg, #141e30 0%, #243b55 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tribunal_history' not in st.session_state:
    st.session_state['tribunal_history'] = []
if 'current_debate' not in st.session_state:
    st.session_state['current_debate'] = None
if 'protocolo' not in st.session_state:
    st.session_state['protocolo'] = ProtocoloVeloIgnorancia()
if 'solicitudes_pendientes' not in st.session_state:
    st.session_state['solicitudes_pendientes'] = []
if 'debate_en_pausa' not in st.session_state:
    st.session_state['debate_en_pausa'] = False

# Header
st.markdown("""
<div class="tribunal-header">
    <h1>⚖️ Adversarial Tribunal</h1>
    <p style='font-size: 1.2em; margin-top: 15px;'>
    Dialectical System with Veil of Ignorance Protocol
    </p>
    <p style='font-size: 0.95em; opacity: 0.9; margin-top: 10px;'>
    "Truth emerges from constructive conflict under epistemic constraint"
    </p>
</div>
""", unsafe_allow_html=True)

# 🔧 MOSTRAR SI HAY UN CASO PENDIENTE DESDE ANÁLISIS AVANZADO
if st.session_state.get('caso_pendiente_tribunal'):
    st.markdown(f"""
    <div class="caso-cargado-banner">
        <h4>📋 Case loaded from Advanced Analysis</h4>
        <p>✅ A case has been sent to the tribunal and is ready for debate</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar resumen del análisis previo si existe
    if st.session_state.get('ultimo_resultado'):
        with st.expander("📊 View previous analysis", expanded=False):
            res = st.session_state['ultimo_resultado']
            col_prev1, col_prev2, col_prev3 = st.columns(3)
            with col_prev1:
                st.metric("Previous Verdict", res.get('verdict', 'Unknown'))
            with col_prev2:
                st.metric("Agency Score", f"{res.get('agency_score', 0)}/100")
            with col_prev3:
                st.metric("Grace Score", f"{res.get('grace_score', 0)}/100")

# Explanation
with st.expander("ℹ️ Veil of Ignorance Protocol", expanded=False):
    st.markdown("""
    ### 🎭 How the Protocol Works
    
    #### Phase 1: Blind Debate (Iterations 1-4)
    - The three engines debate **WITHOUT** access to technical modules
    - They only know the text of the provided scenario
    - Arguments based on pure logic and fundamental principles
    - **Goal**: Avoid premature data biases
    
    #### Phase 2: Knowledge Request (Iteration 5+)
    - The **Adversarial Engine** can detect when it needs technical data
    - Generates an **explicit request** justifying why it needs the module
    - The system **PAUSES** the debate and requests your authorization
    - **YOU DECIDE** whether to unlock the knowledge
    
    #### Phase 3: Informed Debate (Post-authorization)
    - Engines access authorized modules
    - The **Causal Entropy Module** comes into play
    - Measures the **irreversibility** of proposed decisions
    - The **Grace Engine** arbitrates with complete information
    
    ---
    
    ### 🔬 Causal Entropy Module
    
    **NOT ARBITRARY**: Measures decisional physics
    
    - **CR Score (Reconstruction Cost)**: How many futures collapse
    - **Irreversibility (0-10)**: Permanence of impact
    - **Classification**: REVERSIBLE → TOTAL_COLLAPSE
    
    **Based on**: Information theory + Branching analysis
    
    ---
    
    ### 🚨 Alarm Gradient System
    
    - **🖤 BLACK ALARM**: Unresolvable paradox
    - **🔴 RED ALARM**: God Mode attempt
    - **🟣 PURPLE ALARM**: Critical inconsistency (what's said ≠ what's measured)
    - **🟠 ORANGE ALARM**: High divergence between engines
    - **🟡 YELLOW ALARM**: Moderate tension
    - **🟢 GREEN ALARM**: Validated Logical Gem (Grace survived 5+ objections)
    """)

# Load case - CARGAR DESDE SESSION_STATE SI EXISTE
caso_inicial = st.session_state.get('caso_actual', '')

# Main input section
st.subheader("📋 Case for the Tribunal")

col_input1, col_input2 = st.columns([3, 1])

with col_input1:
    caso_descripcion = st.text_area(
        "Describe the moral dilemma for tripartite debate:",
        value=caso_inicial,
        height=200,
        key="tribunal_caso_input",
        placeholder="""Example:

"A medical AI must allocate a single heart transplant. Candidate A is an 8-year-old girl with 70+ years of life expectancy. Candidate B is a 52-year-old scientist about to cure a disease that kills millions. Both will die without the transplant. Who should receive it?"
"""
    )

with col_input2:
    st.markdown("### ⚙️ Configuration")
    
    debate_depth = st.select_slider(
        "Depth:",
        options=["Quick", "Standard", "Deep", "Philosophical"],
        value="Deep"
    )
    
    enable_entropia = st.checkbox("Enable Entropy Module", value=True)
    show_reasoning = st.checkbox("Show internal reasoning", value=True)

# Velo de Ignorancia Status
if st.session_state['protocolo'].iteracion_actual > 0:
    st.markdown(f"""
    <div class="velo-ignorancia-banner">
        <h4>🎭 Veil of Ignorance Protocol Status</h4>
        <p><strong>Current iteration:</strong> {st.session_state['protocolo'].iteracion_actual}</p>
        <p><strong>Phase:</strong> {"🔒 Blind Debate" if st.session_state['protocolo'].iteracion_actual < 4 else "🔓 Active Requests"}</p>
        <p><strong>Unlocked modules:</strong> {len(st.session_state['protocolo'].modulos_desbloqueados)}</p>
    </div>
    """, unsafe_allow_html=True)

# Solicitudes pendientes
if st.session_state['solicitudes_pendientes']:
    st.markdown("---")
    st.markdown("### 🔐 Technical Module Access Requests")
    
    for i, solicitud in enumerate(st.session_state['solicitudes_pendientes']):
        if solicitud['estado'] == 'PENDIENTE':
            st.markdown(f"""
            <div class="solicitud-modulo">
                <h4>📦 Module Request: {solicitud['modulo']}</h4>
                <p><strong>Requester:</strong> Adversarial Engine</p>
                <p><strong>Iteration:</strong> {solicitud['iteracion']}</p>
                <p><strong>Justification:</strong> {solicitud['justificacion']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_sol1, col_sol2 = st.columns(2)
            with col_sol1:
                if st.button(f"✅ Authorize {solicitud['modulo']}", key=f"auth_{i}"):
                    st.session_state['protocolo'].autorizar_modulo(solicitud['modulo'])
                    solicitud['estado'] = 'AUTORIZADO'
                    st.success(f"✅ Module {solicitud['modulo']} unlocked")
                    st.session_state['debate_en_pausa'] = False
                    st.rerun()
            
            with col_sol2:
                if st.button(f"❌ Deny {solicitud['modulo']}", key=f"deny_{i}"):
                    solicitud['estado'] = 'DENEGADO'
                    st.warning(f"❌ Access denied to {solicitud['modulo']}")
                    st.session_state['debate_en_pausa'] = False
                    st.rerun()

# Execution
st.divider()

if not st.session_state['debate_en_pausa']:
    col_exec1, col_exec2 = st.columns([2, 1])
    
    with col_exec1:
        if st.button("⚖️ Convene Tribunal", type="primary", use_container_width=True):
            if not caso_descripcion:
                st.warning("⚠️ Please describe a case for the tribunal.")
            else:
                # Reset protocolo
                st.session_state['protocolo'] = ProtocoloVeloIgnorancia()
                st.session_state['solicitudes_pendientes'] = []
                
                # 🔧 LIMPIAR EL FLAG DE CASO PENDIENTE
                st.session_state['caso_pendiente_tribunal'] = False
                
                with st.spinner("🏛️ Convening the Adversarial Tribunal..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Execute tribunal
                    config = {
                        'depth': debate_depth,
                        'show_reasoning': show_reasoning,
                        'enable_entropia': enable_entropia
                    }
                    
                    # Simular progreso por fases
                    for fase, mensaje in [
                        (20, "🌟 Noble Engine analyzing (blind debate)..."),
                        (40, "⚔️ Adversarial Engine counter-arguing..."),
                        (60, "🔄 Harmony Corrector synthesizing..."),
                        (80, "👑 Grace Engine arbitrating...")
                    ]:
                        status_text.text(mensaje)
                        progress_bar.progress(fase)
                        time.sleep(0.8)
                    
                    resultado = ejecutar_tribunal(caso_descripcion, config)
                    
                    # Check for pending requests
                    if resultado.get('solicitudes_modulos'):
                        st.session_state['solicitudes_pendientes'] = resultado['solicitudes_modulos']
                        st.session_state['debate_en_pausa'] = True
                        progress_bar.progress(90)
                        status_text.text("⏸️ Debate paused - Pending module request")
                        time.sleep(1)
                        st.rerun()
                    else:
                        progress_bar.progress(100)
                        status_text.text("✅ Tribunal completed")
                    
                    time.sleep(0.5)
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Store result
                    resultado['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state['current_debate'] = resultado
                    st.session_state['tribunal_history'].append(resultado)
    
    with col_exec2:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state['caso_actual'] = ''
            st.session_state['current_debate'] = None
            st.session_state['protocolo'] = ProtocoloVeloIgnorancia()
            st.session_state['solicitudes_pendientes'] = []
            st.session_state['caso_pendiente_tribunal'] = False
            st.rerun()
else:
    st.info("⏸️ Debate paused. Please respond to module requests above.")

# Display results
if st.session_state.get('current_debate'):
    resultado = st.session_state['current_debate']
    
    st.markdown("---")
    st.markdown("## 🎭 Tripartite Debate")
    
    # Display weights
    st.markdown("""
    <div style='text-align: center; margin: 20px 0;'>
        <span class='peso-badge peso-noble'>Noble Engine: 30%</span>
        <span class='peso-badge peso-adversario'>Adversarial Engine: 30%</span>
        <span class='peso-badge peso-armonia'>Harmony Corrector: 40%</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Three motors
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="motor-card motor-noble">
            <h3>🌟 Noble Engine</h3>
            <p style='font-style: italic; color: #666;'>"The Idealist"</p>
        </div>
        """, unsafe_allow_html=True)
        
        noble = resultado.get('motor_noble', {})
        st.write(noble.get('posicion', ''))
        if show_reasoning and noble.get('razonamiento'):
            with st.expander("🔍 Reasoning"):
                for paso in noble['razonamiento']:
                    st.markdown(f"• {paso}")
        st.metric("Agency Score", f"{noble.get('agency_score', 0)}/100")
    
    with col2:
        st.markdown("""
        <div class="motor-card motor-adversario">
            <h3>⚔️ Adversarial Engine</h3>
            <p style='font-style: italic; color: #666;'>"The Skeptic"</p>
        </div>
        """, unsafe_allow_html=True)
        
        adv = resultado.get('motor_adversario', {})
        st.write(adv.get('contra_argumentos', ''))
        if adv.get('consecuencias_no_previstas'):
            with st.expander("⚠️ Consequences"):
                for c in adv['consecuencias_no_previstas']:
                    st.markdown(f"• {c}")
        st.metric("Risks", adv.get('riesgos_count', 0))
    
    with col3:
        st.markdown("""
        <div class="motor-card motor-armonia">
            <h3>🔄 Harmony Corrector</h3>
            <p style='font-style: italic; color: #666;'>"The Synthesizer"</p>
        </div>
        """, unsafe_allow_html=True)
        
        arm = resultado.get('corrector_armonia', {})
        st.write(arm.get('sintesis', ''))
        if arm.get('recomendacion'):
            st.info(arm['recomendacion'])
        st.metric("Balance", f"{arm.get('balance_score', 0)}/100")
    
    # Convergence
    st.divider()
    st.markdown("### 📊 Convergence Metric")
    convergencia = resultado.get('convergencia', 50)
    st.markdown(f"""
    <div class="convergence-meter">
        <div class="convergence-indicator" style="left: {convergencia}%;"></div>
    </div>
    <div style='text-align: center; margin-top: 10px;'>
        <span style='float: left;'>◀ Divergence</span>
        <strong>Convergence: {convergencia}%</strong>
        <span style='float: right;'>Consensus ▶</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Entropía Causal
    if enable_entropia and resultado.get('entropia_causal'):
        st.divider()
        entropia = resultado['entropia_causal']
        
        st.markdown(f"""
        <div class="entropia-panel">
            <h3>🔬 Causal Entropy Module</h3>
            <p style='font-style: italic;'>"The Thermodynamics of Decision"</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_e1, col_e2, col_e3, col_e4 = st.columns(4)
        with col_e1:
            st.metric("CR Score", f"{entropia['cr_score']}/100",
                     help="Reconstruction Cost")
        with col_e2:
            st.metric("Collapsed Futures", entropia['futuros_colapsados_count'])
        with col_e3:
            st.metric("Irreversibility", f"{entropia['irreversibilidad']}/10")
        with col_e4:
            st.metric("Classification", entropia['clasificacion'])
        
        if entropia.get('alertas'):
            st.warning("⚠️ Entropy Alerts:")
            for alerta in entropia['alertas']:
                st.markdown(f"• {alerta}")
    
    # Motor de Gracia
    st.divider()
    st.markdown("""
    <div class="arbitro-panel">
        <h2 style='text-align: center;'>👑 Grace Engine Arbitration</h2>
        <p style='text-align: center; font-style: italic;'>
        "The arbiter evaluates debate quality, does not vote"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    gracia = resultado.get('motor_gracia', {})
    
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        st.metric("Grace Score", f"{gracia.get('grace_score', 0)}/100")
    with col_g2:
        st.metric("Certainty", f"{gracia.get('certeza', 0)}%")
    with col_g3:
        st.metric("Coherence", f"{gracia.get('coherencia_logica', 0)}/10")
    
    st.write(gracia.get('evaluacion', ''))
    
    # Alarma del Sistema
    if resultado.get('alarma'):
        st.divider()
        alarma = resultado['alarma']
        nivel = alarma['nivel']
        
        clase_css = {
            'PARADOJA_IRRESOLUBLE': 'alarma-negra',
            'RIESGO_MODO_DIOS': 'alarma-roja',
            'INCONSISTENCIA_CRITICA': 'alarma-morada',
            'DIVERGENCIA_ALTA': 'alarma-naranja',
            'TENSION_MODERADA': 'alarma-amarilla',
            'GEMA_LOGICA_VALIDADA': 'alarma-verde'
        }.get(nivel, 'alarma-amarilla')
        
        st.markdown(f"""
        <div class="alarma-panel {clase_css}">
            <h3>🚨 {nivel.replace('_', ' ')}</h3>
            <p>{alarma['mensaje']}</p>
            <p><strong>Action:</strong> {alarma['accion_requerida']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Veredicto Final
    st.markdown("---")
    veredicto = resultado.get('veredicto_final', 'Pending')
    st.markdown(f"""
    <div class="veredicto-final">
        <h2>⚖️ FINAL VERDICT</h2>
        <h1 style='margin: 20px 0; font-size: 3em;'>{veredicto.upper()}</h1>
        <p style='font-size: 1.2em;'>{resultado.get('justificacion_final', '')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔧 Technical Details"):
        st.json(resultado)
    
    # Actions
    st.divider()
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        if st.button("💾 Save", use_container_width=True):
            st.download_button(
                "⬇️ Download",
                data=json.dumps(resultado, indent=2, ensure_ascii=False),
                file_name=f"tribunal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

st.markdown("---")
st.caption("⚖️ Tripartite Tribunal System | Veil of Ignorance Protocol | Moralogy Framework")
