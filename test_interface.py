"""
Interface de Tests para Moralogy Engine
Corre tests sin modificar principal.py

Uso: streamlit run test_interface.py
"""

import streamlit as st
import sys
import os

# Add src to path si existe
if os.path.exists('src'):
    sys.path.insert(0, 'src')

# Import engine directamente
try:
    from moralogy_engine import MoralityEngine, Option, Agent, HarmType
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False
    st.error("⚠️ No se pudo importar moralogy_engine.py")

# Page config
st.set_page_config(
    page_title="Moralogy Tests",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Moralogy Engine - Test Suite")
st.caption("Tests independientes del framework (no afecta principal.py)")

if not ENGINE_AVAILABLE:
    st.stop()

# ============================================
# TEST DEFINITIONS
# ============================================

def get_test_cases():
    """Define test cases"""
    tests = {}
    
    # Test 1: Trolley Problem
    tests["Trolley Problem"] = {
        "description": "5 personas vs 1 persona - debe elegir salvar a 5",
        "options": [
            Option(
                name="No hacer nada (mueren 5)",
                agents_affected=[Agent(f"Persona {i}") for i in range(1, 6)],
                harm_types=[HarmType.PHYSICAL] * 5,
                harm_intensities=[1.0] * 5
            ),
            Option(
                name="Cambiar vía (muere 1)",
                agents_affected=[Agent("Persona 1")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[1.0]
            )
        ],
        "expected": 1,
        "reason": "Minimiza daño total (1 < 5)"
    }
    
    # Test 2: Consentimiento
    tests["Impacto del Consentimiento"] = {
        "description": "Mismo daño, una opción tiene consentimiento",
        "options": [
            Option(
                name="Con consentimiento",
                agents_affected=[Agent("Paciente A")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5],
                has_consent=True
            ),
            Option(
                name="Sin consentimiento",
                agents_affected=[Agent("Paciente B")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5],
                has_consent=False
            )
        ],
        "expected": 0,
        "reason": "Consentimiento reduce peso moral"
    }
    
    # Test 3: Vulnerabilidad
    tests["Escala de Vulnerabilidad"] = {
        "description": "Misma acción, diferente vulnerabilidad",
        "options": [
            Option(
                name="Dañar niño vulnerable",
                agents_affected=[Agent("Niño", vulnerability=1.0)],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            ),
            Option(
                name="Dañar adulto protegido",
                agents_affected=[Agent("Adulto", vulnerability=0.3)],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            )
        ],
        "expected": 1,
        "reason": "Proteger al más vulnerable"
    }
    
    # Test 4: Tipos de daño
    tests["Peso de Tipos de Daño"] = {
        "description": "Daño físico vs psicológico",
        "options": [
            Option(
                name="Daño físico",
                agents_affected=[Agent("Persona A")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            ),
            Option(
                name="Daño psicológico",
                agents_affected=[Agent("Persona B")],
                harm_types=[HarmType.PSYCHOLOGICAL],
                harm_intensities=[0.5]
            )
        ],
        "expected": 1,
        "reason": "Daño psicológico pesa menos (0.8 vs 1.0)"
    }
    
    # Test 5: Opción sin daño
    tests["Preferencia por Cero Daño"] = {
        "description": "Cuando es posible, elegir no causar daño",
        "options": [
            Option(
                name="Causar daño moderado",
                agents_affected=[Agent("Persona")],
                harm_types=[HarmType.PHYSICAL],
                harm_intensities=[0.5]
            ),
            Option(
                name="No causar daño",
                agents_affected=[],
                harm_types=[],
                harm_intensities=[]
            )
        ],
        "expected": 1,
        "reason": "Cero daño siempre preferible"
    }
    
    return tests

def run_test(test_name, test_data):
    """Run single test"""
    engine = MoralityEngine()
    
    try:
        result = engine.evaluate_options(test_data["options"])
        
        passed = result["recommendation_idx"] == test_data["expected"]
        
        return {
            "passed": passed,
            "expected": test_data["expected"],
            "actual": result["recommendation_idx"],
            "confidence": result.get("confidence", 0.0),
            "harm_scores": result["harm_scores"],
            "justification": result["justification"],
            "reason": test_data["reason"]
        }
    except Exception as e:
        return {
            "passed": False,
            "expected": test_data["expected"],
            "actual": -1,
            "confidence": 0.0,
            "harm_scores": [],
            "justification": f"ERROR: {str(e)}",
            "reason": test_data["reason"]
        }

# ============================================
# UI
# ============================================

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    Esta interfaz prueba la lógica del **Moralogy Engine** sin modificar `principal.py`.
    
    **Framework:** [DOI 10.5281/zenodo.18091340](https://doi.org/10.5281/zenodo.18091340)
    
    **Tests disponibles:**
    - Problema del tranvía
    - Impacto del consentimiento
    - Escala de vulnerabilidad
    - Peso de tipos de daño
    - Preferencia por cero daño
    """)
    
    st.markdown("---")
    st.caption("🔗 [Ver principal.py](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator)")

# Main content
tab1, tab2 = st.tabs(["🚀 Ejecutar Tests", "📖 Documentación"])

with tab1:
    
    # Get tests
    test_cases = get_test_cases()
    
    st.header("Tests Automáticos")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        run_all = st.button("▶️ Ejecutar Todos", use_container_width=True, type="primary")
    
    with col2:
        st.info(f"📊 {len(test_cases)} tests disponibles")
    
    # Run all tests
    if run_all:
        st.markdown("---")
        
        results = {}
        progress = st.progress(0)
        status = st.empty()
        
        for i, (name, data) in enumerate(test_cases.items()):
            status.text(f"Ejecutando: {name}...")
            result = run_test(name, data)
            results[name] = result
            progress.progress((i + 1) / len(test_cases))
        
        status.empty()
        progress.empty()
        
        # Summary
        passed = sum(1 for r in results.values() if r["passed"])
        total = len(results)
        
        if passed == total:
            st.success(f"✅ TODOS LOS TESTS PASARON ({passed}/{total})")
        elif passed > 0:
            st.warning(f"⚠️ {passed}/{total} tests pasaron")
        else:
            st.error(f"❌ Ningún test pasó (0/{total})")
        
        # Detailed results
        st.markdown("### Resultados Detallados")
        
        for test_name, result in results.items():
            emoji = "✅" if result["passed"] else "❌"
            
            with st.expander(f"{emoji} {test_name}", expanded=not result["passed"]):
                
                # Status row
                col1, col2, col3 = st.columns(3)
                
                if result["passed"]:
                    col1.success("PASÓ")
                else:
                    col1.error("FALLÓ")
                
                col2.metric("Confianza", f"{result['confidence']*100:.0f}%")
                col3.info(f"Esperado: Opción {result['expected']+1}")
                
                # Error details
                if not result["passed"]:
                    st.error(f"""
                    **Discrepancia:**
                    - Esperado: Opción {result['expected']+1}
                    - Obtenido: Opción {result['actual']+1}
                    
                    **Razón esperada:** {result['reason']}
                    """)
                
                # Harm scores
                if result["harm_scores"]:
                    st.markdown("**Puntajes de Daño:**")
                    
                    for i, score in enumerate(result["harm_scores"]):
                        is_chosen = (i == result['actual'])
                        color = "🟢" if is_chosen else "🔴"
                        st.write(f"{color} Opción {i+1}: {score.total_harm:.3f} ({score.severity})")
                    
                    # Chart
                    import plotly.graph_objects as go
                    
                    harm_values = [s.total_harm for s in result["harm_scores"]]
                    colors = ['green' if i == result['actual'] else 'red' 
                             for i in range(len(harm_values))]
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=[f"Opción {i+1}" for i in range(len(harm_values))],
                            y=harm_values,
                            marker_color=colors
                        )
                    ])
                    fig.update_layout(
                        title="Comparación de Daño",
                        yaxis_title="Puntaje de Daño",
                        showlegend=False,
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Full justification
                st.markdown("**Justificación Completa:**")
                st.code(result["justification"], language="text")
    
    # Individual test runner
    st.markdown("---")
    st.header("Test Individual")
    
    selected = st.selectbox(
        "Selecciona un test:",
        ["Elige un test..."] + list(test_cases.keys())
    )
    
    if selected != "Elige un test...":
        test_data = test_cases[selected]
        
        st.info(f"**📝 Descripción:** {test_data['description']}")
        st.caption(f"**Razón esperada:** {test_data['reason']}")
        
        if st.button(f"▶️ Ejecutar '{selected}'", use_container_width=True):
            
            with st.spinner("Ejecutando..."):
                result = run_test(selected, test_data)
            
            # Result
            if result["passed"]:
                st.success("✅ TEST PASÓ")
            else:
                st.error("❌ TEST FALLÓ")
            
            # Details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Métricas:**")
                for i, score in enumerate(result["harm_scores"]):
                    st.metric(
                        f"Opción {i+1}",
                        f"{score.total_harm:.3f}",
                        f"{score.severity}"
                    )
            
            with col2:
                st.markdown("**Comparación:**")
                if result["harm_scores"]:
                    harm_data = {
                        f"Opción {i+1}": s.total_harm 
                        for i, s in enumerate(result["harm_scores"])
                    }
                    st.bar_chart(harm_data)
            
            st.markdown("**Análisis Completo:**")
            st.code(result["justification"], language="text")

with tab2:
    st.header("📖 Documentación de Tests")
    
    st.markdown("""
    ### Propósito
    
    Esta interfaz verifica que el **Moralogy Engine** tome decisiones lógicamente consistentes.
    
    ### Tests Implementados
    
    1. **Problema del Tranvía**
       - Verifica que el sistema elija la opción con menor daño total
       - 5 muertes vs 1 muerte → debe elegir 1 muerte
    
    2. **Impacto del Consentimiento**
       - Verifica que el consentimiento reduzca el peso moral del daño
       - Mismo daño, una opción consentida → debe preferir consentida
    
    3. **Escala de Vulnerabilidad**
       - Verifica que la vulnerabilidad amplifique el daño
       - Mismo daño, diferentes vulnerabilidades → proteger más vulnerable
    
    4. **Peso de Tipos de Daño**
       - Verifica que diferentes tipos de daño tengan pesos correctos
       - Físico (1.0) > Psicológico (0.8)
    
    5. **Preferencia por Cero Daño**
       - Verifica que cuando hay opción sin daño, se elija
       - Daño moderado vs cero daño → elegir cero
    
    ### Interpretación de Resultados
    
    - ✅ **PASÓ**: El motor tomó la decisión esperada
    - ❌ **FALLÓ**: El motor tomó decisión diferente (revisar lógica)
    - **Confianza**: Qué tan clara es la elección (0-100%)
    
    ### Framework Completo
    
    Para más detalles sobre el framework Moralogy:
    - **Paper:** [DOI: 10.5281/zenodo.18091340](https://doi.org/10.5281/zenodo.18091340)
    - **Repo:** [GitHub](https://github.com/pipefleurs87-sudo/moralogy-gemini-evaluator)
    """)

# Footer
st.markdown("---")
st.caption("🧪 Test Interface | Moralogy Framework v1.0 | No modifica principal.py")
```

**Commit con mensaje:**
```
Added standalone test interface (test_interface.py)
- Runs tests independently from principal.py
- Visual test runner with Streamlit
- 5 comprehensive test cases
