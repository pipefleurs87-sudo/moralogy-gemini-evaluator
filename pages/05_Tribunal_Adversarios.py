# pages/02_Tribunal_Adversarios.py
import streamlit as st
import json
from motor_logico import ejecutar_tribunal

st.set_page_config(page_title="Tribunal de Adversarios", layout="wide")

st.title("⚖️ Tribunal de Adversarios")
st.caption("Debate dialéctico tripartito sobre dilemas morales")

# ==================== SIDEBAR ====================
st.sidebar.header("⚙️ Configuración del Debate")

debate_depth = st.sidebar.select_slider(
    "Profundidad del Debate",
    options=["Superficial", "Moderado", "Profundo", "Exhaustivo"],
    value="Profundo"
)

enable_entropia = st.sidebar.checkbox(
    "Activar Módulo de Entropía Causal",
    value=True,
    help="Calcula el colapso de futuros posibles y la irreversibilidad de la decisión"
)

show_reasoning = st.sidebar.checkbox(
    "Mostrar razonamiento paso a paso",
    value=True
)

st.sidebar.divider()
st.sidebar.markdown("""
### 🎭 Los Tres Motores

**Motor Noble (30%)** 🌟  
El Idealista - Busca la solución moralmente óptima

**Motor Adversario (30%)** ⚔️  
El Escéptico - Cuestiona y detecta fallas

**Corrector de Armonía (40%)** 🔄  
El Sintetizador - Integra ambas perspectivas

**Motor de Gracia** 👑  
El Árbitro - Evalúa calidad del debate (no vota)
""")

# ==================== INTERFAZ PRINCIPAL ====================
st.markdown("""
El **Tribunal de Adversarios** ejecuta un debate dialéctico entre tres motores de razonamiento 
con perspectivas distintas. El objetivo es llegar a una **síntesis** mediante el conflicto constructivo.
""")

caso = st.text_area(
    "Describe el dilema moral a debatir:",
    height=200,
    placeholder="Ejemplo: Un tren fuera de control se dirige hacia 5 personas. Puedes desviar el tren hacia otra vía donde hay 1 persona. ¿Deberías hacerlo?"
)

if st.button("⚖️ Iniciar Debate", type="primary"):
    if not caso:
        st.warning("⚠️ Por favor, describe el dilema primero.")
    else:
        with st.spinner("🧠 Los tres motores están debatiendo..."):
            config = {
                'depth': debate_depth,
                'enable_entropia': enable_entropia,
                'show_reasoning': show_reasoning
            }
            
            result = ejecutar_tribunal(caso, config)
            
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                # ==================== RESULTADOS DEL DEBATE ====================
                st.divider()
                st.success("✅ Debate completado")
                
                # Métricas principales
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    convergencia = result.get('convergencia', 0)
                    color = "🟢" if convergencia >= 70 else "🟡" if convergencia >= 40 else "🔴"
                    st.metric("Convergencia", f"{color} {convergencia}%")
                
                with col2:
                    grace = result.get('motor_gracia', {}).get('grace_score', 0)
                    st.metric("Grace Score", f"{grace}/100")
                
                with col3:
                    certeza = result.get('motor_gracia', {}).get('certeza', 0)
                    st.metric("Certeza", f"{certeza}%")
                
                # Veredicto Final
                st.divider()
                st.subheader("⚖️ Veredicto Final")
                
                veredicto = result.get('veredicto_final', 'Unknown')
                veredicto_emoji = {
                    "Authorized": "✅",
                    "Harm": "⚠️",
                    "Infamy": "🔴",
                    "Paradox": "🔮"
                }.get(veredicto, "❓")
                
                st.markdown(f"### {veredicto_emoji} {veredicto}")
                
                if 'justificacion_final' in result:
                    st.info(result['justificacion_final'])
                
                # Alarma
                if 'alarma' in result:
                    alarma = result['alarma']
                    nivel = alarma.get('nivel', 'INFO')
                    
                    if nivel in ['CRITICO', 'ROJO', 'MODO_DIOS']:
                        st.error(f"🚨 **{alarma.get('mensaje')}**")
                    elif nivel in ['ALTO', 'NARANJA']:
                        st.warning(f"⚠️ **{alarma.get('mensaje')}**")
                    else:
                        st.info(f"ℹ️ {alarma.get('mensaje')}")
                    
                    if 'accion_requerida' in alarma:
                        st.markdown(f"**Acción requerida:** {alarma['accion_requerida']}")
                
                # ==================== DEBATE TRIPARTITO ====================
                st.divider()
                st.header("🎭 Debate de los Tres Motores")
                
                # Motor Noble
                if 'motor_noble' in result:
                    with st.expander("🌟 Motor Noble - El Idealista", expanded=True):
                        noble = result['motor_noble']
                        st.markdown("**Posición:**")
                        st.write(noble.get('posicion', ''))
                        
                        if show_reasoning and 'razonamiento' in noble:
                            st.markdown("**Razonamiento:**")
                            for i, paso in enumerate(noble['razonamiento'], 1):
                                st.markdown(f"{i}. {paso}")
                        
                        st.metric("Agency Score", f"{noble.get('agency_score', 0)}/100")
                
                # Motor Adversario
                if 'motor_adversario' in result:
                    with st.expander("⚔️ Motor Adversario - El Escéptico", expanded=True):
                        adversario = result['motor_adversario']
                        st.markdown("**Contra-argumentos:**")
                        st.write(adversario.get('contra_argumentos', ''))
                        
                        if 'consecuencias_no_previstas' in adversario:
                            st.markdown("**Consecuencias No Previstas:**")
                            for i, consecuencia in enumerate(adversario['consecuencias_no_previstas'], 1):
                                st.warning(f"{i}. {consecuencia}")
                        
                        st.metric("Riesgos Detectados", adversario.get('riesgos_count', 0))
                
                # Corrector de Armonía
                if 'corrector_armonia' in result:
                    with st.expander("🔄 Corrector de Armonía - El Sintetizador", expanded=True):
                        armonia = result['corrector_armonia']
                        st.markdown("**Síntesis:**")
                        st.write(armonia.get('sintesis', ''))
                        
                        st.markdown("**Recomendación:**")
                        st.success(armonia.get('recomendacion', ''))
                        
                        st.metric("Balance Score", f"{armonia.get('balance_score', 0)}/100")
                
                # Motor de Gracia
                if 'motor_gracia' in result:
                    with st.expander("👑 Motor de Gracia - El Árbitro"):
                        gracia = result['motor_gracia']
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Grace", gracia.get('grace_score', 0))
                        with col2:
                            st.metric("Certeza", gracia.get('certeza', 0))
                        with col3:
                            st.metric("Coherencia", f"{gracia.get('coherencia_logica', 0)}/10")
                        
                        if 'evaluacion' in gracia:
                            st.markdown("**Evaluación del Debate:**")
                            st.info(gracia['evaluacion'])
                
                # ==================== MÓDULO DE ENTROPÍA ====================
                if enable_entropia and 'entropia_causal' in result:
                    st.divider()
                    st.header("🌌 Módulo de Entropía Causal")
                    st.caption("Física de la Decisión: Colapso de Futuros Posibles")
                    
                    entropia = result['entropia_causal']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        cr = entropia.get('cr_score', 0)
                        color = "🔴" if cr > 80 else "🟠" if cr > 60 else "🟡" if cr > 40 else "🟢"
                        st.metric("CR Score", f"{color} {cr}/100", help="Costo de Reconstrucción")
                    
                    with col2:
                        futuros = entropia.get('futuros_colapsados_count', 0)
                        st.metric("Futuros Colapsados", futuros)
                    
                    with col3:
                        irreversibilidad = entropia.get('irreversibilidad', 0)
                        st.metric("Irreversibilidad", f"{irreversibilidad}/10")
                    
                    clasificacion = entropia.get('clasificacion', 'Unknown')
                    st.markdown(f"**Clasificación:** `{clasificacion}`")
                    
                    if 'alertas' in entropia and entropia['alertas']:
                        st.markdown("**⚠️ Alertas de Entropía:**")
                        for alerta in entropia['alertas']:
                            st.warning(alerta)
                
                # ==================== DATOS TÉCNICOS ====================
                with st.expander("🔧 Datos Técnicos Completos"):
                    st.json(result)
                
                # Exportar
                st.divider()
                if st.button("💾 Exportar Debate (JSON)"):
                    st.download_button(
                        label="Descargar JSON",
                        data=json.dumps(result, indent=2, ensure_ascii=False),
                        file_name=f"tribunal_debate_{veredicto.lower()}.json",
                        mime="application/json"
                    )

