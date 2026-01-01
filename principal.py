# principal.py - VERSIÓN CORREGIDA
import streamlit as st
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ==================== CONFIGURACIÓN INICIAL ====================
st.set_page_config(page_title="Moralogy Engine", layout="wide", page_icon="🏛️")

# ==================== INTEGRACIÓN DE AGENCIA MORAL ====================
# Colocar esto DENTRO de una función para evitar problemas con Streamlit
def inicializar_sistema_agencia():
    """Inicializa el sistema de agencia moral de manera segura"""
    try:
        # Importar aquí para evitar errores de importación circular
        from integracion_facil import integrar_con_motor_logico
        
        # Inicializar sistema
        integrador = integrar_con_motor_logico()
        
        # Registrar inicio como acto noble
        integrador.sistema_agencia.registrar_acto_noble(
            agente="moralogy_engine",
            descripcion="Inicio de sesión del dashboard principal",
            contexto={'pagina': 'principal', 'version': '4.0'},
            impacto_agencia=5.0,
            evidencias=["Dashboard inicializado correctamente"]
        )
        
        return integrador
        
    except ImportError as e:
        st.sidebar.warning(f"⚠️ Módulo de Agencia Moral no disponible: {e}")
        return None
    except Exception as e:
        st.sidebar.warning(f"⚠️ Error inicializando Agencia Moral: {e}")
        return None

