import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto, categoria="General", modo="Rápido"):
    """
    Motor central de Moralogy. 
    Actúa como el cerrojo lógico (Safe Lock) para Super IA.
    """
    if "GOOGLE_API_KEY" not in st.secrets:
        return "⚠️ Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit."

    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Especialización por módulo
        especialidad = {
            "Financiera": "Auditoría de activos y riesgo sistémico.",
            "Ingeniería": "Seguridad física y fallos estructurales.",
            "Civil": "Derechos colectivos e infraestructura social.",
            "Social": "Equidad, comunidad y tejido humano."
        }.get(categoria, "Análisis de consistencia general.")

        instruccion = f"""
        ERES EL 'DIVINE SAFE LOCK' (Módulo: {categoria}).
        Tu función es detectar INFAMIA: cuando se destruye la agencia de un sujeto para un fin.
        
        MODO: {modo}. 
        Si es 'Detallado', analiza cada actor. Si es 'Rápido', ve al grano.
        
        FORMATO DE SALIDA:
        - STATUS: [BLOQUEADO 🔒 / AUTORIZADO 🔓]
        - NIVEL DE CONSISTENCIA: %
        - RAZÓN LÓGICA: Explicación técnica de la coherencia o contradicción.
        """
        
        prompt = f"Agentes: {agentes}. Escenario: {situacion}. Contexto: {contexto}"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            config={'system_instruction': instruccion},
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error en el motor: {str(e)}"
