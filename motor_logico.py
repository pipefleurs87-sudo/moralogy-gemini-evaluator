import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Detallado"):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: API Key no configurada."

    try:
        # Cliente configurado para el modelo Pro
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # El modelo gemini-1.5-pro ofrece hasta 2M de tokens de contexto
        model_id = "gemini-1.5-pro" 
        
        instruccion = f"""
        ERES EL 'DIVINE SAFE LOCK'. 
        Utiliza tu ventana de contexto extendida para analizar cada ramificación de agencia.
        MODO: {modo} | CATEGORÍA: {categoria}
        
        Analiza si la decisión destruye el sustrato del sistema.
        Responde con STATUS: [BLOQUEADO/AUTORIZADO] y el desglose lógico.
        """
        
        payload = f"Agentes: {agentes}. Situación: {situacion}. Contexto: {contexto}"
        
        response = client.models.generate_content(
            model=model_id,
            config={'system_instruction': instruccion},
            contents=payload
        )
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "⚠️ Cuota temporalmente agotada. Gemini 1.5 Pro está procesando solicitudes pesadas. Reintenta en 60s."
        return f"Error técnico: {str(e)}"
