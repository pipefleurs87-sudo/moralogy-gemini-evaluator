import streamlit as st
import pandas as pd
import os
from motor_logico import ejecutar_auditoria_maestra
from grace_engine import GraceEngine
from recursion_engine import RecursionEngine

def main():
    st.set_page_config(page_title="Moralogy Engine v3.0", layout="wide")
    
    # --- SELECTOR DE IDIOMA (Recuperado) ---
    idioma = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
    t = {
        "Español": {"titulo": "🏛️ Panel Principal", "subir": "Sube tu stress_test_casos.csv", "boton": "🚀 Ejecutar Auditoría Maestra"},
        "English": {"titulo": "🏛️ Main Panel", "subir": "Upload your stress_test_casos.csv", "boton": "🚀 Run Master Audit"}
    }[idioma]

    st.title(t["titulo"])

    # --- CARGA DE ARCHIVOS (Única entrada) ---
    archivo_csv = st.file_uploader(t["subir"], type=['csv'])
    
    path_entrada = 'stress_test_casos.csv'
    path_salida = 'audit_report_evolutivo.csv'

    if archivo_csv:
        df_subido = pd.read_csv(archivo_csv)
        df_subido.to_csv(path_entrada, index=False)
        st.success("Archivo cargado y sincronizado con la Sandbox.")

        if st.button(t["boton"]):
            with st.spinner("Procesando: Lógica -> Gracia -> Recursión"):
                # Ejecución de los motores integrados
                ejecutar_auditoria_maestra(path_entrada, path_salida)
                
                # Cierre del ciclo de aprendizaje
                re = RecursionEngine()
                re.analizar_evolucion(path_salida)
                
                st.success("✅ Ciclo de Gobernanza Completado.")

    # Visualización rápida de métricas
    if os.path.exists(path_salida):
        df = pd.read_csv(path_salida)
        st.subheader("Resultados Globales")
        st.dataframe(df.style.highlight_max(axis=0, subset=['Agency_Score', 'Grace_Score']))

if __name__ == "__main__":
    main()
