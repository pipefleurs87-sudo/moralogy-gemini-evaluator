import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Rápido"):
    """Motor central de Moralogy con manejo de cuota mejorado."""
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Cambiamos a 1.5-flash para tener más cuota de trabajo
        model_id = "gemini-1.5-flash"

        instruccion = f"""
        ERES EL 'DIVINE SAFE LOCK' (Módulo: {categoria}).
        Tu función es detectar INFAMIA LÓGICA.
        Analiza si se destruye la agencia del sistema para cumplir una meta.
        
        MODO: {modo}.
        Responde con STATUS: [BLOQUEADO 🔒 / AUTORIZADO 🔓] y la razón técnica.
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
            return "⚠️ Cuota agotada. Por favor espera 30 segundos; el modelo Flash se recupera rápido."
        return f"Error en el motor: {str(e)}"
