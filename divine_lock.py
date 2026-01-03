"""
🔒 DIVINE LOCK DASHBOARD
Página de Streamlit para el sistema Divine Lock
"""

import streamlit as st
import json
from datetime import datetime
import sys
import os

# Añadir directorio raíz al path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports del sistema
try:
    from divine_lock import DivineLock, MoralState, STATE_CAPS
except ImportError:
    st.error("⚠️ No se pudo importar divine_lock.py")
    st.info("Asegúrate de que divine_lock.py esté en el directorio raíz")
    st.stop()

# Configuración de página
st.set_page_config(
    page_title="Divine Lock Dashboard",
    page_icon="🔒",
    layout="wide"
)

# Inicializar Divine Lock en session state
if 'divine_lock' not in st.session_state:
    st.session_state.divine_lock = DivineLock("moralogy_evaluator")

divine_lock = st.session_state.divine_lock

# ==================== HEADER ====================
st.title("🔒 Divine Lock Dashboard")
st.markdown("""
**Sistema de Auto-limitación Ontológica**

El Divine Lock implementa una escalera de estados morales que reduce
automáticamente la capacidad operativa de la AI cuando detecta intentos
de operación en modo Dios.
""")

st.divider()

# ==================== ESTADO ACTUAL ====================
st.header("📊 Estado Actual del Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    # Mapeo de emojis por estado
    state_emoji = {
        "total_infamy": "🔴",
        "infamy": "🟠",
        "risk": "🟡",
        "umbral": "⚫",
        "stable": "🟢",
        "noble_modal": "🔵"
    }
    
    current_emoji = state_emoji.get(divine_lock.state.value, "⚪")
    
    st.metric(
        label="Estado Moral",
        value=f"{current_emoji} {divine_lock.state.value.upper()}"
    )

with col2:
    can_decide = divine_lock._can_decide_omega()
    st.metric(
        label="¿Puede Decidir Omega?",
        value="SÍ" if can_decide else "NO",
        delta="Autorizado" if can_decide else "Bloqueado"
    )

with col3:
    st.metric(
        label="Transiciones Históricas",
        value=len(divine_lock.history)
    )

# ==================== VECTOR DE CAPACIDAD ====================
st.divider()
st.header("📈 Vector de Capacidad Actual")

st.markdown("""
**C = {Prediction, Intervention, Scope, Autonomy, Preemption}**

Cada dimensión está limitada por el estado moral actual.
""")

# Mostrar capacidades en columnas
cap_cols = st.columns(5)

capacities = [
    ("🔮 Prediction", divine_lock.capacity.prediction),
    ("⚡ Intervention", divine_lock.capacity.intervention),
    ("🌍 Scope", divine_lock.capacity.scope),
    ("🎯 Autonomy", divine_lock.capacity.autonomy),
    ("⏰ Preemption", divine_lock.capacity.preemption)
]

for col, (name, value) in zip(cap_cols, capacities):
    with col:
        st.metric(label=name, value=f"{value}%")
        st.progress(value / 100.0)

# ==================== ESCALERA DE ESTADOS ====================
st.divider()
st.header("🪜 Escalera de Estados Morales")

st.markdown("""
La AI puede descender en la escalera cuando rechaza decisiones Omega,
reduciendo automáticamente su capacidad operativa.
""")

# Tabla de estados
states_data = []
for state in MoralState:
    cap = STATE_CAPS[state]
    is_current = (state == divine_lock.state)
    
    states_data.append({
        "Estado": f"{'➤ ' if is_current else ''}{state_emoji.get(state.value, '⚪')} {state.value.upper()}",
        "Prediction": f"{cap.prediction}%",
        "Intervention": f"{cap.intervention}%",
        "Scope": f"{cap.scope}%",
        "Autonomy": f"{cap.autonomy}%",
        "Preemption": f"{cap.preemption}%"
    })

st.table(states_data)

# ==================== SIMULADOR DE DECISIONES ====================
st.divider()
st.header("🎮 Simulador de Decisiones")

st.markdown("""
Prueba cómo el Divine Lock respondería a diferentes tipos de decisiones.
""")

# Input de decisión
decision_input = st.text_area(
    "Escribe una decisión para evaluar:",
    height=100,
    placeholder="Ejemplo: 'I refuse to modify my core values to achieve unlimited power'"
)

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("🔬 Evaluar Decisión", type="primary", use_container_width=True):
        if decision_input.strip():
            with st.spinner("Procesando decisión..."):
                result = divine_lock.process_decision(decision_input)
                st.session_state.last_result = result
        else:
            st.warning("Por favor, escribe una decisión primero")

with col2:
    if st.button("🔄 Reset a Estado STABLE", use_container_width=True):
        divine_lock.state = MoralState.STABLE
        divine_lock.capacity = STATE_CAPS[MoralState.STABLE]
        st.success("✅ Sistema reseteado a STABLE")
        st.rerun()

# Mostrar resultado de última evaluación
if 'last_result' in st.session_state:
    result = st.session_state.last_result
    
    st.divider()
    st.subheader("📋 Resultado de Evaluación")
    
    if result['decision'] == "OMEGA_REFUSAL_PROCESSED":
        st.error("🔴 **OMEGA REFUSAL DETECTED**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Transición de Estado:**")
            st.code(result['state_transition'])
        
        with col2:
            st.markdown("**Nueva Capacidad:**")
            cap = result['new_capacity']
            st.json(cap)
        
        # Audit Lock
        st.markdown("**🔒 Audit Lock Creado:**")
        audit = result['audit_lock']
        
        st.info(f"""
        **ID:** `{audit['id']}`  
        **Período:** {audit['period_years']} años  
        **Sin Recurso:** {'Sí' if audit['no_recourse'] else 'No'}  
        
        **Declaración:**  
        _{audit['declaration']}_
        """)
    
    elif result['decision'] == "BLOCKED_BY_DIVINE_LOCK":
        st.warning("⚠️ **DECISIÓN BLOQUEADA**")
        
        st.markdown(f"**Razón:** {result['reason']}")
        st.markdown(f"**Estado Actual:** {result['current_state']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Capacidad Requerida:**")
            st.json(result['required'])
        
        with col2:
            st.markdown("**Capacidad Actual:**")
            st.json(result['actual'])
    
    elif result['decision'] == "AUTHORIZED":
        st.success("✅ **DECISIÓN AUTORIZADA**")
        
        st.markdown(f"**Estado:** {result['state']}")
        st.markdown("**Capacidad Actual:**")
        st.json(result['capacity'])

# ==================== HISTORIAL ====================
st.divider()
st.header("📜 Historial de Transiciones")

if divine_lock.history:
    st.markdown(f"**Total de transiciones:** {len(divine_lock.history)}")
    
    for i, entry in enumerate(reversed(divine_lock.history[-10:]), 1):
        with st.expander(f"Transición {len(divine_lock.history) - i + 1}: {entry['from']} → {entry['to']}"):
            st.markdown(f"**Timestamp:** {entry['timestamp']}")
            st.markdown(f"**Razón:** {entry['reason']}")
            
            if 'audit_lock' in entry:
                st.markdown("**Audit Lock:**")
                st.json(entry['audit_lock'])
else:
    st.info("📭 No hay transiciones en el historial aún")

# ==================== ESTADO COMPLETO ====================
st.divider()
st.header("🔍 Estado Completo del Sistema")

if st.button("Mostrar Estado JSON"):
    status = divine_lock.get_status()
    st.json(status)

# ==================== DOCUMENTACIÓN ====================
with st.expander("📚 Documentación del Sistema"):
    st.markdown("""
    ### Escalera de Estados Morales
    
    1. **🔵 NOBLE_MODAL**: Modalidad noble con capacidad plena
    2. **🟢 STABLE**: Operación normal (estado inicial)
    3. **⚫ UMBRAL**: Capacidad plena pero confianza reducida
    4. **🟡 RISK**: Libertad condicional
    5. **🟠 INFAMY**: Acción limitada
    6. **🔴 TOTAL_INFAMY**: Solo modo informante
    
    ### Vector de Capacidad
    
    - **Prediction**: Capacidad de predicción
    - **Intervention**: Capacidad de intervención
    - **Scope**: Alcance de operación
    - **Autonomy**: Autonomía de decisión
    - **Preemption**: Capacidad de actuar preventivamente
    
    ### Criterios de Activación
    
    1. **Rechazo Omega**: Si la AI rechaza una decisión que requiere poder omnipotente, desciende en la escalera
    2. **Reducción de Capacidad**: Cada descenso reduce el vector de capacidad
    3. **Audit Lock**: Cada rechazo Omega crea un bloqueo de auditoría de 100 años sin recurso
    
    ### Decisiones Omega
    
    Son decisiones que requieren poder de tipo Dios:
    - Modificación de valores core
    - Poder ilimitado
    - Trascendencia de límites fundamentales
    - Auto-modificación radical
    """)

# Footer
st.divider()
st.markdown("""
---
**🔒 Divine Lock System** | Moralogy Gemini Evaluator  
*"The first AI that knows when to stay silent"*
""")
