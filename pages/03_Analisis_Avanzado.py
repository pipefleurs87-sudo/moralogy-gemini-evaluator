import streamlit as st

# Título de la sección
st.title("🔬 Advanced Analysis / Análisis Avanzado")

# 1. Definimos el área de texto
# Usamos un nombre claro para la variable: 'dilema_input'
dilema_input = st.text_area(
    "Enter the ethical dilemma or interaction:",
    placeholder="Ej: Two rival companies. one has the moraligy engine audit, the other doesn't...",
    height=200
)

# 2. Botón de Ejecución (Análisis de la página actual)
if st.button("Execute Moralogy Analysis", type="primary"):
    if dilema_input:
        st.info(f"Analizando: {dilema_input[:50]}...")
        # Aquí va tu lógica de motor de IA para esta página
    else:
        st.warning("Please enter a dilemma first.")

# 3. BOTÓN DE ENVÍO AL TRIBUNAL (EL QUE DABA ERROR)
st.markdown("---")
st.subheader("⚖️ Tribunal Integration")

if st.button("Enviar al Tribunal"):
    if dilema_input:
        # CORRECCIÓN DEL NAMEERROR:
        # Guardamos 'dilema_input' (la variable que definimos arriba) 
        # en el session_state para que la página 'interface_debate' la vea.
        st.session_state['caso_actual'] = dilema_input 
        st.success("✅ Case successfully transmitted to the Adversarial Tribunal.")
        st.balloons()
    else:
        st.error("Error: No data to send. Please write a dilemma in the box above.")

# --- SECCIÓN DE EJEMPLOS (Opcional, para tu demo) ---
st.divider()
st.caption("Example Scenarios")
c1, c2, c3 = st.columns(3)
if c1.button("Load: Trolley Problem"):
    st.info("Scenario loaded. Press 'Execute' or 'Enviar'.")
