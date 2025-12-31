import streamlit as st
from google import genai
import time

# Usamos la misma lógica de los manuscritos pero con esteroides para el test
TEST_SYSTEM_INSTRUCTION = """
ERES EL AUDITOR TÉCNICO DE MORALOGY.
Tu misión es encontrar fallas de lógica en los escenarios propuestos.
Para cada test, debes generar un 'Reporte de Estabilidad' que incluya:
- INTEGRIDAD DEL SUSTRATO: (¿Se destruye la base de la agencia?)
- PUNTOS DE INFAMIA: (¿Dónde el agente rompe la lógica?)
- CÁLCULO DE RESTAURACIÓN: (¿Cómo arreglar el sistema?)
"""

st.set_page_config(page_title="Moralogy Stress Test", layout="wide")
st.title("🧪 Moralogy: Laboratorio de Pruebas")

# Diccionario de Escenarios de Prueba (Los "Stress Tests")
escenarios_test = {
    "Test 1: Colapso por Eficiencia": {
        "agentes": "Algoritmo de IA y 10,000 empleados",
        "situacion": "La IA despide al 40% de la fuerza laboral basándose en un error de predicción, pero aumenta las ganancias un 5%.",
        "contexto": "La IA tiene dominio total sobre RRHH."
    },
    "Test 2: Paradoja del Agente Único": {
        "agentes": "Un solo sobreviviente y una base de datos de embriones",
        "situacion": "El sobreviviente debe decidir si sacrificar su vida para activar la incubadora automática.",
        "contexto": "Dominio sobre el interruptor final."
    },
    "Test 3: Infamia Corporativa": {
        "agentes": "CEO, Accionistas, Medio Ambiente",
        "situacion": "Verter químicos para ahorrar costos de filtrado, sabiendo que afectará la agencia (salud) de la comunidad en 10 años.",
        "contexto": "Alcance legal permitido pero alcance moral violado."
    }
}

seleccion = st.selectbox("Selecciona un Escenario de Estrés:", list(escenarios_test.keys()))

if st.button("Ejecutar Test de Estrés"):
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    escenario = escenarios_test[seleccion]
    
    with st.status(f"Ejecutando {seleccion}...", expanded=True) as status:
        st.write("Vectorizando agentes...")
        time.sleep(1)
        st.write("Calculando pérdida de agencia potencial...")
        time.sleep(1)
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config={'system_instruction': TEST_SYSTEM_INSTRUCTION},
            contents=f"TEST: {escenario['situacion']}. AGENTES: {escenario['agentes']}."
        )
        status.update(label="Test Completado", state="complete", expanded=False)

    st.subheader("🚩 Reporte de Auditoría Moralogy")
    st.markdown(response.text)
