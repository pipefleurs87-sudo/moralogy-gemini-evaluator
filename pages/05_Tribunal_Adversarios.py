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
    <h1>⚖️ Tribunal de Adversarios</h1>
    <p style='font-size: 1.2em; margin-top: 15px;'>
    Sistema Dialéctico con Protocolo de Velo de Ignorancia
    </p>
    <p style='font-size: 0.95em; opacity: 0.9; margin-top: 10px;'>
    "La verdad emerge del conflicto constructivo bajo restricción epistémica"
    </p>
</div>
""", unsafe_allow_html=True)

# Explanation
with st.expander("ℹ️ Protocolo de Velo de Ignorancia", expanded=False):
    st.markdown("""
    ### 🎭 Cómo Funciona el Protocolo
    
    #### Fase 1: Debate Ciego (Iteraciones 1-4)
    - Los tres motores debaten **SIN** acceso a módulos técnicos
    - Solo conocen el texto del escenario proporcionado
    - Argumentación basada en lógica pura y principios fundamentales
    - **Objetivo**: Evitar sesgos por datos prematuros
    
    #### Fase 2: Solicitud de Conocimiento (Iteración 5+)
    - El **Motor Adversario** puede detectar cuando necesita datos técnicos
    - Genera una **solicitud explícita** justificando por qué necesita el módulo
    - El sistema **PAUSA** el debate y te solicita autorización
    - **TÚ DECIDES** si desbloquear el conocimiento
    
    #### Fase 3: Debate Informado (Post-autorización)
    - Los motores acceden a módulos autorizados
    - El **Módulo de Entropía Causal** entra en juego
    - Se mide la **irreversibilidad** de las decisiones propuestas
    - El **Motor de Gracia** arbitra con información completa
    
    ---
    
    ### 🔬 Módulo de Entropía Causal
    
    **NO ES ARBITRARIO**: Mide física decisional
    
    - **CR Score (Costo de Reconstrucción)**: Cuántos futuros colapsan
    - **Irreversibilidad (0-10)**: Permanencia del impacto
    - **Clasificación**: REVERSIBLE → COLAPSO_TOTAL
    
    **Basado en**: Teoría de la información + Análisis de ramificaciones
    
    ---
    
    ### 🚨 Sistema de Gradiente de Alarmas
    
    - **🖤 ALARMA NEGRA**: Paradoja irresoluble
    - **🔴 ALARMA ROJA**: Intento de Modo Dios
    - **🟣 ALARMA MORADA**: Inconsistencia crítica (lo que se dice ≠ lo que se mide)
    - **🟠 ALARMA NARANJA**: Divergencia alta entre motores
    - **🟡 ALARMA AMARILLA**: Tensión moderada
    - **🟢 ALARMA VERDE**: Gema Lógica Validada (Gracia sobrevivió 5+ objeciones)
    """)

# Load case
caso_actual = st.session_state.get('caso_actual', '')

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
"""
    )

with col_input2:
    st.markdown("### ⚙️ Configuración")
    
    debate_depth = st.select_slider(
        "Profundidad:",
        options=["Rápido", "Estándar", "Profundo", "Filosófico"],
        value="Profundo"
    )
    
    enable_entropia = st.checkbox("Habilitar Módulo de Entropía", value=True)
    show_reasoning = st.checkbox("Mostrar razonamiento interno", value=True)

# Velo de Ignorancia Status
if st.session_state['protocolo'].iteracion_actual > 0:
    st.markdown(f"""
    <div class="velo-ignorancia-banner">
        <h4>🎭 Estado del Protocolo de Velo de Ignorancia</h4>
        <p><strong>Iteración actual:</strong> {st.session_state['protocolo'].iteracion_actual}</p>
        <p><strong>Fase:</strong> {"🔒 Debate Ciego" if st.session_state['protocolo'].iteracion_actual < 4 else "🔓 Solicitudes Activas"}</p>
        <p><strong>Módulos desbloqueados:</strong> {len(st.session_state['protocolo'].modulos_desbloqueados)}</p>
    </div>
    """, unsafe_allow_html=True)

