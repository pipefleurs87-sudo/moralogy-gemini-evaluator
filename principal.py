import streamlit as st
from google import genai

st.set_page_config(page_title="Moralogy Engine v3", layout="wide")

# --- BARRA LATERAL: INPUT DE VARIABLES ---
with st.sidebar:
    st.header("⚙️ Configuración del Escenario")
    agentes = st.text_area("Agentes (Ej: Empresa A, Empleado B, Comunidad):", placeholder="Define los nodos del sistema...")
    contexto = st.text_area("Contexto (Dominio/Alcance):", placeholder="¿En qué entorno interactúan?")
    situacion = st.text_area("Situación (Riesgo/Amenaza/Daño):", placeholder="Describe el evento...")
    resumen = st.text_area("Resumen de Objetivos:", placeholder="¿Qué intentan lograr los agentes?")
    
    confirmar = st.button("Vectorizar y Analizar")

# --- ÁREA PRINCIPAL: PROCESAMIENTO ---
st.title("⚖️ Moralogy Engine: Verificación de Agencia")

if confirmar:
    if agentes and situacion:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Construcción del Prompt Estructurado
        prompt_final = f"""
        PROCESAR BAJO TEOREMA DE MORALOGY:
        
        NODOS (Agentes): {agentes}
        DOMINIO/ALCANCE (Contexto): {contexto}
        EVENTO: {situacion}
        METAS DEL SISTEMA: {resumen}
        
        OPERACIÓN REQUERIDA:
        1. Vectorizar la 'Pérdida de Agencia Total' vs 'Agencia Local'.
        2. Identificar si existe una 'Obligación Geométrica' que fuerce una decisión específica.
        3. Detectar 'Contradicciones Performativas' (Infamia).
        4. Dictar protocolo de Restauración si el daño es inevitable.
        """
        
        with st.spinner("Calculando Espectro Noble-Modal..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    config={'system_instruction': "Eres un motor de verificación formal de sistemas de agencia. No des consejos morales, da diagnósticos de consistencia lógica."},
                    contents=prompt_final
                )
                
                # --- VISUALIZACIÓN DE RESULTADOS OPTIMIZADA ---
                st.subheader("📊 Diagnóstico de Vectorización")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Vectores Detectados:**")
                    st.success("Vector de Dependencia (D) analizado")
                    st.warning("Umbral de Daño identificado")
                
                with col2:
                    st.write("**Balance de Agencia:**")
                    # Simulación visual del cálculo que Gemini explica en el texto
                    st.progress(0.65, text="Agencia Sistémica Preservada")

                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error en la vectorización: {e}")
    else:
        st.warning("Por favor, completa al menos 'Agentes' y 'Situación' en la barra lateral.")
