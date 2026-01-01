import streamlit as st
import time

st.set_page_config(page_title="Tribunal Interactivo", layout="wide")

def iniciar_debate_interactivo():
    st.title("🏛️ Tribunal de Tensión: Diálogo Adversarial")
    
    # --- MEMORIA DEL CHAT ---
    if 'historial_debate' not in st.session_state:
        st.session_state.historial_debate = []
    if 'paso_debate' not in st.session_state:
        st.session_state.paso_debate = 1

    # Monitor de Poder
    c1, c2, c3 = st.columns(3)
    c1.metric("Físico", "30%")
    c2.metric("Agencia", "30%")
    c3.metric("Armonía", "40%")

    st.divider()

    # --- MOSTRAR HISTORIAL ---
    for msg in st.session_state.historial_debate:
        with st.chat_message(msg["role"], avatar=msg["avatar"]):
            st.write(f"**{msg['autor']}:** {msg['content']}")

    # --- INPUT DEL USUARIO (Interactividad) ---
    prompt = st.chat_input("Interpela al Tribunal (ej: ¿Por qué la entropía es tan alta?)...")
    
    if prompt:
        # 1. Tu mensaje
        st.session_state.historial_debate.append({"role": "user", "avatar": "👤", "autor": "Soberano", "content": prompt})
        
        # 2. Respuesta Triple (Simulada o vía API)
        # Aquí el "Escéptico" siempre será duro, el "Defensor" cauteloso y la "Armonía" conciliadora.
        respuestas = [
            {"role": "assistant", "avatar": "🔴", "autor": "Escéptico", "content": f"Tu pregunta '{prompt}' ignora el colapso térmico inminente."},
            {"role": "assistant", "avatar": "🔵", "autor": "Armonía", "content": f"Veo en '{prompt}' un camino hacia la Gema Lógica."}
        ]
        st.session_state.historial_debate.extend(respuestas)
        st.rerun()

    # Botón de reinicio seguro (corrigiendo el error anterior)
    if st.button("🧹 Nuevo Juicio"):
        st.session_state.historial_debate = []
        st.session_state.pop('caso_actual', None)
        st.rerun()

iniciar_debate_interactivo()
