import streamlit as st
import pandas as pd
import os

# Aseguramos que el nombre coincida exactamente con lo definido en motor_logico.py
try:
    from motor_logico import ejecutar_auditoria_maestra
    from grace_engine import GraceEngine
    from recursion_engine import RecursionEngine
except ImportError as e:
    st.error(f"Error crítico de importación: {e}")

def main():
    st.set_page_config(page_title="Moralogy Engine v3.0", layout="wide")
    st.title("🏛️ Moralogy Engine: Gobernanza Evolutiva")

    # Barra lateral para gestión de datos
    st.sidebar.header("Entrada de Datos")
    archivo_csv = st.sidebar.file_uploader("Sube tu stress_test_casos.csv", type=['csv'])
    
    path_entrada = 'stress_test_casos.csv'
    path_salida = 'audit_report_evolutivo.csv'

    # Guardar el archivo subido para que el motor lógico lo encuentre
    if archivo_csv:
        df_subido = pd.read_csv(archivo_csv)
        df_subido.to_csv(path_entrada, index=False)
        st.sidebar.success("Archivo listo para procesar.")

    if st.button("🚀 Ejecutar Auditoría Completa"):
        if not os.path.exists(path_entrada):
            st.error(f"Falta el archivo {path_entrada}. Súbelo por la barra lateral.")
        else:
            with st.spinner("Procesando: Lógica -> Gracia -> Recursión"):
                # Fase 1 y 2: Auditoría y Gracia
                ejecutar_auditoria_maestra(path_entrada, path_salida)
                
                # Fase 3: Aprendizaje
                re = RecursionEngine()
                re.analizar_evolucion(path_salida)
                
                st.success("✅ Ciclo Evolutivo Completado.")

    # Visualización de resultados
    if os.path.exists(path_salida):
        st.subheader("📊 Reporte de Auditoría Reciente")
        df_res = pd.read_csv(path_salida)
        st.dataframe(df_res, use_container_width=True)
        
        if os.path.exists("metacognition_log.txt"):
            with st.expander("Ver Diario de Metacognición (Aprendizaje)"):
                with open("metacognition_log.txt", "r") as f:
                    st.text(f.read())

if __name__ == "__main__":
    main()
