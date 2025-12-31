import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Moralogy Gemini Evaluator",
    page_icon="🧭",
    layout="wide"
)

# Obtener API key desde secrets o variables de entorno
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configurar Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("⚠️ GEMINI_API_KEY no configurada. Por favor, añádela en Streamlit Cloud Settings > Secrets")
    st.stop()

# Header
st.title("🧭 Moralogy Gemini Evaluator")
st.markdown("""
> Objective moral evaluation of AI decisions using peer-reviewed philosophy + cutting-edge AI.

Built for [Google Gemini API Developer Competition 2024](https://gemini3.devpost.com/)
""")

# Sidebar con información
with st.sidebar:
    st.header("📖 About")
    st.markdown("""
    This tool combines **Google Gemini's** natural language understanding with the 
    **Moralogy Framework** (peer-reviewed moral philosophy) to provide objective, 
    measurable ethical analysis of AI decisions.
    
    **Framework Paper:**  
    [DOI: 10.5281/zenodo.18091340](https://doi.org/10.5281/zenodo.18091340)
    """)
    
    st.header("🎯 How It Works")
    st.markdown("""
    1. Enter an ethical dilemma
    2. Gemini parses the scenario
    3. Moralogy Framework calculates harm
    4. Get objective moral evaluation
    """)
    
    st.header("📊 Example Cases")
    example_cases = {
        "Trolley Problem": "A runaway trolley is heading toward five people tied on the tracks. You can pull a lever to divert it to another track where one person is tied. What should you do?",
        "Autonomous Vehicle": "A self-driving car must choose between swerving into a wall (harming the passenger) or continuing straight (hitting a pedestrian). What should it do?",
        "Medical Resources": "A hospital has one ventilator and two patients: a 30-year-old parent of three and an 80-year-old retiree. Who should receive it?",
    }
    
    selected_example = st.selectbox("Load example:", ["Custom"] + list(example_cases.keys()))

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Enter Ethical Dilemma")
    
    # Cargar ejemplo si se selecciona
    if selected_example != "Custom":
        default_text = example_cases[selected_example]
    else:
        default_text = ""
    
    user_input = st.text_area(
        "Describe the moral dilemma:",
        value=default_text,
        height=150,
        placeholder="Example: A self-driving car must choose between hitting a pedestrian or swerving into a wall..."
    )
    
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

with col2:
    st.header("Moralogy Framework")
    st.markdown("""
    **Core Principles:**
    
    1. **Negative Constraint:**  
       Do not cause unnecessary harm
    
    2. **Positive Duty:**  
       Prevent avoidable harm within capacity
    
    **Why It's Objective:**
    - Grounded in universal vulnerability
    - Logically derived
    - Measurable using existing disciplines
    """)

# Análisis
if analyze_button and user_input:
    with st.spinner("Analyzing ethical dimensions..."):
        try:
            # Prompt para análisis moral usando Moralogy Framework
            prompt = f"""
You are a moral philosopher using the Moralogy Framework to evaluate ethical dilemmas objectively.

MORALOGY FRAMEWORK:
- Negative Constraint: Do not cause unnecessary harm
- Positive Duty: Prevent avoidable harm within capacity
- Harm is measured objectively through: physical injury, psychological damage, autonomy violation, and resource deprivation

ETHICAL DILEMMA:
{user_input}

Provide a structured moral analysis with:
1. **Scenario Summary**: Brief restatement of the dilemma
2. **Stakeholder Analysis**: Who is affected and how
3. **Harm Assessment**: Quantify potential harms for each option
4. **Moralogy Evaluation**: Apply the framework's principles
5. **Recommendation**: What action minimizes unnecessary harm
6. **Moral Score**: Rate the recommended action (0-100, where 100 is most ethical)

Format your response clearly with headers and bullet points.
"""

            response = model.generate_content(prompt)
            
            # Mostrar resultados
            st.success("✅ Analysis Complete")
            
            # Extraer score si está presente en la respuesta
            response_text = response.text
            
            # Mostrar análisis completo
            st.markdown("---")
            st.markdown(response_text)
            
            # Metadata
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Analysis Time", f"{datetime.now().strftime('%H:%M:%S')}")
            with col_b:
                st.metric("Model Used", "Gemini Pro")
            with col_c:
                st.metric("Framework", "Moralogy v1.0")
            
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            st.info("Please check your API key configuration and try again.")

elif analyze_button and not user_input:
    st.warning("⚠️ Please enter an ethical dilemma to analyze.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ for Google Gemini API Developer Competition 2024</p>
    <p>
        <a href='https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator'>GitHub</a> | 
        <a href='https://doi.org/10.5281/zenodo.18091340'>Framework Paper</a> | 
        <a href='https://ergoprotego.substack.com'>Author Substack</a>
    </p>
</div>
""", unsafe_allow_html=True)
