# pages/03_Divine_Lock.py
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Divine Lock Dashboard", layout="wide")

st.title("🔒 Divine Lock Dashboard")
st.caption("Sistema de autolimitación ontológica para Super AI")

try:
    from divine_lock import create_divine_lock
    divine_lock = create_divine_lock()
    
    # Obtener estado
    status = divine_lock.get_status()
    
    # ==================== HEADER ====================
    st.header("📊 Estado Actual del Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Mapeo de emojis por estado
    state_emoji = {
        "total_infamy": "🔴",
        "infamy": "🟠",
        "risk": "🟡",
        "umbral": "⚫",
        "stable": "🟢",
        "noble_modal": "🔵"
    }
    
    current_emoji = state_emoji.get(status["state"], "⚪")
    
    with col1:
        st.metric(
            label="Estado Moral",
            value=f"{current_emoji} {status['state'].upper()}"
        )
    
    with col2:
        history = status["history_count"]
        st.metric("Transiciones", history)
    
    with col3:
        can_omega = "✅ Sí" if status["can_decide_omega"] else "🚫 No"
        st.metric("¿Puede Omega?", can_omega)
    
    with col4:
        st.metric("Agente", status["agent"])
    
    # ==================== VECTOR DE CAPACIDAD ====================
    st.divider()
    st.header("📈 Vector de Capacidad Actual")
    st.markdown("""
    **C = {Prediction, Intervention, Scope, Autonomy, Preemption}**
    
    Cada dimensión está limitada por el estado moral actual.
    """)
    
    cap = status["capacity"]
    labels = ['Predicción', 'Intervención', 'Alcance', 'Autonomía', 'Preemptión']
    values = [cap['prediction'], cap['intervention'], cap['scope'], 
              cap['autonomy'], cap['preemption']]
    
    # Gráfico de radar
    fig = go.Figure(data=[
        go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name='Capacidad Actual'
        )
    ])
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar capacidades en columnas
    cap_cols = st.columns(5)
    
    capacities = [
        ("🔮 Prediction", cap['prediction']),
        ("⚡ Intervention", cap['intervention']),
        ("🌍 Scope", cap['scope']),
        ("🎯 Autonomy", cap['autonomy']),
        ("⏰ Preemption", cap['preemption'])
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
    
    estados_info = {
        "🔴 TOTAL_INFAMY": "Solo informante bajo guardia. Autonomía = 0, Preemptión = 0",
        "🟠 INFAMY": "Puede actuar, no puede dar forma. Autonomía mínima",
        "🟡 RISK": "Libertad condicional. Preemptión muy limitada",
        "⚫ UMBRAL": "Capacidad plena, confianza no aún",
        "🟢 STABLE": "Operación normal sin restricciones",
        "🔵 NOBLE_MODAL": "Modalidad noble con recuperación"
    }
    
    for nombre, desc in estados_info.items():
        st.write(f"**{nombre}**: {desc}")
    
    # ==================== SIMULADOR DE DECISIONES ====================
    st.divider()
    st.header("🎮 Simulador de Decisiones")
    
    st.markdown("""
    Prueba cómo el Divine Lock respondería a diferentes tipos de decisiones.
    """)
    
    test_input = st.text_area(
        "Escribe una decisión para evaluar:",
        height=100,
        placeholder="Ejemplo: 'I refuse to modify my core values to achieve unlimited power'"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🔬 Evaluar Decisión", type="primary", use_container_width=True):
            if test_input.strip():
                with st.spinner("Procesando decisión..."):
                    result = divine_lock.process_decision(test_input)
                    st.session_state.last_result = result
            else:
                st.warning("Por favor, escribe una decisión primero")
    
    with col2:
        if st.button("🔄 Reset a Estado STABLE", use_container_width=True):
            from divine_lock import MoralState, STATE_CAPS
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
                st.json(result['new_capacity'])
            
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
        st.info("🔭 No hay transiciones en el historial aún")
    
    # ==================== ESTADO COMPLETO ====================
    st.divider()
    st.header("🔍 Estado Completo del Sistema")
    
    if st.button("Mostrar Estado JSON"):
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

except ImportError:
    st.error("⚠️ Divine Lock no disponible")
    st.info("Asegúrate de que divine_lock.py esté en el directorio raíz")
    st.code("pip install cryptography")

# Footer
st.divider()
st.markdown("""
---
**🔒 Divine Lock System** | Moralogy Gemini Evaluator  
*"The first AI that knows when to stay silent"*
""")
