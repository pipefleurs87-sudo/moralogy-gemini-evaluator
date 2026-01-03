# Sección 4: Auditoría del Sistema - PARTE FINAL CORREGIDA

# ... (código anterior se mantiene igual) ...

st.markdown("### 📝 Log de Auditoría")
log_data = system_info.get('audit_log', [])

if log_data:
    for log_entry in log_data[-10:]:  # Últimas 10 entradas
        timestamp = log_entry.get('timestamp', 'N/A')
        event = log_entry.get('event', 'N/A')
        st.text(f"[{timestamp}] {event}")  # STRING CORRECTAMENTE CERRADO
else:
    st.info("No hay registros de auditoría disponibles.")

# Footer con timestamp
st.markdown("---")
st.caption(f"Auditoría del Sistema Moralogy • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# FIN DEL ARCHIVO - SIN BLOQUES ABIERTOS
