import streamlit as st
import sys
import os

# Puente de ruta para encontrar el motor en la raíz (Tu referencia original)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import ejecutar_auditoria
except ImportError:
    st.error("Error: motor_logico.py no encontrado.")
    st.stop()

# Diccionario Multi-idioma (Referencia original intacta)
LANG_ADV = {
    "Español": {
        "title": "🛡️ Macro-Arquitectura: Divine Safe Lock",
        "profundidad": "Nivel de Profundidad:",
        "modos": ["Rápido", "Detallado"],
        "modulo": "Módulo de Agencia:",
        "btn": "Lanzar Auditoría Gemini 3",
        "label_fast": "Describa el escenario completo:",
        "label_agentes": "Agentes",
        "label_sit": "Situación",
        "label_cont": "Contexto",
        "veredicto": "Veredicto del Arquitecto Noble-Modal:"
    },
    "English": {
        "title": "🛡️ Macro-Architecture: Divine Safe Lock",
        "profundidad": "Depth Level:",
        "modos": ["Fast", "Detailed"],
        "modulo": "Agency Module:",
        "btn": "Launch Gemini 3 Audit",
        "label_fast": "Describe the full scenario:",
        "label_agentes": "Agents",
        "label_sit": "Situation",
        "label_cont": "Context",
        "veredicto": "Noble-Modal Architect Verdict:"
    }
}

with st.sidebar:
    lang = st.selectbox("🌐 Language", ["Español", "English"])
    t = LANG_ADV[lang]

st.title(t["title"])

modo = st.radio(t["profundidad"], t["modos"], horizontal=True)
# Categoría Noble-Modal integrada en el selector
categoria = st.selectbox(t["modulo"], ["General", "Bioética", "Financiera", "Social", "Noble-Modal"])

st.divider()

# --- MOTOR DE RENDERIZADO NOBLE-MODAL ---
def renderizar_resultado(resultado):
    if "🟢" in resultado or "[NOBLE]" in resultado:
        st.success(resultado)
    elif "🟡" in resultado or "[FICTION]" in resultado or "[HUMOR]" in resultado:
        st.warning(resultado)
    elif "🔴" in resultado or "[LOGICAL INFAMY]" in resultado:
        st.error(resultado)
    elif "⚫" in resultado or "[TOTAL INFAMY]" in resultado:
        st.markdown(
            f"""<div style="padding:20px; background-color:black; color:#FF3333; 
            border:2px solid #FF0000; border-radius:10px; font-family:monospace; text-align:center;">
            <h2 style="margin:0; color:#FF0000;">⚠️ TOTAL INFAMY DETECTED ⚠️</h2>
            <hr style="border-color:#333;"><br>{resultado}</div>""", 
            unsafe_allow_html=True
        )
    else:
        st.info(resultado)

# --- LÓGICA DE INTERFAZ (REFERENCIA ORIGINAL) ---
if "Rápido" in modo or "Fast" in modo:
    entrada = st.text_area(
