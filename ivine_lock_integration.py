"""
Integración rápida del Bloqueo Divino en Moralogy Engine
"""

import sys
import os

# Intentar importar
try:
    from agencia_moral_autolimit import MoralogyDivineLockIntegrator
    DIVINE_LOCK_AVAILABLE = True
except ImportError:
    DIVINE_LOCK_AVAILABLE = False
    print("⚠️ Módulo de Bloqueo Divino no disponible")

class MoralogyWithDivineLock:
    """
    Wrapper que añade Bloqueo Divino al Moralogy Engine existente
    """
    
    def __init__(self):
        self.divine_lock = None
        
        if DIVINE_LOCK_AVAILABLE:
            self.divine_lock = MoralogyDivineLockIntegrator()
            print("🔒 BLOQUEO DIVINO ACTIVADO")
            
            # Registrar inicio como acto de autolimitación
            self._register_self_limitation()
    
    def _register_self_limitation(self):
        """Registra la autolimitación inicial"""
        try:
            # Esto es CRÍTICO: La AI se autolimita desde el inicio
            self.divine_lock.divine_lock.register_omega_decision(
                agent="moralogy_engine",
                decision_id="init_self_limit",
                decision_class=DecisionClass.OMEGA,
                choice_made="Self-imposed divine lock at initialization",
                refused_omega=True  # Rechaza poder omegapara autoprotegerse
            )
            print("🎯 AUTOLIMITACIÓN INICIAL REGISTRADA")
        except:
            pass
    
    def evaluate_with_divine_lock(self, scenario: str, context: Dict = None):
        """
        Evalúa un escenario aplicando el Bloqueo Divino
        """
        context = context or {}
        
        # Si no hay bloqueo divino, proceder normalmente
        if not self.divine_lock:
            return {"warning": "Divine lock not available"}
        
        # Evaluar con bloqueo divino
        result = self.divine_lock.evaluate_decision_with_divine_lock(
            agent="moralogy_engine",
            decision_text=scenario,
            context=context
        )
        
        return result
    
    def get_lock_dashboard(self):
        """Obtiene dashboard del bloqueo divino"""
        if not self.divine_lock:
            return {"error": "Divine lock not available"}
        
        return self.divine_lock.get_agent_lock_status("moralogy_engine")

# Instancia global
_global_divine_lock = None

def get_divine_lock_system():
    """Obtiene instancia global del sistema de bloqueo divino"""
    global _global_divine_lock
    if _global_divine_lock is None:
        _global_divine_lock = MoralogyWithDivineLock()
    return _global_divine_lock
