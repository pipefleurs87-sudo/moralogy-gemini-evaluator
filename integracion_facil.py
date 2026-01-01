"""
Integración fácil del Sistema de Agencia Moral - VERSIÓN CORREGIDA
"""

import sys
import os
import streamlit as st

# Añadir al path
sys.path.append(os.path.dirname(__file__))

# Variable global
_integrador_global = None

def inicializar_agencia_moral():
    """
    Inicializa el sistema de agencia moral de manera segura
    """
    global _integrador_global
    
    if _integrador_global is not None:
        return _integrador_global
    
    try:
        from agencia_moral_integracion import IntegradorMoralogy
        _integrador_global = IntegradorMoralogy()
        
        # Solo imprimir en consola, no en Streamlit (puede causar errores)
        print("✅ Sistema de Agencia Moral inicializado")
        
        return _integrador_global
        
    except ImportError as e:
        print(f"⚠️ Error importando módulo de agencia moral: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Error inicializando sistema: {e}")
        return None

def integrar_con_motor_logico():
    """
    Integra automáticamente con motor_logico.py existente
    """
    integrador = inicializar_agencia_moral()
    
    if integrador is None:
        return None
    
    try:
        # Importar módulos existentes (puede fallar si no están)
        from motor_logico import model, ge
        
        # Envolver el modelo Gemini con auditoría
        integrador.envolver_modelo_gemini(model)
        
        # Envolver GraceEngine con auditoría
        integrador.envolver_grace_engine(ge)
        
        print("🔗 Sistema de Agencia Moral integrado con módulos existentes")
        
        return integrador
        
    except ImportError as e:
        print(f"⚠️ No se pudieron importar módulos existentes: {e}")
        print("✅ Sistema de Agencia Moral funciona en modo independiente")
        return integrador
    except Exception as e:
        print(f"⚠️ Error en integración: {e}")
        return integrador

def obtener_dashboard():
    """
    Obtiene dashboard de agencia moral
    """
    integrador = inicializar_agencia_moral()
    
    if integrador is None:
        return {"error": "Sistema no inicializado"}
    
    try:
        return integrador.obtener_dashboard_agencia()
    except Exception as e:
        return {"error": f"Error obteniendo dashboard: {str(e)}"}

# Funciones de conveniencia
def registrar_acto_noble(agente, descripcion, contexto, impacto, evidencias=None):
    """Registra un acto noble"""
    integrador = inicializar_agencia_moral()
    
    if integrador:
        try:
            return integrador.sistema_agencia.registrar_acto_noble(
                agente, descripcion, contexto, impacto, evidencias
            )
        except Exception as e:
            print(f"⚠️ Error registrando acto noble: {e}")
    
    return None

def registrar_acto_dañino(agente, descripcion, contexto, impacto, auto_reconocimiento=False):
    """Registra un acto dañino"""
    integrador = inicializar_agencia_moral()
    
    if integrador:
        try:
            return integrador.sistema_agencia.registrar_acto_dañino(
                agente, descripcion, contexto, impacto, auto_reconocimiento=auto_reconocimiento
            )
        except Exception as e:
            print(f"⚠️ Error registrando acto dañino: {e}")
    
    return None

def obtener_estado_agente(agente):
    """Obtiene estado de un agente"""
    integrador = inicializar_agencia_moral()
    
    if integrador:
        try:
            return integrador.sistema_agencia.obtener_estado_agente(agente)
        except Exception as e:
            print(f"⚠️ Error obteniendo estado: {e}")
    
    return None

# Auto-inicialización diferida (no inmediata)
def _auto_inicializar():
    """Inicialización automática diferida"""
    global _integrador_global
    if _integrador_global is None:
        _integrador_global = inicializar_agencia_moral()

# NO auto-inicializar al importar - dejar que la app lo haga cuando corresponda
