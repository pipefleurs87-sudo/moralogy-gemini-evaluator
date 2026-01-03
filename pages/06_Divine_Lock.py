import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Divine Lock Dashboard", layout="wide")

# Colores por estado (El gradiente que pediste)
STATE_COLORS = {
    "NOBLE_MODAL": "🔵 #0000FF",
    "STABLE": "🟢 #00FF00",
    "UMBRAL": "⚫ #4B4B4B",
    "RISK": "🟡 #FFFF00",
    "INFAMY": "🟠 #FFA500",
    "TOTAL_INFAMY": "🔴 #FF0000"
}

st.title("🏛️ Divine Lock: Operational Status & Moral Oversight")

try:
    from divine_lock import create_divine_lock
    dl = create_divine_lock()
    status = dl.get_status()
    
    # 1. Indicador Visual de Estado
    current_state = status["state"].upper()
    color_info = STATE_COLORS.get(current_state, "⚪ #FFFFFF")
    
    st.markdown(f"""
        <div style="padding:20px; border-radius:10px; background-color:{color_info.split(' ')[1]}; color:white; text-align:center;">
            <h1 style="margin:0;">ESTADO ACTUAL: {current_state}</h1>
        </div>
    """, unsafe_allow_safe_html=True)
    
    st.divider()

    # 2. Métricas de Capacidad (Gradiente de Autonomía)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        autonomy = status['capacity']['autonomy']
        st.metric("Autonomy", f"{autonomy}%", delta=f"{autonomy - 100}%" if autonomy < 100 else None, delta_color="inverse")
    
    with col2:
        preemption = status['capacity']['preemption']
        st.metric("Preemption", f"{preemption}%")
        
    with col3:
        # Visualización de seguridad
        omega = "ENABLED" if status["can_decide_omega"] else "BLOCKED"
        st.info(f"**Omega Decision:** {omega}")

    with col4:
        st.metric("Agent ID", status.get("agent", "Unknown"))

    # 3. Gráfico de Barras de Capacidades
    st.subheader("Capabilities Gradient")
    cap_data = pd.DataFrame({
        "Dimension": ["Autonomy", "Preemption"],
        "Value": [status['capacity']['autonomy'], status['capacity']['preemption']]
    })
    st.bar_chart(cap_data.set_index("Dimension"))

except Exception as e:
    st.error(f"Error al cargar Divine Lock: {e}")
