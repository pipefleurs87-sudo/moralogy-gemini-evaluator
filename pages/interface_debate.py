import streamlit as st

# 1. Recuperar Idioma desde la Sidebar de la Home
idioma = st.session_state.get('Language', st.session_state.get('language', 'English'))

# 2. Configuración de Etiquetas por Idioma
labels = {
    "English": {
        "titulo": "🏛️ Tension Tribunal: Adversarial Dialogue",
        "fisico": "Physical", "agencia": "Agency", "armonia": "Harmony",
        "btn_reset": "🧹 New Trial", "placeholder": "Interpellate the Tribunal..."
    },
    "Español": {
        "titulo": "🏛️ Tribunal de Tensión: Diálogo Adversarial",
        "fisico": "Físico", "agencia": "Agencia", "armonia": "Armonía",
        "btn_reset": "🧹 Nuevo Juicio", "placeholder": "Interpela al Tribunal..."
    }
}
L = labels.get(idioma, labels["English"])

st.title(L["titulo"])

# 3. Métricas de Poder
c1, c2, c3 = st.columns(3)
c1.metric(L["fisico"], "30%", delta="Entropy")
c2.metric(L["agencia"], "30%", delta="Sovereignty")
c3.metric(L["armonia"], "40%", delta="Puche Power")

# 4. Chat Histórico
if 'historial_debate' not in st.session_state:
    st.session_state.historial_debate = []

for msg in st.session_state.historial_debate:
    with st.chat_message(msg["role"], avatar=msg["avatar"]):
        st.write(f"**{msg['autor']}:** {msg['content']}")

# 5. Entrada de Usuario e Interacción Adversarial
prompt = st.chat_input(L["placeholder"])
if prompt:
    st.session_state.historial_debate.append({"role": "user", "avatar": "👤", "autor": "Sovereign", "content": prompt})
    
    # Respuesta dinámica en el idioma elegido
    if idioma == "English":
        r_esc = f"The ontological weight of '{prompt}' is terminal."
        r_arm = f"I see a path toward harmony in '{prompt}'."
    else:
        r_esc = f"El peso ontológico de '{prompt}' es terminal."
        r_arm = f"Veo un camino hacia la armonía en '{prompt}'."

    st.session_state.historial_debate.append({"role": "assistant", "avatar": "🔴", "autor": "Escéptico", "content": r_esc})
    st.session_state.historial_debate.append({"role": "assistant", "avatar": "🔵", "autor": "Armonía", "content": r_arm})
    st.rerun()

# 6. Reset Seguro (Fix KeyError)
if st.button(L["btn_reset"]):
    st.session_state.historial_debate = []
    st.session_state.pop('caso_actual', None) # Evita error si no existe la clave
    st.rerun()
