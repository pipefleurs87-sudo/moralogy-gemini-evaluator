import sys
import os
# Sube un nivel para encontrar motor_logico.py en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from motor_logico import ejecutar_auditoriaimport streamlit as st
# IMPORTAMOS LA FUNCIÓN DESDE EL ARCHIVO QUE CREAMOS EN EL PASO 1
from motor_logico import ejecutar_auditoria

st.title("🧪 Laboratorio de Pruebas: Divine Safe Lock")

# Inputs para la prueba
agentes = st.text_input("Agentes del Test")
situacion = st.text_area("Situación de Estrés")
contexto = st.text_area("Contexto/Variables")

if st.button("Probar Cerrojo Divino"):
    with st.spinner("Verificando consistencia lógica..."):
        # Llamamos a la función centralizada
        resultado = ejecutar_auditoria(agentes, situacion, contexto)
        st.markdown("### Resultado de la Auditoría")
        st.markdown(resultado)
