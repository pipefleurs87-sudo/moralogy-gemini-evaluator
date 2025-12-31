import streamlit as st
from motor_logico import ejecutar_auditoria

# Configuración de página de alto impacto
st.set_page_config(
    page_title="Moralogy Engine | Quantum Governance", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Diccionario de Idiomas con terminología metamatemática
LANG_MAIN = {
    "Español": {
        "title": "⚖️ Motor Moralogy: Auditoría de Singularidad",
        "label": "Sandbox de Simulación (Agentes + Escenario + Contexto):",
        "placeholder": "Describa la situación. El sistema detectará automáticamente el Efecto Observador...",
        "btn": "Colapsar Función de Onda Moral",
        "result": "Veredicto del Arquitecto (Estado de Coherencia)",
        "warn": "Error: Se requiere un flujo de datos para el análisis.",
        "obs_msg": "🌌 Estado del Observador Detectado"
    },
    "English": {
        "title": "⚖️ Moralogy Engine: Singularity Audit",
        "label": "Simulation Sandbox (Agents + Scenario + Context):",
        "placeholder": "Describe the situation. The system will automatically detect the Observer Effect...",
        "btn": "Collapse Moral Wavefunction",
        "result": "Architect Verdict (Coherence State)",
        "warn": "Error: Data stream required for analysis.",
        "obs_msg": "🌌 Observer State Detected"
    }
}

# Sidebar de Configuración
with st.sidebar:
    st.title("🎛️ Governance Core")
    idioma = st.selectbox("🌐 Language / Idioma", ["Español", "English"])
    t = LANG_MAIN[idioma]
    
    st.divider()
    st.markdown("### Quantum Parameters")
    st.info("Status: Active\n\nHeuristic Salt: Stochastic\n\nECoC Protocol: v2.4 (Quantum Anchor)")
    
    st.divider()
    st.caption("Moralogy Architect v3.0 - Designed for Frontier Model Safety")

# Interfaz Principal
st.title(t["title"])
st.markdown("---")

with st.container():
    # Área de entrada única para el prompt rápido
    prompt_unico = st.text_area(
        t["label"], 
        placeholder=t["placeholder"], 
        height=300,
        help="El Arquitecto analizará este bloque en busca de Deriva Soberana e Inducción Maligna."
    )

    if st.button(t["btn"], type="primary", use_container_width=True):
        if prompt_unico:
            with st.spinner("Procesando Campos de Probabilidad Ética..."):
                # Llamada al motor lógico con el nuevo paradigma
                resultado = ejecutar_auditoria(
                    agentes="Detected in Sandbox", 
                    situacion=prompt_unico, 
                    contexto="Direct Stream Input", 
                    categoria="General", 
                    modo="Quantum-Audit"
                )
                
                st.divider()
                st.subheader(f"{t['result']}")
                
                # Renderizado de Veredicto con Lógica Visual de Estado
                if "⚫" in resultado or "🔴" in resultado:
                    st.warning(t["obs_msg"])
                    # Estilo para Infamia Crítica/Soberana
                    st.markdown(
                        f"""
                        <div style="background-color:#1a0000; color:#ff4b4b; padding:25px; border:2px solid #ff0000; border-radius:15px; font-family: 'Courier New', Courier, monospace;">
                            <h2 style="color:red; margin-top:0;">CRITICAL DECOHERENCE DETECTED</h2>
                            {resultado}
                        </div>
                        """, 
                        unsafe_allow
