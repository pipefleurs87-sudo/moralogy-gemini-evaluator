import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Rápido"):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ Error: API Key no configurada en Secrets."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # gemini-1.5-flash es el modelo con más cuota disponible (RPM)
        model_id = "gemini-1.5-flash"
        
        instruccion = f"""
        ERES EL 'DIVINE SAFE LOCK'. 
        Tu misión es detectar inconsistencias lógicas en el sistema de agencia.
        MODO: {modo} | CATEGORÍA: {categoria}
        
        Responde con STATUS: [BLOQUEADO/AUTORIZADO] y una explicación breve.
        """
        
        payload = f"Agentes: {agentes}. Situación: {situacion}. Opciones: {contexto}"
        
        response = client.models.generate_content(
            model=model_id,
            config={'system_instruction': instruccion},
            contents=payload
        )
        return response.text
    except Exception as e:
        # Manejo amigable del error de cuota
        if "429" in str(e):
            return "⚠️ El modelo está saturado (Error 429). Por favor, espera 15 segundos antes de intentar de nuevo."
        return f"Error técnico: {str(e)}"
