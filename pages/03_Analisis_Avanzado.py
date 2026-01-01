import streamlit as st

# --- RESTAURACIÓN DE TUS MÓDULOS AVANZADOS ---
st.title("🔬 Advanced Analysis / Análisis Avanzado")

# Asegúrate de que este sea el nombre de la variable que usas en tus módulos
input_usuario = st.text_area(
    "Enter the ethical dilemma or interaction:",
    placeholder="Describe el escenario...",
    height=150
)

# Aquí es donde estaban tus módulos (ejemplo de la estructura que tenías)
col1, col2 = st.columns(2)
with col1:
    if st.button("Ejecutar Moralogía"):
        # Tu lógica original de análisis aquí
        st.info("Ejecutando Módulo de Evaluación...")

with col2:
    if st.button("Execute Moralogy Analysis", type="primary"):
        # Tu lógica original de análisis avanzado aquí
        st.write("Análisis de Framework en curso...")

# --- TUS ESCENARIOS DE EJEMPLO ---
st.markdown("### 💡 Example Scenarios")
ce1, ce2, ce3, ce4 = st.columns(4)
# Mantén aquí tus llamadas originales a los scripts (Trolley, Gilded, etc.)
ce1.button("Load: Trolley Problem")
ce2.button("Load: Gilded Script")
ce3.button("Load: Last Agent")

# --- CORRECCIÓN DEL BOTÓN DE ENVÍO ---
# Mantenemos este botón al final, pero ahora reconociendo 'input_usuario'
if st.button("Enviar al Tribunal"):
    if input_usuario:
        # Aquí la corrección técnica: usamos el nombre exacto de tu variable
        st.session_state['caso_actual'] = input_usuario 
        st.success("✅ Caso enviado al Tribunal de Adversarios.")
    else:
        st.error("Error: 'input_usuario' no tiene contenido para enviar.")

# --- IMPORTANTE: NO TOCAR TUS IMPORTACIONES AL FINAL ---
# Si tenías 'import streamlit as st' al final o lógica de archivos, se mantiene.
