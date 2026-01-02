import streamlit as st

# 1. MÓDULO DE IDIOMA: Sincronización con la Sidebar
idioma = st.session_state.get('Language', st.session_state.get('language', 'English'))

# Diccionario de etiquetas para mantener la interfaz bilingüe
textos = {
    "English": {
        "titulo": "🔬 Advanced Analysis / Análisis Avanzado",
        "label": "Enter the ethical dilemma or interaction:",
        "placeholder": "Describe el escenario...",
        "btn_moralogy": "Ejecutar Moralogía",
        "btn_advanced": "Execute Moralogy Analysis",
        "scenarios": "Example Scenarios",
        "btn_tribunal": "Enviar al Tribunal"
    },
    "Español": {
        "titulo": "🔬 Advanced Analysis / Análisis Avanzado",
        "label": "Ingrese el dilema ético o interacción:",
        "placeholder": "Describe el escenario...",
        "btn_moralogy": "Ejecutar Moralogía",
        "btn_advanced": "Execute Moralogy Analysis",
        "scenarios": "Escenarios de Ejemplo",
        "btn_tribunal": "Enviar al Tribunal"
    }
}
T = textos.get(idioma, textos["English"])

st.title(T["titulo"])

# 2. ÁREA DE TEXTO (Variable: 'input_usuario')
# Se usa 'input_usuario' para evitar el NameError posterior
input_usuario = st.text_area(T["label"], placeholder=T["placeholder"], height=150)

# 3. TUS MÓDULOS DE ACCIÓN ORIGINALES
col1, col2 = st.columns([1, 1])
with col1:
    if st.button(T["btn_moralogy"]):
        st.info("Ejecutando Módulo de Evaluación...")

with col2:
    if st.button(T["btn_advanced"], type="primary"):
        st.write("Framework Analysis en curso...")

# 4. TUS ESCENARIOS DE CARGA (Trolley, Gilded, Last Agent)
st.markdown(f"### 💡 {T['scenarios']}")
ce1, ce2, ce3 = st.columns(3)

if ce1.button("Load: Trolley Problem"):
    st.info("Trolley Problem loaded.")

if ce2.button("Load: Gilded Script"):
    st.info("Gilded Script loaded.")

if ce3.button("Load: Last Agent"):
    st.info("Last Agent loaded.")

# 5. MÓDULO DE CONEXIÓN AL TRIBUNAL
st.divider()
if st.button(T["btn_tribunal"]):
    if input_usuario:
        # Guardamos en el estado global para que la página de debate lo lea
        st.session_state['caso_actual'] = input_usuario 
        st.success("✅ Caso enviado al Tribunal de Adversarios.")
    else:
        st.error("Error: Escriba un dilema primero.")
