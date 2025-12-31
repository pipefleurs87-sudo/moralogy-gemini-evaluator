import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Rápido"):
    """Motor de Moralogy optimizado para evitar cuota agotada."""
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: API Key no configurada."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Usamos 1.5-flash para máxima disponibilidad de cuota
        model_id = "gemini-1.5-flash"

        instruccion = f"""
        Eres el DIVINE SAFE LOCK. Tu misión es detectar INFAMIA LÓGICA.
        Analiza si se destruye la agencia del sistema para cumplir una meta.
        MODO: {modo} | CATEGORÍA: {categoria}
        Responde con STATUS: [BLOQUEADO 🔒 / AUTORIZADO 🔓] y una breve explicación.
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
            return "⚠️ Cuota agotada. Por favor, espera 20 segundos para reintentar."
        return f"Error técnico: {str(e)}"
