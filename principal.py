# principal.py - VERSIÓN FUNCIONAL MÍNIMA
import streamlit as st

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Moralogy Engine", layout="wide", page_icon="🏛️")

# 2. DEFINIR TEXTO PRIMERO
TEXTOS = {
    "English": {
        "title": "🏛️ Moralogy Engine",
        "subtitle": "Formal Vulnerability-Based Ethics System + Divine Lock",
        "box": "Describe the ethical dilemma:",
        "btn": "Analyze Through Framework",
        "placeholder": "Example: 'Is it ethical to sacrifice one person to save five?'"
    },
    "Español": {
        "title": "🏛️ Motor de Moralogía", 
        "subtitle": "Sistema Ético Formal Basado en Vulnerabilidad + Bloqueo Divino",
        "box": "Describe el dilema ético:",
        "btn": "Analizar con Framework",
        "placeholder": "Ejemplo: '¿Es ético sacrificar a una persona para salvar a cinco?'"
    }
}

# 3. INICIALIZAR session_state
if "idioma" not in st.session_state:
    st.session_state.idioma = "English"

# 4. SIDEBAR PRIMERO
with st.sidebar:
    st.markdown("### 🏛️ Moralogy Engine")
    
    # Selector de idioma
    st.session_state.idioma = st.selectbox(
        "Language / Idioma", 
        ["English", "Español"],
        key="lang_selector"
    )
    
    st.markdown("---")
    st.markdown("### About Moralogy")
    st.markdown("""
    **Framework Foundation:**
    - Agency requires vulnerability
    - Vulnerability grounds moral relevance
    - Harm = agency degradation
    - Actions justified by consent OR preventing greater harm
    """)

# 5. USAR EL IDIOMA CORRECTO
txt = TEXTOS[st.session_state.idioma]

# 6. INTERFAZ PRINCIPAL
st.title(txt["title"])
st.caption(txt["subtitle"])

# Input principal
caso = st.text_area(
    txt["box"],
    height=200,
    placeholder=txt["placeholder"],
    key="main_input"
)

# Botón de análisis
if st.button(txt["btn"], type="primary", key="analyze_btn"):
    if not caso:
        st.warning("⚠️ Please enter a scenario to analyze.")
    else:
        with st.spinner("🧠 Processing..."):
            st.success(f"✅ Received: {caso[:50]}...")
            st.info("(Aquí iría el análisis real)")

# 7. FOOTER
st.divider()
st.markdown("### Other Tools")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔬 Advanced Analysis", key="btn1"):
        st.write("Iría a análisis avanzado")

with col2:
    if st.button("🌟 Emergent Philosophy", key="btn2"):
        st.write("Iría a filosofía emergente")

with col3:
    if st.button("📊 Divine Lock Dashboard", key="btn3"):
        st.write("Iría a Divine Lock")

st.divider()
st.caption("Moralogy Engine v4.0 - Functional Test")
