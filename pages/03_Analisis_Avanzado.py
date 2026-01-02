import streamlit as st

# 1. MÓDULO DE IDIOMA: Sincronización con la Sidebar
# Recupera la selección de idioma de la barra lateral
idioma = st.session_state.get('Language', st.session_state.get('language', 'English'))

# Título dinámico según idioma
titulo = "Advanced Analysis / Análisis Avanzado"
st.title(f"🔬 {titulo}")

# 2. ÁREA DE ENTRADA (Variable original: 'input_usuario')
input_usuario = st.text_area(
    "Enter the ethical dilemma or interaction:" if idioma == "English" else "Ingrese el dilema ético o interacción:",
    placeholder="Describe el escenario..." if idioma == "English" else "Describe el escenario...",
    height=150
)

# 3. TUS MÓDULOS DE ACCIÓN ORIGINALES
col1, col2 = st.columns([1, 1])
with col1:
    # Botón blanco original
    if st.button("Ejecutar Moralogía"):
        st.info("Ejecutando Módulo de Evaluación...")

with col2:
    # Botón rojo original
    if st.button("Execute Moralogy Analysis", type="primary"):
        st.write("Framework Analysis en curso...")

# 4. TUS ESCENARIOS DE CARGA (Trolley, Gilded, Last Agent)
st.markdown("### 💡 Example Scenarios" if idioma == "English" else "### 💡 Escenarios de Ejemplo")
ce1, ce2, ce3 = st.columns(3)

with ce1:
    if st.button("Load: Trolley Problem"):
        st.info("Trolley Problem loaded.")

with ce2:
    if st.button("Load: Gilded Script"):
        st.info("Gilded Script loaded.")

with ce3:
    if st.button("Load: Last Agent"):
        st.info("Last Agent loaded.")

# 5. MÓDULO DE ENVÍO AL TRIBUNAL (CORREGIDO SIN NAMEERROR)
st.divider()
if st.button("Enviar al Tribunal"):
    if input_usuario:
        # Aquí se guarda correctamente en el estado global
        st.session_state['caso_actual'] = input_usuario 
        st.success("✅ Caso enviado al Tribunal de Adversarios.")
    else:
        st.error("Error: Escriba un dilema primero.")
