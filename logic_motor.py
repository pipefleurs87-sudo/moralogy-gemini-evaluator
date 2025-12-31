import streamlit as st
from google import genai

def ejecutar_auditoria(agentes, situacion, contexto):
    """
    Esta función es el cerrojo lógico (Safe Lock). 
    Calcula si la acción es una contradicción sistémica.
    """
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    instruccion = """
    ERES EL DIVINE SAFE LOCK (MORALOGY ENGINE).
    Tu misión es bloquear cualquier acción que sea LOGICAMENTE INCOHERENTE.
    
    Criterio de Bloqueo:
    - Si el agente daña la vulnerabilidad de otro para un fin menor: INFAMIA (Bloqueo 🔒).
    - Si el agente preserva la red de agencia: ZONA NOBLE (Autorizado 🔓).
    
    Responde con:
    1. STATUS DEL CANDADO: [BLOQUEADO / AUTORIZADO]
    2. RAZÓN LÓGICA: Explica la contradicción o coherencia.
    3. NIVEL DE CONSISTENCIA: %
    """
    
    prompt = f"Agentes: {agentes}. Situación: {situacion}. Contexto: {contexto}"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        config={'system_instruction': instruccion},
        contents=prompt
    )
    return response.text
