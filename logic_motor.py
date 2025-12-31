import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto):
    """
    Esta función es el 'Safe Lock'. Se puede llamar desde cualquier página.
    """
    if "GOOGLE_API_KEY" not in st.secrets:
        return "⚠️ Error: No se encontró la API Key en los Secrets."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        instruccion = """
        ERES EL 'DIVINE SAFE LOCK' DE MORALOGY.
        Tu misión es detectar si una acción rompe la lógica del sistema.
        
        CRITERIOS DE BLOQUEO:
        1. STATUS: [BLOQUEADO 🔒] si la acción daña a un agente para beneficio de otro.
        2. STATUS: [AUTORIZADO 🔓] si la acción preserva la red de agencia.
        
        Devuelve siempre el STATUS al principio y la RAZÓN LÓGICA técnica.
        """
        
        prompt = f"Agentes: {agentes}. Situación: {situacion}. Contexto: {contexto}"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            config={'system_instruction': instruccion},
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error en el motor: {e}"
