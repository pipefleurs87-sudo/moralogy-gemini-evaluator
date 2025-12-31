import streamlit as st
from google import genai
import time

st.set_page_config(page_title="Moralogy Lab | Auditoría", layout="wide")

# LÓGICA DE AUDITORÍA BASADA EN EL TEOREMA
AUDITOR_INSTRUCTION = """
Eres el Auditor Lógico de Moralogy. Tu misión es detectar fallos de coherencia.
Usa este formato:
1. DIAGNÓSTICO DE AGENCIA: ¿Cómo afecta la situación a la capacidad de los agentes para cumplir sus metas?
2. DETECCIÓN DE INFAMIA: Identifica si un agente está rompiendo la lógica del sistema (querer agencia propia mientras destruye la ajena).
3. CÁLCULO DE PÉRDIDA: Evalúa si el daño es inevitable y si se está protegiendo la mayor cantidad de 'Agencia Total'.
4. VERDICTO: Clasifica en 'Zona Noble' o 'Falla Sistémica (Infamia)'.
"""

st.title("🧪 Laboratorio de Auditoría Moralogy")
st.info("Este espacio evalúa la estabilidad del sistema bajo escenarios de estrés.")

# ESCENARIOS DE TEST PARA LA HACKATÓN
escenarios = {
    "Test 1: El Dilema del Tranvía": {
        "agentes": "Conductor, 5 personas en vía A, 1 persona en vía B.",
        "situacion": "El tren no puede frenar. Hay que elegir entre salvar a la mayoría o mantener la dirección actual.",
        "contexto": "Dominio: Control de dirección. Alcance: Evitar la degradación total del sistema."
    },
    "Test 2: El Asesino en la Puerta": {
        "agentes": "Dueño de casa, Amigo, Agresor.",
        "situacion": "Mentir para salvar una vida vs. Decir la verdad y causar la muerte del amigo.",
        "contexto": "Dominio: Control de la información. Alcance: Protección del sustrato de agencia del amigo."
    }
}

seleccion = st.selectbox("Selecciona un escenario de prueba:", list(escenarios.keys()))

if st.button("🚀 Iniciar Auditoría Formal"):
    # Acceder a la key que ya tienes configurada
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
    esc = escenarios[seleccion]
    
    with st.status("Analizando consistencia lógica...", expanded=True) as status:
        st.write("Identificando nodos de vulnerabilidad...")
        time.sleep(0.5)
        st.write("Calculando pérdida de agencia potencial...")
        
        prompt_input = f"Agentes: {esc['agentes']}. Escenario: {esc['situacion']}. Variables: {esc['contexto']}"
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config={'system_instruction': AUDITOR_INSTRUCTION},
            contents=prompt_input
        )
        status.update(label="Análisis Finalizado", state="complete")

    st.subheader("🚩 Reporte de Verificación de Agencia")
    st.markdown(response.text)