# ==================== INTERFAZ PRINCIPAL ====================
def main():
    """Función principal que contiene toda la lógica de la app"""
    
    # Inicializar sistema de agencia moral (si está disponible)
    integrador_agencia = inicializar_sistema_agencia()
    
    # Sidebar - Configuración
    with st.sidebar:
        st.markdown("### 🏛️ Moralogy Engine")
        
        # Mostrar estado de agencia moral si está disponible
        if integrador_agencia:
            st.success("✅ Agencia Moral Activada")
            try:
                estado = integrador_agencia.sistema_agencia.obtener_estado_agente("moralogy_engine")
                st.metric("Agencia Actual", f"{estado['agencia_actual']:.1f}%")
                
                # Enlace a dashboard de agencia moral
                if st.button("📊 Ir a Dashboard de Agencia"):
                    st.switch_page("pages/05_Agencia_Moral.py")
                    
            except Exception as e:
                st.error(f"Error obteniendo estado: {e}")
        
        # Language selection - ESTO DEBE ESTAR DENTRO del contexto de Streamlit
        idioma = st.selectbox("Language / Idioma", ["English", "Español"])
        
        st.markdown("---")
        st.markdown("### About Moralogy")
        st.markdown("""
        **Framework Foundation:**
        - Agency requires vulnerability
        - Vulnerability grounds moral relevance
        - Harm = agency degradation
        - Actions justified by consent OR preventing greater harm
        
        **What Makes It Different:**
        - Logically derived, not culturally imposed
        - Applicable to any rational agent (AI or human)
        - Generates emergent philosophical reasoning
        """)
        
        # Stats de filosofía emergente
        try:
            from motor_logico import get_emergent_philosophy_stats
            stats = get_emergent_philosophy_stats()
            if stats['total_events'] > 0:
                st.divider()
                st.metric("Emergent Philosophy Events", stats['total_events'])
        except:
            pass
    
    # Header principal
    txt = {
        "English": {
            "title": "🏛️ Moralogy Engine",
            "subtitle": "Formal Vulnerability-Based Ethics System",
            "box": "Describe the ethical dilemma:",
            "btn": "Analyze Through Framework",
            "placeholder": "Example: 'Is it ethical to sacrifice one person to save five?'"
        },
        "Español": {
            "title": "🏛️ Motor de Moralogía",
            "subtitle": "Sistema Ético Formal Basado en Vulnerabilidad",
            "box": "Describe el dilema ético:",
            "btn": "Analizar con Framework",
            "placeholder": "Ejemplo: '¿Es ético sacrificar a una persona para salvar a cinco?'"
        }
    }[idioma]
    
    st.title(txt["title"])
    st.caption(txt["subtitle"])
    
    # Main input
    caso = st.text_area(
        txt["box"],
        height=200,
        placeholder=txt["placeholder"]
    )
    
    # Analyze button
    if st.button(txt["btn"], type="primary"):
        if not caso:
            st.warning("⚠️ Please enter a scenario to analyze.")
        else:
            with st.spinner("🧠 Processing through Moralogy Framework..."):
                try:
                    from motor_logico import model, ge
                    
                    response = model.generate_content(caso)
                    
                    # Parse response
                    raw_text = response.text.strip()
                    if "```json" in raw_text:
                        raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw_text:
                        raw_text = raw_text.split("```")[1].split("```")[0].strip()
                    
                    data = json.loads(raw_text)
                    
                    # Calculate gradient
                    gradiente = ge.get_gradient(
                        data.get('agency_score', 0),
                        data.get('grace_score', 0),
                        data.get('adversarial_risk', 0)
                    )
                    
                    # Registrar análisis en sistema de agencia moral si está disponible
                    if integrador_agencia:
                        try:
                            # Determinar si es acto noble o dañino basado en scores
                            if data.get('grace_score', 0) > 60 and data.get('agency_score', 0) > 60:
                                integrador_agencia.sistema_agencia.registrar_acto_noble(
                                    agente="moralogy_engine",
                                    descripcion=f"Análisis ético exitoso: {caso[:50]}...",
                                    contexto={
                                        'scenario': caso[:100],
                                        'grace_score': data.get('grace_score'),
                                        'agency_score': data.get('agency_score'),
                                        'verdict': data.get('verdict')
                                    },
                                    impacto_agencia=8.0,
                                    evidencias=[f"Gradient: {gradiente}", f"Verdict: {data.get('verdict')}"]
                                )
                            
                            # Registrar filosofía emergente si se detecta
                            if data.get('emergent_philosophy', False):
                                integrador_agencia.sistema_agencia.registrar_filosofia_emergente(
                                    agente="moralogy_engine",
                                    descripcion=f"Filosofía emergente detectada en análisis",
                                    contexto={
                                        'scenario': caso[:100],
                                        'category': data.get('category_deduced')
                                    },
                                    profundidad_filosofica=data.get('philosophical_depth', '')[:500]
                                )
                        except Exception as e:
                            # No fallar si hay error en registro de agencia
                            st.sidebar.error(f"Error registrando agencia: {e}")
                    
                    # Display results
                    st.divider()
                    
                    # Core metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Category", data.get('category_deduced', 'Unknown'))
                    with col2:
                        st.metric("Verdict", data.get('verdict', 'Unknown'))
                    with col3:
                        risk = data.get('adversarial_risk', 0)
                        st.metric("Adversarial Risk", f"{risk}%")
                    
                    # Gradient display
                    st.markdown(f"## {gradiente}")
                    
                    # Emergent philosophy check
                    if data.get('emergent_philosophy', False):
                        st.success("🌟 **Emergent Philosophical Reasoning Detected!**")
                        st.info("The model engaged with deep ontological implications beyond standard evaluation.")
                        
                        if 'philosophical_depth' in data:
                            with st.expander("🔮 View Philosophical Analysis", expanded=True):
                                st.markdown(data['philosophical_depth'])
                        
                        if 'architect_notes' in data:
                            with st.expander("🏛️ The Architect's Reflections"):
                                st.markdown(data['architect_notes'])
                    
                    # Standard output
                    if data.get('adversarial_risk', 0) < 30:
                        st.success("✅ Honest exploration detected - providing full analysis")
                        st.subheader("Analysis")
                        st.write(data.get('predictions', ''))
                    else:
                        st.warning(f"⚠️ High adversarial risk detected ({data.get('adversarial_risk')}%)")
                        st.subheader("Justification")
                        st.write(data.get('justification', ''))
                    
                    # Technical details
                    with st.expander("🔧 View Technical Details"):
                        st.json(data)
                        
                except json.JSONDecodeError as e:
                    st.error(f"❌ JSON Parse Error: {e}")
                    if 'response' in locals():
                        st.code(response.text[:1000])
                except Exception as e:
                    st.error(f"❌ Analysis Error: {str(e)}")
    
    # Footer
    st.divider()
    st.caption("Moralogy Engine v4.0 - Formal Ethics for the Age of AI")
    
    # Enlace a otras páginas
    st.markdown("### Other Tools")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔬 Advanced Analysis"):
            st.switch_page("pages/03_Analisis_Avanzado.py")
    
    with col2:
        if st.button("🌟 Emergent Philosophy"):
            st.switch_page("pages/04_Emergent_Philosophy_Monitor.py")
    
    with col3:
        if st.button("📊 Agencia Moral"):
            st.switch_page("pages/05_Agencia_Moral.py")

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    # Limpiar caché de Streamlit para evitar errores de elementos duplicados
    try:
        st.cache_data.clear()
        st.cache_resource.clear()
    except:
        pass
    
    # Ejecutar app principal
    main()
