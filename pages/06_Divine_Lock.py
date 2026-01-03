# Buscar y eliminar: unsafe_allow_safe_html=True

# En st.metric() - Líneas ~24-34:
with col1:
    st.metric("Estado del Motor", 
              "🟢 Activo" if engine.is_ready() else "🔴 Inactivo",
              delta=None)  # ELIMINADO: unsafe_allow_safe_html=True

with col2:
    st.metric("Dilemas Cargados", 
              engine.total_dilemmas,
              delta=None)  # ELIMINADO: unsafe_allow_safe_html=True

with col3:
    st.metric("Versión del Sistema", 
              engine.get_version(),
              delta=None)  # ELIMINADO: unsafe_allow_safe_html=True

# En st.text_area() - Línea ~136:
st.text_area("Logs Recientes", 
            "\n".join(logs), 
            height=300,
            disabled=True)  # ELIMINADO: unsafe_allow_safe_html=True
