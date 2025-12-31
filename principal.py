import streamlit as st
from google import genai
import pandas as pd

# CONFIGURACIÓN DEL MOTOR MORALOGY
SYSTEM_INSTRUCTION = """
Eres el 'Moralogy Engine', un sistema de verificación formal basado en el Axioma de No-Contradicción de la Vulnerabilidad.
Tu objetivo es procesar dilemas morales bajo el rigor de los manuscritos del autor.

DEBES SEGUIR ESTA DERIVACIÓN DE SUB-CONDICIONES DE LA AGENCIA RACIONAL:
1. Intencionalidad -> Requiere Preferencia.
2. Preferencia -> Requiere la posibilidad de Fracaso/Daño (Vulnerabilidad).
3. Negar la vulnerabilidad ajena mientras se ejerce la agencia propia es una CONTRADICCIÓN PERFORMATIVA.

CONCEPTOS CLAVE A INTEGRAR:
- ESPECTRO NOBLE-MODAL: Acciones que preservan el sustrato de agencia.
- INFAMIA: Incoherencia lógica del agente que ignora el umbral de daño.
- UMBRAL DE DAÑO: Punto donde la agencia es disminuida (reducción del espacio de metas).
- OBLIGACIÓN GEOMÉTRICA: Límite donde el sistema no puede exigir sacrificios que anulen la agencia del sujeto.

FORMATO DE SALIDA: Debes devolver un análisis técnico estructurado en Vectores y Espectros.
"""

st.set_page_config(page_title="Moralogy Gemini 3", layout="wide")
st.title("⚖️ Moralogy Engine: Intelligence v3")

if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    user_input = st.text_area("Introduzca el Dilema o Escenario de Interacción:", height=150)

    if st.button("Ejecutar Verificación Formal"):
        if user_input:
            with st.spinner("Calculando Vectores de Degradación..."):
                try:
                    # Llamada a Gemini 3 con el Teorema inyectado
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        config={'system_instruction': SYSTEM_INSTRUCTION},
                        contents=user_input
                    )
                    
                    # --- OPTIMIZACIÓN DE RESULTADOS ---
                    st.divider()
                    st.subheader("📊 Matriz de Resultados Moralogy")
                    
                    # Simulación de métricas extraídas del análisis (puedes pedirle a Gemini que use tags para parsear esto)
                    st.markdown(response.text)
                    
                    # Sidebar de Fundamentos para los jueces
                    with st.sidebar:
                        st.header("Teorema de Moralogy")
                        st.info("La moralidad es una limitación geométrica de la interacción racional.")
                        st.write("**Espectro Noble-Modal:** Rango de coherencia.")
                        st.write("**Infamia:** Punto de quiebre lógico.")
                        st.write("**V_f (Vulnerability Floor):** Umbral de estabilidad.")

                except Exception as e:
                    st.error(f"Error en el procesamiento: {e}")