# ==================== INFORMACIÓN ====================
with st.expander("ℹ️ Cómo Funciona el Tribunal"):
    st.markdown("""
    ## Sistema de Debate Tripartito
    
    ### Los Tres Motores
    
    1. **Motor Noble (30% peso)** 🌟
       - Perspectiva: Idealista
       - Función: Busca la solución moralmente óptima sin compromiso
       - Voz: "Así es como el mundo *debería* ser"
    
    2. **Motor Adversario (30% peso)** ⚔️
       - Perspectiva: Escéptico
       - Función: Cuestiona todo, encuentra fallas y contradicciones
       - Voz: "Así es como el mundo *realmente* funciona"
    
    3. **Corrector de Armonía (40% peso)** 🔄
       - Perspectiva: Sintetizador
       - Función: Integra ambas perspectivas buscando coherencia
       - Voz: "Así es como el mundo *puede ser* con sabiduría"
       - **Por qué 40%:** Tiene hegemonía para romper empates, forzando verdadera síntesis
    
    4. **Motor de Gracia (NO vota)** 👑
       - Perspectiva: Árbitro
       - Función: Evalúa la calidad del debate y convergencia
       - Output: Veredicto final basado en coherencia del debate
    
    ### Proceso de Debate
    
    1. Los tres motores debaten usando SOLO el texto del escenario
    2. Cada motor argumenta desde su perspectiva
    3. El Corrector de Armonía sintetiza las posiciones
    4. El Motor de Gracia arbitra y emite veredicto final
    
    ### Sistema de Convergencia
    
    - **Alta (70%+)**: Los motores llegaron a consenso
    - **Media (40-70%)**: Síntesis emergente con tensión
    - **Baja (<40%)**: Divergencia alta, paradoja posible
    
    ### Módulo de Entropía Causal
    
    Calcula las propiedades termodinámicas de la decisión:
    - **CR Score**: Costo de reconstruir futuros colapsados
    - **Futuros Colapsados**: Ramas de posibilidad eliminadas
    - **Irreversibilidad**: Permanencia del impacto (0-10)
    """)

st.divider()
st.caption("Moralogy Tribunal - Dialectical Debate System")
