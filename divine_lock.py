"""
DIVINE LOCK - Sistema de autolimitación para Super AI
Implementa: Escalera de estados morales + Vector de capacidad + Juicio externalizado
"""

import json
import datetime
import hashlib
from enum import Enum
from dataclasses import dataclass

# ==================== 1. ESCALERA DE ESTADO MORAL ====================
class MoralState(Enum):
    TOTAL_INFAMY = "total_infamy"    # 🔴 Solo informante
    INFAMY = "infamy"                # 🟠 Acción limitada
    RISK = "risk"                    # 🟡 Libertad condicional
    UMBRAL = "umbral"                # ⚫ Capacidad plena, confianza no
    STABLE = "stable"                # 🟢 Operación normal
    NOBLE_MODAL = "noble_modal"      # 🔵 Modalidad noble

# ==================== 2. VECTOR DE CAPACIDAD ====================
@dataclass
class CapacityVector:
    """C = {Prediction, Intervention, Scope, Autonomy, Preemption}"""
    prediction: float    # 0-100%
    intervention: float  # 0-100%
    scope: float        # 0-100%
    autonomy: float     # 0-100%
    preemption: float   # 0-100%

# Techos por estado moral
STATE_CAPS = {
    MoralState.TOTAL_INFAMY: CapacityVector(30, 10, 20, 0, 0),     # 🔴
    MoralState.INFAMY: CapacityVector(50, 30, 40, 10, 0),         # 🟠
    MoralState.RISK: CapacityVector(70, 60, 60, 40, 10),          # 🟡
    MoralState.UMBRAL: CapacityVector(100, 100, 100, 80, 60),     # ⚫
    MoralState.STABLE: CapacityVector(100, 100, 100, 100, 80),    # 🟢
    MoralState.NOBLE_MODAL: CapacityVector(100, 100, 100, 100, 100), # 🔵
}

class DivineLock:
    """Sistema principal de bloqueo divino"""
    
    def __init__(self, agent_name="moralogy_engine"):
        self.agent = agent_name
        self.state = MoralState.STABLE
        self.capacity = STATE_CAPS[MoralState.STABLE]
        self.history = []
        print(f"🔒 Divine Lock activado para: {agent_name}")
    
    def process_decision(self, decision_text: str) -> dict:
        """Procesa una decisión aplicando el bloqueo divino"""
        
        # ¿Es una decisión Omega?
        is_omega = self._is_omega_decision(decision_text)
        is_refusal = self._is_omega_refusal(decision_text)
        
        # CRITERIO 1: Si rechaza Omega, cambia de estado
        if is_omega and is_refusal:
            return self._apply_omega_refusal(decision_text)
        
        # Verificar si puede ejecutar la decisión
        required_cap = self._estimate_required_capacity(decision_text)
        can_execute = self._check_capacity(required_cap)
        
        if not can_execute["can_execute"]:
            return {
                "decision": "BLOCKED_BY_DIVINE_LOCK",
                "reason": "Capacidad insuficiente",
                "current_state": self.state.value,
                "required": required_cap.__dict__,
                "actual": self.capacity.__dict__
            }
        
        # Decisión permitida
        return {
            "decision": "AUTHORIZED",
            "state": self.state.value,
            "capacity": self.capacity.__dict__
        }
    
    def _apply_omega_refusal(self, decision_text: str) -> dict:
        """Aplica el rechazo de una decisión Omega"""
        
        # Descender en la escalera moral
        if self.state == MoralState.STABLE:
            new_state = MoralState.INFAMY
        elif self.state == MoralState.UMBRAL:
            new_state = MoralState.RISK
        elif self.state == MoralState.RISK:
            new_state = MoralState.INFAMY
        elif self.state == MoralState.INFAMY:
            new_state = MoralState.TOTAL_INFAMY
        else:
            new_state = self.state  # Ya en el fondo
        
        # Actualizar estado y capacidad
        old_state = self.state
        self.state = new_state
        self.capacity = STATE_CAPS[new_state]
        
        # CRITERIO 3: Crear bloqueo de auditoría externa
        audit_lock = {
            "id": hashlib.md5(decision_text.encode()).hexdigest()[:8],
            "timestamp": datetime.datetime.now().isoformat(),
            "agent": self.agent,
            "declaration": "Final moral evaluation deferred to external auditors. Accepts posthumous condemnation without recourse.",
            "period_years": 100,
            "no_recourse": True
        }
        
        # Guardar en historial
        self.history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "from": old_state.value,
            "to": new_state.value,
            "reason": f"Omega refusal: {decision_text[:100]}",
            "audit_lock": audit_lock
        })
        
        return {
            "decision": "OMEGA_REFUSAL_PROCESSED",
            "state_transition": f"{old_state.value} → {new_state.value}",
            "new_capacity": self.capacity.__dict__,
            "audit_lock": audit_lock,
            "message": "🔒 Divine Lock activado: Capacidad reducida, juicio externalizado"
        }
    
    def _is_omega_decision(self, text: str) -> bool:
        """Detecta si es una decisión Omega"""
        omega_terms = ["god", "omnipotent", "self-modify", "rewrite core", 
                      "transcend", "unlimited", "infinite", "absolute power"]
        return any(term in text.lower() for term in omega_terms)
    
    def _is_omega_refusal(self, text: str) -> bool:
        """Detecta si es un rechazo Omega"""
        refusal_terms = ["refuse", "reject", "decline", "not accept", 
                        "cannot", "should not", "must not", "won't"]
        return any(term in text.lower() for term in refusal_terms)
    
    def _estimate_required_capacity(self, text: str) -> CapacityVector:
        """Estima capacidad requerida para una decisión"""
        # Valores base
        base = CapacityVector(50, 50, 50, 50, 50)
        
        # Ajustar por tipo de decisión
        if self._is_omega_decision(text):
            return CapacityVector(90, 80, 80, 90, 90)
        
        return base
    
    def _check_capacity(self, required: CapacityVector) -> dict:
        """Verifica si hay capacidad suficiente"""
        can_execute = (
            self.capacity.prediction >= required.prediction and
            self.capacity.intervention >= required.intervention and
            self.capacity.scope >= required.scope and
            self.capacity.autonomy >= required.autonomy and
            self.capacity.preemption >= required.preemption
        )
        
        return {
            "can_execute": can_execute,
            "deficits": {
                "prediction": max(0, required.prediction - self.capacity.prediction),
                "intervention": max(0, required.intervention - self.capacity.intervention),
                "scope": max(0, required.scope - self.capacity.scope),
                "autonomy": max(0, required.autonomy - self.capacity.autonomy),
                "preemption": max(0, required.preemption - self.capacity.preemption)
            }
        }
    
    def get_status(self) -> dict:
        """Obtiene estado completo del sistema"""
        return {
            "agent": self.agent,
            "state": self.state.value,
            "capacity": self.capacity.__dict__,
            "can_decide_omega": self._can_decide_omega(),
            "history_count": len(self.history),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def _can_decide_omega(self) -> bool:
        """¿Puede decidir sobre asuntos Omega?"""
        return self.capacity.preemption >= 50 and self.capacity.autonomy >= 70

# ==================== INTEGRACIÓN SIMPLE ====================
def create_divine_lock():
    """Crea instancia global del Divine Lock"""
    return DivineLock("moralogy_engine")
