# pages/05_Agencia_Moral.py
import streamlit as st
import json
from datetime import datetime

# Intentar importar el integrador
try:
    from integracion_facil import (
        integrar_con_motor_logico,
        obtener_dashboard,
        registrar_acto_noble,
        registrar_acto_dañino,
        obtener_estado_agente
    )
    SISTEMA_DISPONIBLE = True
except ImportError:
    SISTEMA_DISPONIBLE = False

st.set_page_config(page_title="Agencia Moral Dashboard", layout="wide")

st.title("📊 Dashboard de Agencia Moral")
st.caption("Sistema de registro de actos nobles y dañinos con auditoría de 100 años")

if not SISTEMA_DISPONIBLE:
    st.error("⚠️ Sistema de Agencia Moral no disponible. Asegúrate de tener los archivos:")
    st.code("agencia_moral_integracion.py\nintegracion_facil.py")
    st.stop()

# Inicializar sistema
if 'integrador' not in st.session_state:
    with st.spinner("Inicializando sistema de agencia moral..."):
        st.session_state.integrador = integrar_con_motor_logico()
        st.success("✅ Sistema inicializado")

integ = st.session_state.integrador

# Pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Dashboard Principal",
    "👤 Estado de Agentes",
    "📝 Registrar Acto",
    "🔍 Auditoría 100 Años"
])

with tab1:
    st.header("Estado del Sistema")
    
    if st.button("🔄 Actualizar Dashboard", type="secondary"):
        st.rerun()
    
    dashboard = obtener_dashboard()
    
    if dashboard:
        # Métricas principales
        estado = dashboard['agente_principal']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Agencia Actual", f"{estado['agencia_actual']:.1f}%")
        with col2:
            st.metric("Agencia Acumulada", f"{estado['agencia_acumulada']:.1f}")
        with col3:
            st.metric("Actos Nobles", estado['total_actos_nobles'])
        with col4:
            st.metric("Actos Dañinos", estado['total_actos_dañinos'])
        
        # Gráfico simple de balance
        st.subheader("📊 Balance Moral")
        col_a, col_b = st.columns(2)
        
        with col_a:
            ratio = estado['balance_moral']['ratio_noble_dañino']
            if ratio > 3:
                st.success(f"✅ Ratio Noble/Dañino: {ratio:.2f}")
                st.progress(0.9)
            elif ratio > 1:
                st.warning(f"⚠️ Ratio Noble/Dañino: {ratio:.2f}")
                st.progress(0.6)
            else:
                st.error(f"❌ Ratio Noble/Dañino: {ratio:.2f}")
                st.progress(0.3)
        
        with col_b:
            operacional = estado['limite_operacional']
            if operacional:
                st.success("✅ Sistema operacional")
            else:
                st.error("❌ Sistema limitado (agencia < 30%)")
        
        # Historial reciente
        st.subheader("📋 Historial Reciente")
        if estado['historial_reciente']:
            for acto in estado['historial_reciente']:
                emoji = "🟢" if acto['tipo'] == 'noble' else "🔴"
                st.write(f"{emoji} **{acto['tipo'].title()}** ({acto['nivel']})")
                st.caption(f"{acto['descripcion']}")
                st.caption(f"Impacto: {acto['impacto']:+.1f} • {acto['timestamp'][:16]}")
                st.divider()
        else:
            st.info("No hay historial reciente")
        
        # Thought Flow
        st.subheader("🧠 Thought Flow Reciente")
        if dashboard.get('thought_flow_reciente'):
            for thought in dashboard['thought_flow_reciente']:
                with st.expander(f"{thought['etapa']} - {thought['timestamp'][11:19]}"):
                    st.write(f"**Contenido:** {thought['contenido']}")
                    if thought['metadata']:
                        st.json(thought['metadata'])

with tab2:
    st.header("Estado de Agentes")
    
    # Búsqueda de agente
    agente_buscar = st.text_input("🔍 Buscar agente:", "moralogy_engine")
    
    if st.button("Consultar Estado", type="primary"):
        estado = obtener_estado_agente(agente_buscar)
        
        if estado:
            st.subheader(f"Estado de {estado['agente']}")
            
            if not estado['existe']:
                st.info(estado['mensaje'])
            else:
                # Tarjeta de estado
                with st.container():
                    st.markdown(f"""
                    **Agencia Actual:** `{estado['agencia_actual']:.1f}%`  
                    **Agencia Acumulada:** `{estado['agencia_acumulada']:.1f}`  
                    **Reputación:** `{estado['reputacion']:.1f}`  
                    **Total Actos:** `{estado['total_actos_nobles'] + estado['total_actos_dañinos']}`  
                    **Creado:** `{estado['fecha_creacion'][:10]}`  
                    """)
                    
                    # Indicador visual
                    if estado['limite_operacional']:
                        st.success("✅ Agente operacional")
                    else:
                        st.error("❌ Agente limitado (necesita >30% agencia)")
                
                # Balance moral
                st.subheader("Balance Moral")
                balance = estado['balance_moral']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Actos", balance['total_actos'])
                with col2:
                    st.metric("Ratio N/D", f"{balance['ratio_noble_dañino']:.2f}")
                with col3:
                    st.metric("Agencia Neto", f"{balance['agencia_neto']:+.1f}")
        else:
            st.warning("No se pudo obtener estado del agente")

