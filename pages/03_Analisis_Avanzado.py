import streamlit as st

# 1. Configuración de Títulos
st.title("🔬 Advanced Analysis / Análisis Avanzado")

# 2. Área de entrada de datos (Aseguramos el nombre de la variable)
# Esta es la variable que el botón de abajo debe leer
dilema_input = st.text_area(
    "Enter the ethical dilemma or interaction:",
    placeholder="Escriba aquí el caso para analizar...",
    height=200
)

# 3. Botón de Ejecución Local
if st.button("Execute Moralogy Analysis", type="primary"):
    if dilema_input:
        st.info("Analizando el impacto ontológico...")
        # Simulación de análisis para la demo
        st.success("Análisis completado. Puede proceder al Tribunal.")
    else:
        st.warning("Por favor, ingrese un dilema antes de ejecutar.")

# 4. Sección de Escenarios de Ejemplo (Botones rápidos)
st.markdown("### Example Scenarios")
col1, col2, col3 = st.columns(3)
if col1.button("Load: Trolley Problem"):
    st.info("Cargado: Dilema del Tranvía. Presione 'Enviar al Tribunal'.")
    # Nota: Para que se llene el área de texto automáticamente requeriría session_state, 
    # por ahora esto sirve para la guía visual.

# 5. BOTÓN DE ENVÍO AL TRIBUNAL (EL QUE TENÍA EL ERROR)
st.divider()
if st.button("Enviar al Tribunal"):
    if dilema_input:
        # CORRECCIÓN DEFINITIVA: 
        # Usamos 'dilema_input' porque es la variable que definimos arriba.
        st.session_state['caso_actual'] = dilema_input 
        st.success("✅ Caso enviado exitosamente al Tribunal de Adversarios.")
        st.balloons()
    else:
        st.error("Error: No hay datos para enviar. Escriba algo en el cuadro superior.")
