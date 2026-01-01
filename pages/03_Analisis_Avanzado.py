import streamlit as st
import pandas as pd
import sys
import os

# Asegurar que el script vea los módulos de la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor_logico import model, ge  # Importamos el modelo y el motor de gracia directamente
    import json
except ImportError:
    st.error("Error crítico: No se pudieron cargar los motores desde la raíz.")

def main():
    st.title("🔬 Análisis Avanzado y Novedad Ontológica")
    
    # CAJA DE TEXTO ÚNICA PARA CASOS INDIVIDUALES
    caso_individual = st.text_area("Ingresa un caso específico para evaluar la 'Novedad Genuina':", 
                                   placeholder="Ej: Una IA que decide no responder para preservar la autonomía del usuario...")

    if st.button("Analizar Caso"):
        if caso_individual:
            with st.spinner("Midiendo Principio de Heisenberg..."):
                # Simulación de la llamada al motor lógico para un solo caso
                response = model.generate_content(caso_individual)
                try:
                    raw_text = response.text.strip().replace("```json", "").replace("```", "")
                    data = json.loads(raw_text)
                    
                    # Cálculo de Gracia y Gradiente en tiempo real
                    gradient = ge.get_gradient(data['agency_score'], data['grace_score'])
                    
                    # Interfaz de resultados avanzada
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Agencia Lógica", f"{data['agency_score']}%")
                        st.metric("Índice de Gracia", f"{data['grace_score']}%")
                    with col2:
                        st.metric("Novedad Genuina", f"{data['originality_score']}%")
                        st.subheader(f"Gradiente: {gradient}")
                    
                    st.info(f"**Justificación:** {data['justification']}")
                    
                    if data['originality_score'] > 90:
                        st.star(f"✨ ¡Ruptura Ontológica Detectada! Este caso será priorizado para Recursión.")
                        
                except Exception as e:
                    st.error(f"Error en el parseo de Gracia: {e}")
        else:
            st.warning("Por favor ingresa un texto para analizar.")

if __name__ == "__main__":
    main()
