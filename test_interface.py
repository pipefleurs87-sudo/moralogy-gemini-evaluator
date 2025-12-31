"""
Interface de Tests para Moralogy Engine
Corre tests sin modificar principal.py

Uso: streamlit run test_interface.py
"""

import streamlit as st
import plotly.graph_objects as go  # MOVER AQUÍ (línea 8)
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
st.set_page_co
