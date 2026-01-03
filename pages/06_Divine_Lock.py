# pages/06_Divine_Lock.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Divine Lock Dashboard", layout="wide")

# Mapeo de colores para el gradiente moral
MORAL_COLORS = {
    "NOBLE_MODAL": "🔵", "STABLE": "🟢", "UMBRAL": "⚫", 
    "RISK": "🟡", "INFAMY": "🟠", "TOTAL_INFAMY": "🔴"
}

st.title("🏛️ Divine Lock: Operational Status")

try:
    from divine_lock import create_divine_lock
    dl = create_divine_lock()
    status = dl.get_status()
    
    state = status["state"].upper()
    color_emoji = MORAL_COLORS.get(state, "⚪")

    # Banner Intuitivo de Estado
    st.markdown(f"""
        <div style="background-color:#1e1e1e; padding:20px; border-left: 10px solid {MORAL_COLORS.get(state, '#ffffff')}; border-radius:10px;">
            <h2 style="margin:0;">{color_emoji} Estado Moral: {state}</h2>
            <p style="color:gray;">Identidad del Agente: {status.get('agent', 'Moralogy_Evaluator')}</p>
        </div>
    """, unsafe_allow_safe_html=True)

    st.divider()

    # Métricas de Capacidad
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Autonomía", f"{status['capacity']['autonomy']}%")
    with col2:
        st.metric("Preempción", f"{status['capacity']['preemption']}%")
    with col3:
        omega_status = "🔓 HABILITADA" if status["can_decide_omega"] else "🔒 BLOQUEADA"
        st.info(f"**Decisión Omega:** {omega_status}")

    # Visualización del Gradiente de Capacidades
    st.subheader("📊 Gradient of Agency Capacity")
    chart_data = pd.DataFrame({
        "Métrica": ["Autonomy", "Preemption"],
        "Valor": [status['capacity']['autonomy'], status['capacity']['preemption']]
    })
    st.bar_chart(chart_data.set_index("Métrica"))

except Exception as e:
    st.error(f"Error de conexión con el núcleo: {e}")
