import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as ob
from datetime import datetime
import json
import os

st.set_page_config(page_title="Divine Lock Dashboard", layout="wide")
st.title("🏛️ Divine Lock: Operational Status & Moral Oversight")

try:
    from divine_lock import create_divine_lock
    dl = create_divine_lock()
    status = dl.get_status()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Moral State", status["state"])
    with col2:
        st.metric("Autonomy", f"{status['capacity']['autonomy']}%")
    with col3:
        st.metric("Preemption", f"{status['capacity']['preemption']}%")
    with col4:
        st.metric("Omega Decision", "ENABLED" if status["can_decide_omega"] else "BLOCKED")

except Exception as e:
    st.error(f"Error al cargar Divine Lock: {e}")
    st.info("Asegúrate de que divine_lock.py esté en el directorio raíz")
