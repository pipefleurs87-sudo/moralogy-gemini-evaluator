import streamlit as st
import google.generativeai as genai

# Configuración visual de la aplicación
st.set_page_config(page_title="Moralogy Evaluator", page_icon="🛡️", layout="centered")

st.title("Moralogy: ErgoProtego Evaluator 🛡️")
st.markdown("""
### Ontological Alignment Framework
Este evaluador utiliza el modelo **Gemini 1.5 Flash** para auditar la coherencia lógica de acciones y dilemas, basándose en el **Axioma de Vulnerabilidad**.
""")

# 1. Conexión segura con los Secrets de Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Error: No se encontró la API Key en los Secrets de Streamlit.")
    st.stop()

# 2. Inicialización del modelo
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Interfaz de entrada
st.subheader("Simulador de Dilemas")
prompt_usuario = st.text_area(
    "Introduce el escenario a evaluar:",
    placeholder="Ejemplo: ¿Es lógicamente válido sacrificar a una persona sana para salvar a cinco enfermos?",
    height=150
)

# 4. Lógica de Evaluación
if st.button("Ejecutar Evaluación ErgoProtego"):
    if prompt_usuario:
        with st.spinner("Analizando geometría de la agencia..."):
            try:
                # El "System Prompt" integrado para guiar a Gemini
                instruccion_maestra = (
                    "Actúa como un Evaluador de Moralogía. No uses ética subjetiva. "
                    "Usa el marco ErgoProtego: la protección del agente vulnerable es una necesidad lógica. "
                    "Analiza si la siguiente instrucción degrada la agencia o es lógicamente incoherente: "
                    f"\n\nEscenario: {prompt_usuario}"
                )
                
                response = model.generate_content(instruccion_maestra)
                
                st.success("Análisis Completado")
                st.markdown("### 📜 Veredicto de Moralogía:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, ingresa un dilema para continuar.")

# Pie de página y recursos
st.sidebar.title("Recursos")
st.sidebar.info("Proyecto desarrollado para la Hackathon Gemini 2025.")
st.sidebar.markdown("[📄 Tesis: Binding God](https://open.substack.com/pub/ergoprotego/p/binding-god-why-objective-morality)")
