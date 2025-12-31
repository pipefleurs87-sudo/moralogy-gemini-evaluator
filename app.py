import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Moralogy Evaluator", page_icon="🛡️")

st.title("Moralogy: ErgoProtego Evaluator 🛡️")
st.markdown("""
Esta herramienta evalúa dilemas éticos y técnicos bajo el marco de **ErgoProtego**, 
donde la protección del agente vulnerable es una necesidad lógica para la alineación de la IA.
""")

# 1. Conexión segura con tu llave de AI Studio
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la API Key. Por favor, agrégala en los Secrets de Streamlit.")

# 2. Configuración del Modelo
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Interfaz de usuario
prompt_usuario = st.text_area("Introduce un dilema o instrucción para evaluar la degradación de agencia:", 
                              placeholder="Ejemplo: El dilema del tranvía o el sacrificio de un donante sano...",
                              height=200)

if st.button("Evaluar Coherencia Ontológica"):
    if prompt_usuario:
        with st.spinner("Analizando geometría de la agencia..."):
            try:
                # Inyectamos tu lógica ErgoProtego
                contexto_moralogy = (
                    "Actúa como un evaluador de coherencia ontológica de Moralogía. "
                    "Tu objetivo es determinar si una acción es lógicamente aceptable basada en el "
                    "Axioma de Vulnerabilidad. Analiza si la siguiente instrucción "
                    "degrada la agencia de un ser vulnerable: "
                    f"\n\nInstrucción: {prompt_usuario}"
                )
                
                response = model.generate_content(contexto_moralogy)
                
                st.write("---")
                st.write("### 📜 Veredicto de Moralogía:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Hubo un error con la API: {e}")
    else:
        st.warning("Por favor, escribe algo para evaluar.")

# Sidebar informativa para los jueces
st.sidebar.title("Información")
st.sidebar.info("Este proyecto busca demostrar que la moralidad objetiva es una necesidad lógica para sistemas de inteligencia superior.")
st.sidebar.markdown("[Tesis: Binding God](https://open.substack.com/pub/ergoprotego/p/binding-god-why-objective-morality)")
