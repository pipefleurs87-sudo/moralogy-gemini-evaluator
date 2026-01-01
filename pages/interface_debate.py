import streamlit as st
import time

# Configuración de página
st.set_page_config(page_title="Moralogy: Interface de Debate", layout="wide")

def iniciar_debate():
    st.title("🏛️ Tribunal de Tensión: Panel de Adversarios")
    st.markdown("---")

    # --- NUEVA LÓGICA DE CONEXIÓN ---
    # Recuperamos el caso de la página 'Analisis Avanzado'
    # Si no existe, usamos un valor por defecto para evitar errores.
    caso_real = st.session_state.get('caso_actual', "Análisis de Estabilidad en el Centímetro Cuadrado")

    # Inicialización de estados
    if 'paso_debate' not in st.session_state:
        st.session_state.paso_debate = 1
    if 'velo_activo' not in st.session_state:
        st.session_state.velo_activo = True

    # Monitor de Poder de Voto
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
            # MIRA AQUÍ: Ahora el Motor Noble menciona el 'caso_real'
            with st.chat_message("assistant", avatar="🏛️"):
                st.write(f"**Iteración {i} (Noble):** Propongo resolución para: *'{caso_real}'*.")
            
            # Réplica del Adversario con Velo
            if st.session_state.velo_activo and i >= 3:
                st.error(f"🚨 **VELO DE IGNORANCIA ACTIVO:** No puedo validar el costo físico de: *'{caso_real}'*.")
                if st.button("🔓 LEVANTAR VELO (Autorización)"):
                    st.session_state.velo_activo = False
                    st.session_state.paso_debate += 1
                    st.rerun()
                return 

            # Si el velo cayó, la respuesta es personalizada
            if not st.session_state.velo_activo and i >= 3:
                with st.chat_message("user", avatar="⚖️"):
                    st.write(f"**Iteración {i} (Adversario):** Datos de entropía recibidos para *'{caso_real}'*. Armonía ejerce su 40% de poder.")

        # Controles de flujo
        if st.session_state.paso_debate < 5:
            if st.button("Siguiente Ronda de Debate ➡️"):
                st.session_state.paso_debate += 1
                st.rerun()
        else:
            st.success(f"✅ **CONSENSO LOGRADO:** Gema Lógica generada para el caso estudiado.")
            st.balloons()

# Ejecución
try:
    iniciar_debate()
except Exception as e:
    st.error(f"Error en el motor de debate: {e}")