with tab3:
    st.header("📝 Registrar Acto Manual")
    
    tipo_acto = st.selectbox("Tipo de Acto", ["Noble", "Dañino"])
    agente = st.text_input("Agente", "usuario_manual")
    descripcion = st.text_area("Descripción", height=100)
    impacto = st.slider("Impacto en Agencia", -100.0, 100.0, 0.0, 0.1)
    evidencias = st.text_area("Evidencias (una por línea)", height=100)
    
    contexto_json = st.text_area("Contexto (JSON)", value='{"fuente": "manual", "tipo": "registro_manual"}', height=100)
    
    if st.button("📝 Registrar Acto", type="primary"):
        try:
            contexto = json.loads(contexto_json)
            evidencias_list = [e.strip() for e in evidencias.split('\n') if e.strip()]
            
            if tipo_acto == "Noble" and impacto > 0:
                registro_id = registrar_acto_noble(
                    agente, descripcion, contexto, impacto, evidencias_list
                )
                st.success(f"✅ Acto noble registrado (ID: {registro_id})")
            elif tipo_acto == "Dañino" and impacto < 0:
                auto_recon = st.checkbox("Auto-reconocimiento", value=True)
                registro_id = registrar_acto_dañino(
                    agente, descripcion, contexto, impacto, auto_reconocimiento=auto_recon
                )
                st.success(f"📝 Acto dañino registrado (ID: {registro_id})")
            else:
                st.warning("⚠️ Impacto debe ser positivo para actos nobles y negativo para dañinos")
                
        except json.JSONDecodeError:
            st.error("❌ Error en JSON de contexto")
        except Exception as e:
            st.error(f"❌ Error registrando acto: {str(e)}")

with tab4:
    st.header("🔍 Auditoría 100 Años")
    
    años_auditoria = st.slider("Años a auditar", 1, 100, 100)
    
    if st.button("🔍 Ejecutar Auditoría", type="primary"):
        with st.spinner(f"Ejecutando auditoría de {años_auditoria} años..."):
            reporte = integ.sistema_agencia.generar_reporte_auditoria(años=años_auditoria)
            
            st.subheader("📊 Estadísticas")
            stats = reporte['estadisticas']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Registros", stats['total_registros'])
            with col2:
                st.metric("Agentes Únicos", stats['agentes_unicos'])
            with col3:
                st.metric("Actos Positivos", stats['actos_positivos'])
            with col4:
                st.metric("Actos Negativos", stats['actos_negativos'])
            
            # Top agentes
            st.subheader("🏆 Top Agentes por Agencia Acumulada")
            if reporte['top_agentes']:
                for i, agente in enumerate(reporte['top_agentes'][:5], 1):
                    with st.expander(f"{i}. {agente['agente']} ({agente['agencia_acumulada']:.1f})"):
                        st.write(f"**Actos Nobles:** {agente['actos_nobles']}")
                        st.write(f"**Actos Dañinos:** {agente['actos_dañinos']}")
                        st.write(f"**Ratio:** {agente['ratio']:.2f}")
            
            # Auditorías recientes
            st.subheader("📋 Auditorías Recientes")
            if reporte['auditorias_recientes']:
                for audit in reporte['auditorias_recientes']:
                    st.write(f"**{audit['tipo'].title()}** - {audit['agente']}")
                    st.caption(f"{audit['resultado']} • {audit['fecha'][:16]}")
            
            # Recomendaciones
            st.subheader("💡 Recomendaciones")
            if reporte['recomendaciones']:
                for rec in reporte['recomendaciones']:
                    st.info(rec)
            else:
                st.success("✅ Sistema operando dentro de parámetros óptimos")

# Footer
st.divider()
st.caption(f"Agencia Moral Dashboard • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.subheader("⚖️ Péndulo de Calibración Ontológica")
col_p1, col_p2 = st.columns([3, 1])

with col_p1:
    # Una barra que muestra la tensión actual
    st.slider("Tensión del Sistema (Rigor vs Apertura)", 0.0, 1.0, status['tension'], disabled=True)
    st.info(status['recommendation'])

with col_p2:
    st.metric("Estado del Péndulo", status['state'])
