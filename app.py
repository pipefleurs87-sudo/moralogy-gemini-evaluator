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

st.header("Ingresa el Dilema Ético")

entrada_usuario = st.text_area(
    "Describe el dilema moral:",
    value=ejemplos[seleccion],
    height=150,
    placeholder="Ejemplo: Un auto autónomo debe elegir entre..."
)

if st.button("🔍 Analizar", type="primary"):
    if entrada_usuario:
        with st.spinner("Analizando..."):
            try:
                prompt = f"""Eres un filósofo moral usando el Framework Moralogy.

FRAMEWORK MORALOGY:
- Restricción Negativa: No causar daño innecesario
- Deber Positivo: Prevenir daño evitable dentro de tu capacidad
- El daño se mide mediante: lesión física, daño psicológico, violación de autonomía, privación de recursos

DILEMA: {entrada_usuario}

Proporciona un análisis estructurado:
1. **Resumen del Escenario**
2. **Partes Afectadas**
3. **Evaluación de Daños** (para cada opción)
4. **Evaluación Moralogy**
5. **Recomendación**
6. **Puntuación Moral** (0-100, donde 100 es más ético)

Usa encabezados claros y formato legible."""

                respuesta = model.generate_content(prompt)
                
                st.success("✅ Análisis Completo")
                st.markdown("---")
                st.markdown(respuesta.text)
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Modelo:** Gemini Pro")
                with col2:
                    st.info("**Framework:** Moralogy v1.0")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Por favor ingresa un dilema")

st.markdown("---")
st.markdown("<div style='text-align: center'><small>Construido para Google Gemini API Developer Competition 2024</small></div>", unsafe_allow_html=True)
```

4. Click en **"Commit new file"**

### Paso 3: Verifica que tu `requirements.txt` tenga:
```
streamlit
google-generativeai
python-dotenv
