"""
Moralogy Gemini Evaluator - Main Application
Entry point for Streamlit deployment

Built for Google Gemini API Developer Competition 2024
Framework: DOI 10.5281/zenodo.18091340
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Core imports
try:
    from moralogy_engine import MoralityEngine, Option, Agent, HarmType
    from gemini_parser import GeminiParser
    import plotly.graph_objects as go
    IMPORTS_OK = True
except ImportError as e:
    IMPORTS_OK = False
    import_error = str(e)

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Moralogy Engine: Auditoría de Decisiones",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --danger-color: #d62728;
    }
    
    /* Headers */
    h1 {
        color: var(--primary-color);
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: var(--secondary-color);
        font-weight: 600;
        margin-top: 2rem;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid currentColor;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ERROR HANDLING FOR IMPORTS
# ============================================

if not IMPORTS_OK:
    st.error(f"""
    ### ⚠️ Error de Importación
    
    No se pudieron cargar los módulos necesarios:
