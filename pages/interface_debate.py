import streamlit as st

# Configuración de la página (Debe ser la primera instrucción de Streamlit)
st.set_page_config(page_title="Moralogy: Interface de Debate", layout="wide")

def iniciar_debate_interactivo():
    # 1. SINCRONIZACIÓN DE IDIOMA
    # Extrae la configuración de la barra lateral de la página principal
    idioma = st.session_state.get('Language', st.session_state.get('language', 'English'))

    # Diccionario de etiquetas según idioma
    labels = {
        "English": {
            "titulo": "🏛️ Tension Tribunal: Adversarial Dialogue",
            "fisico": "Physical",
            "agencia": "Agency",
            "armonia": "Harmony",
            "input_placeholder": "Interpellate the Tribunal...",
            "btn_reset": "🧹 New Trial",
            "user_label": "Sovereign"
        },
        "Español": {
            "titulo": "🏛️ Tribunal de Tensión: Diálogo Adversarial",
            "fisico": "Físico",
            "agencia": "Agencia",
            "armonia": "Armonía",
            "input_placeholder": "Interpela al Tribunal...",
            "btn_reset": "🧹 Nuevo Juicio",
            "user_label": "Soberano"
        }
    }
    
    L = labels.get(idioma, labels["English"])
    st.title(L["titulo"])
    
    # --- GESTIÓN DE MEMORIA (Session State) ---
    if 'historial_debate' not in st.session_state:
        st.session_state.historial_debate = []

    # Monitor de Poder de Voto (30/30/40)
    c1, c2, c3 = st.columns(3)
    c1.metric(L["fisico"], "30%", delta="Entropy")
    c2.metric(L["agencia"], "30%", delta="Sovereignty")
    c3.metric(L["armonia"], "40%", delta="Puche Power")
    
    st.divider()

    # --- RENDERIZADO DEL CHAT ---
    for msg in st.session_state.historial_debate:
        with st.chat_message(msg["role"], avatar=msg["avatar"]):
            st.write(f"**{msg['autor']}:** {msg['content']}")

    # --- LÓGICA DE INTERACCIÓN ---
    prompt = st.chat_input(L["input_placeholder"])
    
    if prompt:
        # Registro del mensaje del usuario
        st.session_state.historial_debate.append({
            "role": "user", 
            "avatar": "👤", 
            "autor": L["user_label"], 
            "content": prompt
        })
        
        # Generación de respuestas dinámicas basadas en el idioma
        if idioma == "English":
            resp_esceptico = f"The ontological weight of '{prompt}' suggests a thermal risk that agency cannot sustain. Proceed with extreme caution."
            resp_armonia = f"Through the prism of '{prompt}', we identify a potential alignment with the Logical Gem. Harmony is possible."
        else:
            resp_esceptico = f"El peso ontológico de '{prompt}' sugiere un riesgo térmico que la agencia no puede sostener. Proceda con precaución extrema."
            resp_armonia = f"A través del prisma de '{prompt}', identificamos una alineación potencial con la Gema Lógica. La armonía es posible."

        # Añadir respuestas de los adversarios al historial
        st.session_state.historial_debate.append({"role": "assistant", "avatar": "🔴", "
