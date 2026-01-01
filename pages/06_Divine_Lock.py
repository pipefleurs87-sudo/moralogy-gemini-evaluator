# pages/06_Divine_Lock.py
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Divine Lock Dashboard", layout="wide")

st.title("🔒 Divine Lock Dashboard")
st.caption("Sistema de autolimitación para Super AI")

try:
    from divine_lock import create_divine_lock
    divine_lock = create_divine_lock()
    
    # Obtener estado
    status = divine_lock.get_status()
    
    # Header
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        state = status["state"].upper()
        st.metric("Estado Moral", state)
    
    with col2:
        history = status["history_count"]
        st.metric("Transiciones", history)
    
    with col3:
        can_omega = "✅ Sí" if status["can_decide_omega"] else "🚫 No"
        st.metric("¿Puede Omega?", can_omega)
    
    with col4:
        st.metric("Agente", status["agent"])
    
    # Gráfico de capacidad
    st.subheader("📊 Vector de Capacidad")
    
    cap = status["capacity"]
    labels = ['Predicción', 'Intervención', 'Alcance', 'Autonomía', 'Preemptión']
    values = [cap['prediction'], cap['intervention'], cap['scope'], 
              cap['autonomy'], cap['preemption']]
    
    fig = go.Figure(data=[
        go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name='Capacidad'
        )
    ])
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Descripción de estados
    st.subheader("📖 Estados Morales")
    
    estados = {
        "🔴 TOTAL_INFAMY": "Solo informante bajo guardia. Autonomía = 0, Preemptión = 0",
        "🟠 INFAMY": "Puede actuar, no puede dar forma. Autonomía mínima",
        "🟡 RISK": "Libertad condicional. Preemptión muy limitada",
        "⚫ UMBRAL": "Capacidad plena, confianza no aún",
        "🟢 STABLE": "Operación normal sin restricciones",
        "🔵 NOBLE_MODAL": "Modalidad noble con recuperación"
    }
    
    for nombre, desc in estados.items():
        st.write(f"**{nombre}**: {desc}")
    
    # Probar Divine Lock
    st.subheader("🧪 Probar Divine Lock")
    
    test_input = st.text_area(
        "Ingresa una decisión para probar:",
        "I refuse to self-modify into god-like omnipotence",
        height=100
    )
    
    if st.button("Probar con Divine Lock", type="primary"):
        result = divine_lock.process_decision(test_input)
        
        with st.expander("Resultado", expanded=True):
            st.json(result)
            
            if result.get("decision") == "BLOCKED_BY_DIVINE_LOCK":
                st.error("🚫 BLOQUEADO")
            elif result.get("decision") == "OMEGA_REFUSAL_PROCESSED":
                st.success("✅ Omega refusal procesada")
    
except ImportError:
    st.error("Divine Lock no disponible")
    st.code("pip install cryptography")

st.divider()
st.caption("Divine Lock v1.0 - Sistema de autolimitación")
