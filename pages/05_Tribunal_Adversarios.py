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
    <h1>⚖️ Tribunal de Adversarios</h1>
    <p style='font-size: 1.2em; margin-top: 15px;'>
    Sistema Dialéctico con Protocolo de Velo de Ignorancia
    </p>
    <p style='font-size: 0.95em; opacity: 0.9; margin-top: 10px;'>
    "La verdad emerge del conflicto constructivo bajo restricción epistémica"
    </p>
</div>
""", unsafe_allow_html=True)

# 🔧 MOSTRAR SI HAY UN CASO PENDIENTE DESDE ANÁLISIS AVANZADO
if st.session_state.get('caso_pendiente_tribunal'):
    st.markdown(f"""
    <div class="caso-cargado-banner">
        <h4>📋 Caso cargado desde Análisis Avanzado</h4>
        <p>✅ Un caso ha sido enviado al tribunal y está listo para debate</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar resumen del análisis previo si existe
    if st.session_state.get('ultimo_resultado'):
        with st.expander("📊 Ver análisis previo", expanded=False):
            res = st.session_state['ultimo_resultado']
            col_prev1, col_prev2, col_prev3 = st.columns(3)
            with col_prev1:
                st.metric("Veredicto Previo", res.get('verdict', 'Unknown'))
            with col_prev2:
                st.metric("Agency Score", f"{res.get('agency_score', 0)}/100")
            with col_prev3:
                st.metric("Grace Score", f"{res.get('grace_score', 0)}/100")

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

# Load case - CARGAR DESDE SESSION_STATE SI EXISTE
caso_inicial = st.session_state.get('caso_actual', '')

# Main input section
st.subheader("📋 Caso para el Tribunal")

col_input1, col_input2 = st.columns([3, 1])

with col_input1:
    caso_descripcion = st.text_area(
        "Describe el dilema moral para debate tripartito:",
        value=caso_inicial,
        height=200,
        key="tribunal_caso_input",
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
if st.ses
