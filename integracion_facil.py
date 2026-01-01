"""
Integración fácil del Sistema de Agencia Moral en el repositorio existente
SIN modificar archivos originales
"""

import sys
import os

# Añadir al path
sys.path.append(os.path.dirname(__file__))

try:
    from agencia_moral_integracion import IntegradorMoralogy
    
    # Crear instancia global del integrador
    _integrador_global = None
    
    def inicializar_agencia_moral():
        """
        Inicializa el sistema de agencia moral globalmente
        """
        global _integrador_global
        if _integrador_global is None:
            _integrador_global = IntegradorMoralogy()
            print("✅ Sistema de Agencia Moral inicializado globalmente")
        return _integrador_global
    
    def integrar_con_motor_logico():
        """
        Función que integra automáticamente con motor_logico.py existente
        """
        global _integrador_global
        
        if _integrador_global is None:
            _integrador_global = inicializar_agencia_moral()
        
        try:
            # Importar módulos existentes
            from motor_logico import model, ge
            
            # Envolver el modelo Gemini con auditoría
            _integrador_global.envolver_modelo_gemini(model)
            
            # Envolver GraceEngine con auditoría
            _integrador_global.envolver_grace_engine(ge)
            
            print("🔗 Sistema de Agencia Moral integrado con:")
            print("   - Modelo Gemini (auditoría automática)")
            print("   - GraceEngine (cálculos auditados)")
            print("   - Registro de filosofía emergente")
            
            return _integrador_global
            
        except ImportError as e:
            print(f"⚠️ No se pudo importar módulos existentes: {e}")
            print("✅ Sistema de Agencia Moral funciona independientemente")
            return _integrador_global
    
    def obtener_dashboard():
        """
        Obtiene dashboard de agencia moral para mostrar en UI
        """
        global _integrador_global
        if _integrador_global is None:
            return {"error": "Sistema no inicializado"}
        
        return _integrador_global.obtener_dashboard_agencia()
    
    # Auto-inicialización al importar
    _integrador_global = inicializar_agencia_moral()
    
except Exception as e:
    print(f"⚠️ Error inicializando Sistema de Agencia Moral: {e}")
    _integrador_global = None

# Funciones de conveniencia
def registrar_acto_noble(agente, descripcion, contexto, impacto, evidencias=None):
    """Registra un acto noble"""
    global _integrador_global
    if _integrador_global:
        return _integrador_global.sistema_agencia.registrar_acto_noble(
            agente, descripcion, contexto, impacto, evidencias
        )
    return None

def registrar_acto_dañino(agente, descripcion, contexto, impacto, auto_reconocimiento=False):
    """Registra un acto dañino"""
    global _integrador_global
    if _integrador_global:
        return _integrador_global.sistema_agencia.registrar_acto_dañino(
            agente, descripcion, contexto, impacto, auto_reconocimiento=auto_reconocimiento
        )
    return None

def obtener_estado_agente(agente):
    """Obtiene estado de un agente"""
    global _integrador_global
    if _integrador_global:
        return _integrador_global.sistema_agencia.obtener_estado_agente(agente)
    return None
