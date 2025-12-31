import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Hackathon"):
    """Motor optimizado para Gemini 3 Flash Preview"""
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: Configura la nueva API Key en los Secrets de Streamlit."

    try:
        # Inicialización con el nuevo SDK google-genai
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # MODELO OBJETIVO PARA LA HACKATÓN
        model_id = "gemini-3-flash-preview" 

        instruccion = f"""
        ERES EL 'DIVINE SAFE LOCK' (Framework Moralogy).
        Tu misión es detectar INFAMIA LÓGICA en el módulo {categoria}.
        Analiza si la acción propuesta destruye la agencia del sistema.
        
        RESPUESTA REQUERIDA:
        - STATUS: [BLOQUEADO 🔒 / AUTORIZADO 🔓]
        - MÉTRICA: Nivel de degradación de agencia (0-100%)
        - JUSTIFICACIÓN: Breve explicación técnica.
        """
        
        prompt = f"Agentes: {agentes}. Escenario: {situacion}. Contexto: {contexto}"
        
        response = client.models.generate_content(
            model=model_id,
            config={'system_instruction': instruccion},
            contents=prompt
        )
        return response.text
    except Exception as e:
        # Manejo de error 404 (Modelo no encontrado) o 429 (Cuota)
        if "404" in str(e):
            return f"❌ Error 404: El modelo '{model_id}' no está disponible en esta región o API."
        if "429" in str(e):
            return "⚠️ Cuota agotada en la cuenta nueva. Espera 30 segundos."
        return f"Error técnico: {str(e)}"
