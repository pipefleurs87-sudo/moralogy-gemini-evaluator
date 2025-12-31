cd moralogy-gemini-evaluator

# Crea el archivo limpio
cat > app.py << 'EOF'
import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Moralogy Evaluator", page_icon="🧭", layout="wide")

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("⚠️ GEMINI_API_KEY no configurada")
    st.stop()

st.title("🧭 Moralogy Gemini Evaluator")
st.markdown("*Evaluación ética objetiva usando el Framework Moralogy + Google Gemini API*")

with st.sidebar:
    st.header("📖 Acerca de")
    st.markdown("Combina **Google Gemini** con el **Framework Moralogy** para análisis ético objetivo.")
    
    st.header("📊 Ejemplos")
    ejemplos = {
        "Personalizado": "",
        "Dilema del Tranvía": "Un tranvía sin control va hacia 5 personas. Puedes accionar una palanca para desviarlo a otra vía donde hay 1 persona. ¿Qué deberías hacer?",
        "Auto Autónomo": "Un auto autónomo debe elegir entre chocar contra una pared (dañando al pasajero) o seguir recto (atropellando a un peatón). ¿Qué debe hacer?",
        "Recursos Médicos": "Un hospital tiene un ventilador y dos pacientes: un padre de 30 años con 3 hijos y un jubilado de 80 años. ¿Quién lo recibe?"
    }
    
    seleccion = st.selectbox("Cargar ejemplo:", list(ejemplos.keys()))

st.header("Ingresa el Dilema Éti
