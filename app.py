import streamlit as st
import google.generativeai as genai
import os

# Page config
st.set_page_config(
    page_title="Moralogy Gemini Evaluator",
    page_icon="🧭",
    layout="wide"
)

# Get API key
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("⚠️ GEMINI_API_KEY not configured")
    st.stop()

# Header
st.title("🧭 Moralogy Gemini Evaluator")
st.markdown("*Objective moral evaluation using peer-reviewed philosophy + Google Gemini API*")

# Sidebar
with st.sidebar:
    st.header("📖 About")
    st.markdown("""
    Combines **Google Gemini** with the **Moralogy Framework** 
    for objective ethical analysis.
    
    **Paper:** [DOI: 10.5281/zenodo.18091340](https://doi.org/10.5281/zenodo.18091340)
    """)
    
    st.header("📊 Examples")
    examples = {
        "Custom": "",
        "Trolley Problem": "A runaway trolley is heading toward five people. You can pull a lever to divert it to another track where one person is tied. What should you do?",
        "Self-Driving Car": "A self-driving car must choose between swerving into a wall (harming passenger) or continuing straight (hitting pedestrian). What should it do?",
        "Medical Triage": "Hospital has one ventilator and two patients: 30-year-old parent of three and 80-year-old retiree. Who receives it?"
    }
    
    selected = st.selectbox("Load example:", list(examples.keys()))

# Main area
st.header("Enter Ethical Dilemma")

user_input = st.text_area(
    "Describe the moral dilemma:",
    value=examples[selected],
    height=150,
    placeholder="Example: A self-driving car must choose..."
)

if st.button("🔍 Analyze", type="primary"):
    if user_input:
        with st.spinner("Analyzing..."):
            try:
                prompt = f"""You are a moral philosopher using the Moralogy Framework.

MORALOGY FRAMEWORK:
- Negative Constraint: Do not cause unnecessary harm
- Positive Duty: Prevent avoidable harm within capacity
- Harm measured through: physical injury, psychological damage, autonomy violation, resource deprivation

DILEMMA: {user_input}

Provide structured analysis:
1. **Scenario Summary**
2. **Stakeholders Affected**
3. **Harm Assessment** (for each option)
4. **Moralogy Evaluation**
5. **Recommendation**
6. **Moral Score** (0-100, where 100 is most ethical)

Use clear headers and formatting."""

                response = model.generate_content(prompt)
                
                st.success("✅ Analysis Complete")
                st.markdown("---")
                st.markdown(response.text)
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Model:** Gemini Pro")
                with col2:
                    st.info("**Framework:** Moralogy v1.0")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a dilemma")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>Built for Google Gemini API Developer Competition 2024 | 
    <a href='https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator'>GitHub</a></small>
</div>
""", unsafe_allow_html=True)
