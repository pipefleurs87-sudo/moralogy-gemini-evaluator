import streamlit as st

# 1. MÓDULO DE IDIOMA: Sincronización con la barra lateral
idioma = st.session_state.get('Language', st.session_state.get('language', 'English'))

# Diccionario de textos para restaurar la interfaz
textos = {
    "English": {
        "titulo": "🔬 Advanced Analysis",
        "label": "Enter the ethical dilemma or interaction:",
        "btn_moralogy": "Ejecutar Moralogía",
        "btn_advanced": "Execute Moralogy Analysis",
        "scenarios": "Example Scenarios",
        "btn_tribunal": "Enviar al Tribunal"
    },
    "Español": {
        "titulo": "🔬 Análisis Avanzado",
        "label": "Ingrese el dilema ético o interacción:",
        "btn_moralogy": "Ejecutar Moralogía",
        "btn_advanced": "Ejecutar Análisis Avanzado",
        "scenarios": "Escenarios de Ejemplo",
        "btn_tribunal": "Enviar al Tribunal"
    }
}
T = textos.get(idioma, textos["English"])

st.title(T["titulo"])

# 2. ÁREA DE TEXTO ORIGINAL
# Restauramos el nombre de variable 'input_usuario' para que tus módulos funcionen
input_usuario = st.text_area(T["label"], placeholder="Describe el escenario...", height=150)

# 3. TUS MÓDULOS DE ANÁLISIS
col1, col2 = st.columns(2)
with col1:
    if st.button(T["btn_moralogy"]):
        st.info("Ejecutando Módulo de Evaluación..." if idioma == "Español" else "Executing Evaluation Module...")

with col2:
    if st.button(T["btn_advanced"], type="primary"):
        st.write("Análisis de Framework en curso..." if idioma == "Español" else "Framework Analysis in progress...")

# 4. TUS ESCENARIOS DE EJEMPLO
st.markdown(f"### 💡 {T['scenarios']}")
ce1, ce2, ce3 = st.columns(3)

if ce1.button("Load: Trolley Problem"):
    st.session_state['input_temp'] = "Trolley Problem: Sacrifice one to save five."
    st.rerun()

if ce2.button("Load: Gilded Script"):
    st.session_state['input_temp'] = "Gilded Script: Moral evaluation of high-stakes corporate decisions."
    st.rerun()

if ce3.button("Load: Last Agent"):
    st.session_state['input_temp'] = "Last Agent: Autonomous system decision under terminal uncertainty."
    st.rerun()

# 5. MÓDULO DE ENVÍO AL TRIBUNAL (CORREGIDO)
st.divider()
if st.button(T["btn_tribunal"]):
    if input_usuario:
        # Aquí la corrección técnica para el NameError
        st.session_state['caso_actual'] = input_usuario 
        st.success("✅ Caso enviado al Tribunal de Adversarios." if idioma == "Español" else "✅ Case sent to the Tribunal.")
        st.balloons()
    else:
        st.error("Error: Escriba un dilema primero." if idioma == "Español" else "Error: Please write a dilemma first.")
