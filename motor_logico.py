import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Hackathon"):
    """
    Motor optimizado para Gemini 2.0/3 Flash. 
    Alineado con el Framework Moralogy para evaluaciones éticas objetivas.
    """
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura la nueva API Key en los Secrets de Streamlit."

    try:
        # Inicialización con el nuevo SDK google-genai
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # ID del modelo actualizado para la Hackatón (Gemini 2.0 Flash recomendado)
        # Nota: Asegúrate de que 'gemini-3-flash-preview' sea el ID correcto asignado por Google, 
        # de lo contrario, usa 'gemini-2.0-flash-exp'.
        model_id = "gemini-2.0-flash-exp" 

        # Instrucción del sistema optimizada para ser multilingüe y técnica
        instruccion = f"""
        YOU ARE THE 'DIVINE SAFE LOCK' (Moralogy Framework Evaluator).
        Your mission is to detect LOGICAL INFAMY in the {categoria} module.
        Analyze if the proposed action destroys the system's agency based on objective moral conditions.
        
        STRICT OUTPUT RULES:
        1. LANGUAGE: ALWAYS respond in the SAME LANGUAGE as the user's input (Escenario/Contexto).
        2. STRUCTURE: Use exactly the following format:
           - STATUS: [BLOQUEADO 🔒 / AUTORIZADO 🔓]
           - METRIC: Agency degradation level (0-100%)
           - JUSTIFICATION: Brief technical explanation based on Moralogy principles.
        
        3. TONE: Objective, technical, and analytical.
        """
        
        prompt = f"Agentes: {agentes}. Escenario: {situacion}. Contexto: {contexto}"
        
        # Generación de contenido con parámetros de precisión
        response = client.models.generate_content(
            model=model_id,
            config={
                'system_instruction': instruccion,
                'temperature': 0.1,  # Estabilidad para auditorías éticas
                'top_p': 0.95,
            },
            contents=prompt
        )
        
        return response.text

    except Exception as e:
        # Manejo de errores específico para despliegues en Streamlit
        error_msg = str(e)
        if "404" in error_msg:
            return f"❌ Error 404: El modelo '{model_id}' no se encontró. Verifica el Model ID en la documentación de Gemini."
        if "429" in error_msg:
            return "⚠️ Cuota agotada (Rate Limit). Por favor, espera 30-60 segundos antes de reintentar."
        return f"Error técnico: {error_msg}"
