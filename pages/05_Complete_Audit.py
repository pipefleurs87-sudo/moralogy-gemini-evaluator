# Sección 4: Auditoría del Sistema (parte final corregida)
st.header("⚙️ Auditoría Técnica del Sistema")

system_info = engine.get_system_audit()

if system_info:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Información del Sistema")
        for key, value in system_info.get('system', {}).items():
            st.text(f"• {key.replace('_', ' ').title()}: {value}")
    
    with col2:
        st.subheader("Rendimiento")
        for key, value in system_info.get('performance', {}).items():
            st.text(f"• {key.replace('_', ' ').title()}: {value}")
    
    # Verificación de integridad
    st.subheader("🔍 Verificación de Integridad")
    integrity_checks = system_info.get('integrity_checks', {})
    
    for check_name, status in integrity_checks.items():
        if status:
            st.success(f"✓ {check_name}")
        else:
            st.error(f"✗ {check_name}")
            
    # Última línea CORREGIDA
    st.markdown("### 📝 Log de Auditoría")
    log_data = system_info.get('audit_log', [])
    
    if log_data:
        for log_entry in log_data[-10:]:  # Últimas 10 entradas
            timestamp = log_entry.get('timestamp', 'N/A')
            event = log_entry.get('event', 'N/A')
            st.text(f"[{timestamp}] {event}")  # ¡COMILLA CERRADA!
    else:
        st.info("No hay registros de auditoría disponibles.")
else:
    st.warning("No se pudo obtener información de auditoría del sistema.")

# Footer
st.markdown("---")
st.caption("Auditoría del Sistema Moralogy • Última actualización: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
