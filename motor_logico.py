import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Hackathon"):
    """
    Motor optimizado para la Hackatón usando Gemini 3 Flash Preview. 
    Implementa el Divine Safe Lock basado en el Framework Moralogy.
    """
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura la nueva API Key en los Secrets de Streamlit."

    try:
        # Inicialización con el nuevo SDK
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # MODELO RECOMENDADO PARA LA HACKATÓN
        model_id = "gemini-3-flash-preview" 

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
        
        # Generación de contenido con el modelo Gemini 3
        response = client.models.generate_content(
            model=model_id,
            config={
                'system_instruction': instruccion,
                'temperature': 0.1,  # Estabilidad para auditorías éticas
            },
            contents=prompt
        )
        
        return response.text

    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            return f"❌ Error 404: El modelo '{model_id}' no está disponible. Revisa los permisos de la Hackatón."
        return f"Error técnico: {error_msg}"
