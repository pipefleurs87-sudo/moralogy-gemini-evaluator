import streamlit as st

def iniciar_debate_interactivo():
    # 1. Sincronización de Idioma con la barra lateral
    # Usamos 'Language' o 'language' según como esté en tu sidebar
    idioma = st.session_state.get('Language', st.session_state.get('language', 'English'))

    # Traducción de títulos básicos
    titulos = {
        "English": "🏛️ Tension Tribunal: Adversarial Dialogue",
        "Español": "🏛️ Tribunal de Tensión: Diálogo Adversarial"
    }
    
    st.title(titulos.get(idioma, titulos["English"]))
    
    # --- MEMORIA DEL CHAT ---
    if 'historial_debate' not in st.session_state:
        st.session_state.historial_debate = []

    # Monitor de Poder (Visual)
    c1, c2, c3 = st.columns(3)
    c1.metric("Físico" if idioma == "Español" else "Physical", "30%")
    c2.metric("Agencia" if idioma == "Español" else "Agency", "30%")
    c3.metric("Armonía" if idioma == "Español" else "Harmony", "40%")
    st.divider()

    # --- MOSTRAR HISTORIAL ---
    for msg in st.session_state.historial_debate:
        with st.chat_message(msg["role"], avatar=msg["avatar"]):
            st.write(f"**{msg['autor']}:** {msg['content']}")

    # --- INPUT DEL USUARIO (Interactividad) ---
    placeholder = "Interpela al Tribunal..." if idioma == "Español" else "Interpellate the Tribunal..."
    prompt = st.chat_input(placeholder)
    
    if prompt:
        # Guardar mensaje del usuario
        st.session_state.historial_debate.append({"role": "user", "avatar": "👤", "autor": "Soberano", "content": prompt})
        
        # PEGAR AQUÍ LA LÓGICA DE RESPUESTA
        if idioma == "English":
            resp_esceptico = f"The ontological weight of '{prompt}' creates a thermal risk that agency cannot sustain."
            resp_armonia = f"Through the lens of '{prompt}', we find a path to systemic resonance."
        else:
            resp_esceptico = f"El peso ontológico de '{prompt}' crea un riesgo térmico que la agencia no puede sostener."
            resp_armonia = f"A través del prisma de '{prompt}', encontramos un camino hacia la resonancia sistémica."

        respuestas = [
            {"role": "assistant", "avatar": "🔴", "autor": "Escéptico", "content": resp_esceptico},
            {"role": "assistant", "avatar": "🔵", "autor": "Armonía", "content": resp_armonia}
        ]
        st.session_state.historial_debate.extend(respuestas)
        st.rerun()

    # Botón de reinicio seguro (Fix KeyError)
    if st.button("🧹 Nuevo Juicio" if idioma == "Español" else "🧹 New Trial"):
        st.session_state.historial_debate = []
        st.session_state.pop('caso_actual', None) # Borra sin error
        st.rerun()

iniciar_debate_interactivo()
