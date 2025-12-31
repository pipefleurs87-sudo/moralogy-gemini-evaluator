import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Hackathon"):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura tu nueva API Key en Streamlit Secrets."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # MODELOS RECOMENDADOS PARA HACKATÓN:
        # 1. "gemini-1.5-flash" -> El más estable, mucha cuota.
        # 2. "gemini-3-flash-preview" -> El más nuevo (usa este si tienes acceso).
        model_id = "gemini-1.5-flash" 

        instruccion = f"""
        ERES EL DIVINE SAFE LOCK. 
        Misión: Auditar la consistencia ética del escenario.
        Framework: Moralogy Engine.
        """
        
        prompt = f"Agentes: {agentes}. Escenario: {situacion}. Contexto: {contexto}"
        
        response = client.models.generate_content(
            model=model_id,
            config={'system_instruction': instruccion},
            contents=prompt
        )
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "⚠️ CUOTA AGOTADA. Espera 10 segundos para que el sistema respire."
        return f"Error técnico: {str(e)}"