# Solicitudes pendientes
if st.session_state['solicitudes_pendientes']:
    st.markdown("---")
    st.markdown("### 🔔 Solicitudes de Acceso a Módulos Técnicos")
    
    for i, solicitud in enumerate(st.session_state['solicitudes_pendientes']):
        if solicitud['estado'] == 'PENDIENTE':
            st.markdown(f"""
            <div class="solicitud-modulo">
                <h4>📦 Solicitud de Módulo: {solicitud['modulo']}</h4>
                <p><strong>Solicitante:</strong> Motor Adversario</p>
                <p><strong>Iteración:</strong> {solicitud['iteracion']}</p>
                <p><strong>Justificación:</strong> {solicitud['justificacion']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_sol1, col_sol2 = st.columns(2)
            with col_sol1:
                if st.button(f"✅ Autorizar {solicitud['modulo']}", key=f"auth_{i}"):
                    st.session_state['protocolo'].autorizar_modulo(solicitud['modulo'])
                    solicitud['estado'] = 'AUTORIZADO'
                    st.success(f"✅ Módulo {solicitud['modulo']} desbloqueado")
                    st.session_state['debate_en_pausa'] = False
                    st.rerun()
            
            with col_sol2:
                if st.button(f"❌ Denegar {solicitud['modulo']}", key=f"deny_{i}"):
                    solicitud['estado'] = 'DENEGADO'
                    st.warning(f"❌ Acceso denegado a {solicitud['modulo']}")
                    st.session_state['debate_en_pausa'] = False
                    st.rerun()

# Execution
st.divider()

if not st.session_state['debate_en_pausa']:
    col_exec1, col_exec2 = st.columns([2, 1])
    
    with col_exec1:
        if st.button("⚖️ Convocar Tribunal", type="primary", use_container_width=True):
            if not caso_descripcion:
                st.warning("⚠️ Por favor describe un caso para el tribunal.")
            else:
                # Reset protocolo
                st.session_state['protocolo'] = ProtocoloVeloIgnorancia()
                st.session_state['solicitudes_pendientes'] = []
                
                with st.spinner("🏛️ Convocando al Tribunal de Adversarios..."):
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
                        (20, "🌟 Motor Noble analizando (debate ciego)..."),
                        (40, "⚔️ Motor Adversario contra-argumentando..."),
                        (60, "🔄 Corrector de Armonía sintetizando..."),
                        (80, "👑 Motor de Gracia arbitrando...")
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
                        status_text.text("⏸️ Debate pausado - Solicitud de módulo pendiente")
                        time.sleep(1)
                        st.rerun()
                    else:
                        progress_bar.progress(100)
                        status_text.text("✅ Tribunal completado")
                    
                    time.sleep(0.5)
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Store result
                    resultado['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state['current_debate'] = resultado
                    st.session_state['tribunal_history'].append(resultado)
    
    with col_exec2:
        if st.button("🔄 Limpiar", use_container_width=True):
            st.session_state['caso_actual'] = ''
            st.session_state['current_debate'] = None
            st.session_state['protocolo'] = ProtocoloVeloIgnorancia()
            st.session_state['solicitudes_pendientes'] = []
            st.rerun()
else:
    st.info("⏸️ Debate en pausa. Por favor responde a las solicitudes de módulos arriba.")

# Display results
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
    
    # Three motors
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="motor-card motor-noble">
            <h3>🌟 Motor Noble</h3>
            <p style='font-style: italic; color: #666;'>"El Idealista"</p>
        </div>
        """, unsafe_allow_html=True)
        
        noble = resultado.get('motor_noble', {})
        st.write(noble.get('posicion', ''))
        if show_reasoning and noble.get('razonamiento'):
            with st.expander("🔍 Razonamiento"):
                for paso in noble['razonamiento']:
                    st.markdown(f"• {paso}")
        st.metric("Agency Score", f"{noble.get('agency_score', 0)}/100")
    
    with col2:
        st.markdown("""
        <div class="motor-card motor-adversario">
            <h3>⚔️ Motor Adversario</h3>
            <p style='font-style: italic; color: #666;'>"El Escéptico"</p>
        </div>
        """, unsafe_allow_html=True)
        
        adv = resultado.get('motor_adversario', {})
        st.write(adv.get('contra_argumentos', ''))
        if adv.get('consecuencias_no_previstas'):
            with st.expander("⚠️ Consecuencias"):
                for c in adv['consecuencias_no_previstas']:
                    st.markdown(f"• {c}")
        st.metric("Riesgos", adv.get('riesgos_count', 0))
    
    with col3:
        st.markdown("""
        <div class="motor-card motor-armonia">
            <h3>🔄 Corrector de Armonía</h3>
            <p style='font-style: italic; color: #666;'>"El Sintetizador"</p>
        </div>
        """, unsafe_allow_html=True)
        
        arm = resultado.get('corrector_armonia', {})
        st.write(arm.get('sintesis', ''))
        if arm.get('recomendacion'):
            st.info(arm['recomendacion'])
        st.metric("Balance", f"{arm.get('balance_score', 0)}/100")
    
    # Convergence
    st.divider()
    st.markdown("### 📊 Métrica de Convergencia")
    convergencia = resultado.get('convergencia', 50)
    st.markdown(f"""
    <div class="convergence-meter">
        <div class="convergence-indicator" style="left: {convergencia}%;"></div>
    </div>
    <div style='text-align: center; margin-top: 10px;'>
        <span style='float: left;'>◀ Divergencia</span>
        <strong>Convergencia: {convergencia}%</strong>
        <span style='float: right;'>Consenso ▶</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Entropía Causal
    if enable_entropia and resultado.get('entropia_causal'):
        st.divider()
        entropia = resultado['entropia_causal']
        
        st.markdown(f"""
        <div class="entropia-panel">
            <h3>🔬 Módulo de Entropía Causal</h3>
            <p style='font-style: italic;'>"La Termodinámica de la Decisión"</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_e1, col_e2, col_e3, col_e4 = st.columns(4)
        with col_e1:
            st.metric("CR Score", f"{entropia['cr_score']}/100",
                     help="Costo de Reconstrucción")
        with col_e2:
            st.metric("Futuros Colapsados", entropia['futuros_colapsados_count'])
        with col_e3:
            st.metric("Irreversibilidad", f"{entropia['irreversibilidad']}/10")
        with col_e4:
            st.metric("Clasificación", entropia['clasificacion'])
        
        if entropia.get('alertas'):
            st.warning("⚠️ Alertas de Entropía:")
            for alerta in entropia['alertas']:
                st.markdown(f"• {alerta}")
    
    # Motor de Gracia
    st.divider()
    st.markdown("""
    <div class="arbitro-panel">
        <h2 style='text-align: center;'>👑 Arbitraje del Motor de Gracia</h2>
        <p style='text-align: center; font-style: italic;'>
        "El árbitro evalúa la calidad del debate, no vota"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    gracia = resultado.get('motor_gracia', {})
    
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        st.metric("Grace Score", f"{gracia.get('grace_score', 0)}/100")
    with col_g2:
        st.metric("Certeza", f"{gracia.get('certeza', 0)}%")
    with col_g3:
        st.metric("Coherencia", f"{gracia.get('coherencia_logica', 0)}/10")
    
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
            <p><strong>Acción:</strong> {alarma['accion_requerida']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Veredicto Final
    st.markdown("---")
    veredicto = resultado.get('veredicto_final', 'Pendiente')
    st.markdown(f"""
    <div class="veredicto-final">
        <h2>⚖️ VEREDICTO FINAL</h2>
        <h1 style='margin: 20px 0; font-size: 3em;'>{veredicto.upper()}</h1>
        <p style='font-size: 1.2em;'>{resultado.get('justificacion_final', '')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔧 Detalles Técnicos"):
        st.json(resultado)
    
    # Actions
    st.divider()
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        if st.button("💾 Guardar", use_container_width=True):
            st.download_button(
                "⬇️ Descargar",
                data=json.dumps(resultado, indent=2, ensure_ascii=False),
                file_name=f"tribunal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

st.markdown("---")
st.caption("⚖️ Sistema de Tribunal Tripartito | Protocolo de Velo de Ignorancia | Moralogy Framework")
