import streamlit as st
import pandas as pd

st.set_page_config(page_title="Divine Lock Dashboard", layout="wide")

st.title("🏛️ Divine Lock: Operational Status")

try:
    from divine_lock import create_divine_lock
    dl = create_divine_lock()
    status = dl.get_status()
    
    state = status["state"].upper()
    
    st.markdown(f'<div style="background-color:#1e1e1e; padding:20px; border-left: 10px solid #00FF00; border-radius:10px;"><h2 style="margin:0;">Estado Moral: {state}</h2></div>', unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Autonomía", f"{status['capacity']['autonomy']}%")
    with col2:
        st.metric("Preempción", f"{status['capacity']['preemption']}%")

except Exception as e:
    st.error(f"Error de conexión con el núcleo: {e}")
