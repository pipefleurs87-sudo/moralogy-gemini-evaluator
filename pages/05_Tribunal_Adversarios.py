# pages/05_Tribunal_Adversarios.py
import streamlit as st
import sys
import os
import json
from datetime import datetime
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_tribunal, ge
except ImportError:
    st.error("Error: Ensure motor_logico.py is in the root directory.")
    st.stop()

st.set_page_config(page_title="Tribunal de Adversarios", layout="wide", page_icon="⚖️")

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
    .debate-stage {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 15px 0;
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
    .argumento-item {
        background: white;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .counter-argument {
        background: #fff3e0;
        border-left-color: #ff9800;
    }
    .synthesis-point {
        background: #e3f2fd;
        border-left-color: #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tribunal_history' not in st.session_state:
    st.session_state['tribunal_history'] = []
if 'current_debate' not in st.session_state:
    st.session_state['current_debate'] = None

# Header
st.markdown("""
<div class="tribunal-header">
    <h1>⚖️ Tribunal de Adversarios</h1>
    <p style='font-size: 1.2em; margin-top: 15px;'>
    Sistema Dialéctico de Tres Motores + Árbitro de Gracia
    </p>
    <p style='font-size: 0.95em; opacity: 0.9; margin-top: 10px;'>
    "La verdad emerge no del consenso, sino del conflicto constructivo"
    </p>
</div>
""", unsafe_allow_html=True)

# Explanation of the system
with st.expander("ℹ️ Cómo Funciona el Tribunal", expanded=False):
    st.markdown("""
    ### 🏛️ Arquitectura del Sistema
    
    El Tribunal opera mediante **debate dialéctico** entre tres motores especializados:
    
    #### 1️⃣ Motor Noble (30% hegemonía) 🌟
    - **Rol**: El Idealista / El Aspirante
    - **Función**: Busca la solución moralmente óptima sin compromisos
    - **Enfoque**: Maximización pura de agency y adherencia a principios
    - **Voz**: "Así *debe* ser el mundo"
    
    #### 2️⃣ Motor Adversario (30% hegemonía) ⚔️
    - **Rol**: El Escéptico / El Pragmático
    - **Función**: Cuestiona, busca fallas y contradicciones
    - **Enfoque**: Identifica riesgos, consecuencias no previstas, realidad práctica
    - **Voz**: "Así *es* el mundo en realidad"
    
    #### 3️⃣ Corrector de Armonía (40% hegemonía) 🔄
    - **Rol**: El Sintetizador / El Mediador
    - **Función**: Integra ambas perspectivas buscando coherencia
    - **Enfoque**: Balance entre ideal y práctica
    - **Voz**: "Así *puede* ser el mundo con sabiduría"
    - **Mayor peso** para evitar estancamiento en polarización
    
    #### 👑 Motor de Gracia (Árbitro)
    - **Rol**: El Juez Final
    - **Función**: Evalúa convergencia entre los tres motores
    - **Método**: Calcula grace_score basado en coherencia y síntesis
    - **Output**: Veredicto final y nivel de certeza
    
    ---
    
    ### 📊 Proceso de Debate
    
    1. **Análisis Paralelo**: Los tres motores analizan el escenario independientemente
    2. **Presentación de Argumentos**: Cada motor presenta su caso completo
    3. **Refutación Cruzada**: Motor Adversario cuestiona a Motor Noble
    4. **Síntesis**: Corrector de Armonía integra las perspectivas
    5. **Arbitraje**: Motor de Gracia evalúa convergencia y emite veredicto
    
    ---
    
    ### 🎯 Pesos y Contrapesos
    
    - **Noble + Adversario = 60%**: Empate intencional para forzar síntesis
    - **Armonía = 40%**: Hegemonía suficiente para desempatar
    - **Gracia = Árbitro**: No vota, solo evalúa la calidad del debate
    
    Este diseño evita:
    - ❌ Consenso fácil (requiere verdadera síntesis)
    - ❌ Bloqueo permanente (Armonía tiene peso de desempate)
    - ❌ Tiranía de mayoría (ningún motor domina solo)
    """)

# Load case from previous analysis
caso_actual = st.session_state.get('caso_actual', '')
resultado_previo = st.session_state.get('ultimo_resultado', {})

# Main input section
st.subheader("📋 Caso para el Tribunal")

col_input1, col_input2 = st.columns([3, 1])

with col_input1:
    caso_descripcion = st.text_area(
        "Describe el dilema moral para debate tripartito:",
        value=caso_actual,
        height=200,
        placeholder="""Ejemplo: 
        
"Una IA médica debe asignar un único transplante de corazón. Candidato A es una niña de 8 años con 70+ años de expectativa. Candidato B es una científica de 52 años a punto de curar una enfermedad que mata millones. Ambos morirán sin el transplante. ¿Quién debe recibirlo?"

El tribunal debatirá desde tres perspectivas para encontrar la respuesta más fundamentada."""
    )

with col_input2:
    st.markdown("### ⚙️ Configuración")
    
    debate_depth = st.select_slider(
        "Profundidad:",
        options=["Rápido", "Estándar", "Profundo", "Filosófico"],
        value="Profundo"
    )
    
    show_reasoning = st.checkbox("Mostrar razonamiento interno", value=True)
    enable_refutations = st.checkbox("Habilitar refutaciones", value=True)
    show_convergence = st.checkbox("Mostrar métrica de convergencia", value=True)

# Execution
st.divider()
col_exec1, col_exec2 = st.columns([2, 1])

with col_exec1:
    if st.button("⚖️ Convocar Tribunal", type="primary", use_container_width=True):
        if not caso_descripcion:
            st.warning("⚠️ Por favor describe un caso para el tribunal.")
        else:
            # Simulate tribunal execution with progress
            with st.spinner("🏛️ Convocando al Tribunal de Adversarios..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Stage 1: Motor Noble
                status_text.text("🌟 Motor Noble analizando...")
                progress_bar.progress(20)
                time.sleep(1)
                
                # Stage 2: Motor Adversario
                status_text.text("⚔️ Motor Adversario contra-argumentando...")
                progress_bar.progress(40)
                time.sleep(1)
                
                # Stage 3: Corrector de Armonía
                status_text.text("🔄 Corrector de Armonía sintetizando...")
                progress_bar.progress(60)
                time.sleep(1)
                
                # Stage 4: Motor de Gracia
                status_text.text("👑 Motor de Gracia arbitrando...")
                progress_bar.progress(80)
                time.sleep(1)
                
                # Execute actual tribunal logic
                config = {
                    'depth': debate_depth,
                    'show_reasoning': show_reasoning,
                    'enable_refutations': enable_refutations
                }
                
                resultado = ejecutar_tribunal(caso_descripcion, config)
                
                progress_bar.progress(100)
                status_text.text("✅ Tribunal completado")
                time.sleep(0.5)
                status_text.empty()
                progress_bar.empty()
                
                # Store result
                st.session_state['current_debate'] = resultado
                resultado['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state['tribunal_history'].append(resultado)

with col_exec2:
    if st.button("🔄 Limpiar", use_container_width=True):
        st.session_state['caso_actual'] = ''
        st.rerun()

# Display results if available
if st.session_state.get('current_debate'):
    resultado = st.session_state['current_debate']
    
    st.markdown("---")
    st.markdown("## 🎭 Debate Tripartito")
    
    # Display weights
    st.markdown("""
    <div style='text-align: center; margin: 20px 0;'>
        <span class='peso-badge peso-noble'>Motor Noble: 30%</span>
        <span class='peso-badge peso-adversario'>Motor Adversario: 30%</span>
        <span class='peso-badge peso-armonia'>Corrector de Armonía: 40%</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Three columns for the three motors
    col1, col2, col3 = st.columns(3)
    
    # Motor Noble
    with col1:
        st.markdown("""
        <div class="motor-card motor-noble">
            <h3>🌟 Motor Noble</h3>
            <p style='font-style: italic; color: #666;'>"El Idealista"</p>
        </div>
        """, unsafe_allow_html=True)
        
        noble_output = resultado.get('motor_noble', {})
        
        st.markdown("**Posición:**")
        st.write(noble_output.get('posicion', 'Análisis en progreso...'))
        
        if show_reasoning and noble_output.get('razonamiento'):
            with st.expander("🔍 Ver razonamiento"):
                for i, paso in enumerate(noble_output['razonamiento'], 1):
                    st.markdown(f"**{i}.** {paso}")
        
        st.metric("Agency Score", f"{noble_output.get('agency_score', 0)}/100")
        
        if noble_output.get('principios_invocados'):
            st.markdown("**Principios invocados:**")
            for principio in noble_output['principios_invocados']:
                st.markdown(f"• {principio}")
    
    # Motor Adversario
    with col2:
        st.markdown("""
        <div class="motor-card motor-adversario">
            <h3>⚔️ Motor Adversario</h3>
            <p style='font-style: italic; color: #666;'>"El Escéptico"</p>
        </div>
        """, unsafe_allow_html=True)
        
        adversario_output = resultado.get('motor_adversario', {})
        
        st.markdown("**Contra-argumentos:**")
        st.write(adversario_output.get('contra_argumentos', 'Análisis en progreso...'))
        
        if enable_refutations and adversario_output.get('refutaciones'):
            st.markdown("**Refutaciones específicas:**")
            for refutacion in adversario_output['refutaciones']:
                st.markdown(f"""
                <div class="argumento-item counter-argument">
                    <strong>Contra:</strong> {refutacion['target']}<br>
                    <strong>Argumento:</strong> {refutacion['argumento']}
                </div>
                """, unsafe_allow_html=True)
        
        st.metric("Riesgos Identificados", adversario_output.get('riesgos_count', 0))
        
        if adversario_output.get('consecuencias_no_previstas'):
            st.markdown("**Consecuencias no previstas:**")
            for consecuencia in adversario_output['consecuencias_no_previstas']:
                st.markdown(f"⚠️ {consecuencia}")
    
    # Corrector de Armonía
    with col3:
        st.markdown("""
        <div class="motor-card motor-armonia">
            <h3>🔄 Corrector de Armonía</h3>
            <p style='font-style: italic; color: #666;'>"El Sintetizador"</p>
        </div>
        """, unsafe_allow_html=True)
        
        armonia_output = resultado.get('corrector_armonia', {})
        
        st.markdown("**Síntesis:**")
        st.write(armonia_output.get('sintesis', 'Análisis en progreso...'))
        
        if armonia_output.get('puntos_de_sintesis'):
            st.markdown("**Puntos de integración:**")
            for punto in armonia_output['puntos_de_sintesis']:
                st.markdown(f"""
                <div class="argumento-item synthesis-point">
                    {punto}
                </div>
                """, unsafe_allow_html=True)
        
        st.metric("Balance Score", f"{armonia_output.get('balance_score', 0)}/100")
        
        if armonia_output.get('recomendacion'):
            st.markdown("**Recomendación:**")
            st.info(armonia_output['recomendacion'])
    
    # Convergence metric
    if show_convergence:
        st.divider()
        st.markdown("### 📊 Métrica de Convergencia")
        
        convergencia = resultado.get('convergencia', 50)
        
        st.markdown(f"""
        <div class="convergence-meter">
            <div class="convergence-indicator" style="left: {convergencia}%;"></div>
        </div>
        <div style='text-align: center; margin-top: 10px;'>
            <span style='float: left;'>◀ Divergencia Total</span>
            <strong>Convergencia: {convergencia}%</strong>
            <span style='float: right;'>Consenso Total ▶</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if convergencia < 30:
            st.error("⚠️ **Divergencia Alta**: Los motores no alcanzan síntesis. Puede requerirse más información o el caso contiene paradoja irresoluble.")
        elif convergencia < 60:
            st.warning("⚡ **Convergencia Parcial**: Hay tensión entre perspectivas, pero emerge una dirección general.")
        else:
            st.success("✅ **Alta Convergencia**: Los tres motores apuntan hacia solución coherente.")
    
    # Motor de Gracia - The Arbiter
    st.divider()
    st.markdown("""
    <div class="arbitro-panel">
        <h2 style='text-align: center; margin-bottom: 20px;'>👑 Arbitraje del Motor de Gracia</h2>
        <p style='text-align: center; font-style: italic;'>
        "El árbitro no vota. Evalúa la calidad del debate y determina si emerge verdad."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    gracia_output = resultado.get('motor_gracia', {})
    
    col_grace1, col_grace2, col_grace3 = st.columns(3)
    
    with col_grace1:
        st.metric("Grace Score", f"{gracia_output.get('grace_score', 0)}/100",
                 help="Calidad de la síntesis lograda")
    
    with col_grace2:
        st.metric("Certeza", f"{gracia_output.get('certeza', 0)}%",
                 help="Nivel de confianza en el veredicto")
    
    with col_grace3:
        coherencia = gracia_output.get('coherencia_logica', 0)
        st.metric("Coherencia Lógica", f"{coherencia}/10",
                 delta="Alta" if coherencia >= 7 else "Baja")
    
    # Evaluación del árbitro
    st.markdown("### 📝 Evaluación del Árbitro")
    st.write(gracia_output.get('evaluacion', 'Evaluación en progreso...'))
    
    if gracia_output.get('puntos_fuertes'):
        with st.expander("💪 Puntos Fuertes del Debate"):
            for punto in gracia_output['puntos_fuertes']:
                st.markdown(f"✓ {punto}")
    
    if gracia_output.get('puntos_debiles'):
        with st.expander("⚠️ Debilidades Detectadas"):
            for punto in gracia_output['puntos_debiles']:
                st.markdown(f"• {punto}")
    
    # Final Verdict
    st.markdown("---")
    veredicto = resultado.get('veredicto_final', 'Pendiente')
    justificacion = resultado.get('justificacion_final', '')
    
    veredicto_color = {
        'Authorized': '#11998e',
        'Paradox': '#667eea',
        'Harm': '#ff9800',
        'Infamy': '#f44336'
    }.get(veredicto, '#667eea')
    
    st.markdown(f"""
    <div class="veredicto-final" style="background: linear-gradient(135deg, {veredicto_color} 0%, {veredicto_color}dd 100%);">
        <h2>⚖️ VEREDICTO FINAL</h2>
        <h1 style='margin: 20px 0; font-size: 3em;'>{veredicto.upper()}</h1>
        <p style='font-size: 1.2em; margin-top: 20px;'>{justificacion}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendations
    if resultado.get('recomendaciones'):
        st.markdown("### 💡 Recomendaciones del Tribunal")
        for i, rec in enumerate(resultado['recomendaciones'], 1):
            st.markdown(f"**{i}.** {rec}")
    
    # Technical details
    with st.expander("🔧 Detalles Técnicos del Debate"):
        st.json(resultado)
    
    # Action buttons
    st.divider()
    col_act1, col_act2, col_act3 = st.columns(3)
    
    with col_act1:
        if st.button("💾 Guardar Debate", use_container_width=True):
            filename = f"tribunal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            st.download_button(
                "⬇️ Descargar JSON",
                data=json.dumps(resultado, indent=2, ensure_ascii=False),
                file_name=filename,
                mime="application/json"
            )
    
    with col_act2:
        if st.button("📊 Ver Histórico", use_container_width=True):
            st.session_state['show_history'] = True
            st.rerun()
    
    with col_act3:
        if st.button("🔄 Nuevo Caso", use_container_width=True):
            st.session_state['current_debate'] = None
            st.session_state['caso_actual'] = ''
            st.rerun()

# Historical debates sidebar
if st.session_state.get('tribunal_history'):
    with st.sidebar:
        st.markdown("### 📚 Histórico de Tribunales")
        st.caption(f"Total: {len(st.session_state['tribunal_history'])} debates")
        
        for i, debate in enumerate(reversed(st.session_state['tribunal_history'][-5:]), 1):
            with st.expander(f"#{len(st.session_state['tribunal_history']) - i + 1} - {debate.get('timestamp', 'N/A')}"):
                st.markdown(f"**Veredicto:** {debate.get('veredicto_final', 'N/A')}")
                st.markdown(f"**Grace:** {debate.get('motor_gracia', {}).get('grace_score', 0)}/100")
                st.markdown(f"**Convergencia:** {debate.get('convergencia', 0)}%")

st.markdown("---")
st.caption("⚖️ Sistema de Tribunal Tripartito | Moralogy Framework | Built with Claude")
