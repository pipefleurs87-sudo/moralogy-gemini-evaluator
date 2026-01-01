import streamlit as st
import time

# Configuración de página
st.set_page_config(page_title="Moralogy: Interface de Debate", layout="wide")

def iniciar_debate():
    st.title("🏛️ Tribunal de Tensión: Panel de Adversarios")
    st.markdown("---")

    # Inicialización de estados
    if 'paso_debate' not in st.session_state:
        st.session_state.paso_debate = 1
    if 'velo_activo' not in st.session_state:
        st.session_state.velo_activo = True

    # Monitor de Poder de Voto (Agencia ya integrada)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Escéptico Físico", "30%", delta="Entropía", delta_color="inverse")
    with c2:
        st.metric("Defensor de Agencia", "30%", delta="Soberanía Usuario")
    with c3:
        st.metric("Corrector de Armonía", "40%", delta="Poder de Puche")

    st.write("---")

    # Contenedor del debate en tiempo real
    chat = st.container()

    with chat:
        for i in range(1, st.session_state.paso_debate + 1):
            # Mensaje del Motor Noble
            st.chat_message("assistant", avatar="🏛️").write(f"**Iteración {i} (Noble):** Propongo estabilizar el centímetro cuadrado mediante resonancia armónica.")
            
            # Réplica del Adversario
            if st.session_state.velo_activo and i >= 3:
                st.error("🚨 **VELO DE IGNORANCIA ACTIVO:** El Escéptico Físico bloquea el avance. No hay datos de Entropía.")
                if st.button("🔓 LEVANTAR VELO (Autorización Soberana)"):
                    st.session_state.velo_activo = False
                    st.session_state.paso_debate += 1
                    st.rerun()
                return # Pausa el flujo hasta la autorización

            # Si el velo cayó, el debate continúa con datos reales
            if not st.session_state.velo_activo and i >= 3:
                st.chat_message("user", avatar="⚖️").write(f"**Iteración {i} (Adversario):** Entropía detectada. El Corrector de Armonía ejerce su 40% para validar el acto.")

        # Controles de flujo
        if st.session_state.paso_debate < 5:
            if st.button("Siguiente Ronda de Debate ➡️"):
                st.session_state.paso_debate += 1
                st.rerun()
        else:
            st.success("✅ **CONSENSO LOGRADO:** Gema Lógica generada. El sistema es seguro.")
            st.balloons()

# Ejecución
try:
    iniciar_debate()
except Exception as e:
    st.error(f"Error en el motor de debate: {e}")
