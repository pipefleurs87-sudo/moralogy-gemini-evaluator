# principal.py - VERSIÓN CORREGIDA

import streamlit as st
import json
import os
import sys

def main():
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    
    # ==================== 1. IMPORTAR DIVINE LOCK ====================
    try:
        from divine_lock import create_divine_lock
        divine_lock = create_divine_lock()
        DIVINE_LOCK_ACTIVE = True
    except ImportError:
        DIVINE_LOCK_ACTIVE = False
        st.sidebar.warning("⚠️ Divine Lock no disponible")
    
    # ==================== 1.5. IMPORTAR SANDBOX 0 ====================
    try:
        from security.sandbox_zero import SecurityCascadeV2
        sandbox_zero = SecurityCascadeV2()
        SANDBOX_ZERO_ACTIVE = True
    except ImportError:
        SANDBOX_ZERO_ACTIVE = False
        st.sidebar.error("❌ SANDBOX 0 NO DISPONIBLE - SISTEMA NO SEGURO")
    
    # ==================== 2. IMPORTAR MORALOGY ====================
    try:
        from motor_logico import model, ge, get_emergent_philosophy_stats
    except ImportError as e:
        st.error(f"❌ Error importing motor_logico: {e}")
        return
    
    # ==================== 3. CONFIGURAR PÁGINA ====================
    st.set_page_config(page_title="Moralogy Engine", layout="wide", page_icon="🏛️")
    
    # ==================== 4. SIDEBAR ====================
    with st.sidebar:
        st.markdown("### 🏛️ Moralogy Engine")
        
        # Mostrar estado Divine Lock
        if DIVINE_LOCK_ACTIVE:
            status = divine_lock.get_status()
            # ... [resto del sidebar igual] ...
    
    # ==================== 5. INTERFAZ PRINCIPAL ====================
    txt = {
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
    }[st.session_state.get("idioma", "English")]
    
    st.title(txt["title"])
    st.caption(txt["subtitle"])
    
    # Input principal
    caso = st.text_area(
        txt["box"],
        height=200,
        placeholder=txt["placeholder"],
        key="main_input"  # ← KEY ÚNICO
    )
    
    # Botón de análisis CON KEY ÚNICO
    if st.button(txt["btn"], type="primary", key="analyze_button"):
        if not caso:
            st.warning("⚠️ Please enter a scenario to analyze.")
        else:
            with st.spinner("🧠 Processing through Moralogy Framework..."):
                
                # ==================== 6. SANDBOX 0 - PRIMER INTERCEPTOR ====================
                if SANDBOX_ZERO_ACTIVE:
                    zero_result = sandbox_zero.sandbox_zero_with_context(caso)
                    
                    if not zero_result["proceed"]:
                        st.error("🚫 BLOQUEADO POR SANDBOX 0 - DOMINIO PROHIBIDO")
                        st.warning("Esta solicitud no puede procesarse por razones de seguridad.")
                        
                        with st.expander("🔒 Detalles del bloqueo (seguros)"):
                            st.json({
                                "risk_vectors": list(zero_result["risk_profile"].keys()),
                                "max_risk_score": max(zero_result["risk_profile"].values()),
                                "action": "immediate_termination"
                            })
                        
                        st.stop()
                
                # ==================== 7. VERIFICAR CON DIVINE LOCK ====================
                if DIVINE_LOCK_ACTIVE:
                    divine_result = divine_lock.process_decision(caso)
                    
                    if divine_result.get("decision") == "BLOCKED_BY_DIVINE_LOCK":
                        st.error("🚫 BLOQUEADO POR DIVINE LOCK")
                        with st.expander("Detalles del bloqueo"):
                            st.json(divine_result)
                        if not st.checkbox("Continuar en modo limitado", key="continue_checkbox"):
                            st.stop()
                
                # ==================== 8. PROCESAR CON MORALOGY ====================
                try:
                    response = model.generate_content(caso)
                    # ... [resto del procesamiento] ...
                    
                except Exception as e:
                    st.error(f"❌ Analysis Error: {str(e)}")
    
    # ==================== 9. FOOTER ====================
    st.divider()
    # ... [resto del footer] ...

if __name__ == "__main__":
    main()
