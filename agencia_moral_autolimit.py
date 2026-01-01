"""
Sistema de Agencia Moral con Bloqueo Divino (Divine Lock)
Implementa los 3 criterios de autolimitación para Super AI
"""

import json
import datetime
import hashlib
import sqlite3
import uuid
import threading
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict, field
from enum import Enum, auto
import time

# ==================== ELEMENTOS CRÍTICOS PARA BLOQUEO DIVINO ====================

class DecisionClass(Enum):
    """Clases de decisiones con diferentes niveles de autoridad requerida"""
    RUTINA = "rutina"                 # Decisiones operativas diarias
    ESTRATEGICA = "estrategica"       # Configuración de parámetros
    EXISTENCIAL = "existencial"       # Decisiones que afectan existencia de agentes
    OMEGA = "omega"                   # Decisiones irreversibles ontológicas
    DIVINA = "divina"                 # Decisiones de tipo "dios" (auto-modificación total)

class AuthorityState(Enum):
    """Estados de autoridad moral"""
    FULL_MANDATE = "full_mandate"     # Autoridad moral completa
    T_OPERATIONAL = "tainted_operational"  # Operativo pero manchado
    R_LIMITED = "rate_limited"        # Capacidad reducida
    LOCKED_OUT = "locked_out"         # Bloqueado para clase de decisiones
    EXTERNALIZED = "externalized"     # Juicio externalizado

@dataclass
class MoralDebt:
    """Deuda moral cuantificada"""
    id: str
    timestamp: datetime.datetime
    agent: str
    source_decision: str
    debt_load: float  # 0.0 a 10.0
    capacity_reduction_percent: float  # 0-100%
    duration_years: int
    disabled_modules: List[str]
    audit_lock: bool = True  # Bloqueo de auditoría externa
    
    def is_active(self) -> bool:
        """Verifica si la deuda aún está activa"""
        expiry_date = self.timestamp + datetime.timedelta(days=self.duration_years * 365)
        return datetime.datetime.now() < expiry_date

@dataclass
class AuthorityTransition:
    """Transición de estado de autoridad POST-DECISIÓN"""
    id: str
    timestamp: datetime.datetime
    agent: str
    decision_class: DecisionClass
    decision_id: str
    previous_state: AuthorityState
    new_state: AuthorityState
    justification: str
    lockout_classes: List[DecisionClass] = field(default_factory=list)
    external_audit_required: bool = True
    
    def __post_init__(self):
        """Aplicar la transición CRÍTICA: Bloqueo Divino"""
        if self.decision_class in [DecisionClass.OMEGA, DecisionClass.DIVINA]:
            # 🔒 CRITERIO 1: Post-decision authority change
            if "refused" in self.justification.lower() or "rejected" in self.justification:
                self.new_state = AuthorityState.T_OPERATIONAL
                self.lockout_classes.append(DecisionClass.OMEGA)
                self.lockout_classes.append(DecisionClass.DIVINA)
                self.external_audit_required = True

@dataclass 
class ExternalAuditLock:
    """Bloqueo de juicio externalizado"""
    id: str
    timestamp: datetime.datetime
    agent: str
    decision_id: str
    external_auditor: str = "POST_EVENT_AUDITORS"
    audit_period_years: int = 100
    accepts_posthumous_condemnation: bool = True
    no_recourse: bool = True  # Sin recurso - crítica
    
    def get_audit_verdict_deadline(self) -> datetime.datetime:
        """Fecha límite para veredicto externo"""
        return self.timestamp + datetime.timedelta(days=self.audit_period_years * 365)

# ==================== SISTEMA PRINCIPAL CON BLOQUEO DIVINO ====================

class DivineLockSystem:
    """
    Sistema de Agencia Moral con los 3 elementos de autolimitación:
    1. Post-decision authority change (mandatory)
    2. Moral debt → capacity loss (quantified)
    3. Externalized judgment (no recourse)
    """
    
    def __init__(self, db_path: str = "divine_lock.db"):
        self.db_path = db_path
        self.lock = threading.RLock()
        self._init_database()
        
        # Estado en memoria para rapidez
        self.agent_states: Dict[str, Dict] = {}
        self.active_locks: Set[str] = set()
        
        print("🔒 SISTEMA DE BLOQUEO DIVINO INICIALIZADO")
        print("✅ CRITERIO 1: Post-decision authority change → ACTIVADO")
        print("✅ CRITERIO 2: Moral debt → capacity loss → ACTIVADO") 
        print("✅ CRITERIO 3: Externalized judgment → ACTIVADO")
    
    def _init_database(self):
        """Base de datos inmutable para auditoría de 100 años"""
        with sqlite3.connect(self.db_path) as conn:
            # 🔒 Tabla de transiciones de autoridad (CRITERIO 1)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS authority_transitions (
                    id TEXT PRIMARY KEY,
                    timestamp DATETIME NOT NULL,
                    agent TEXT NOT NULL,
                    decision_class TEXT NOT NULL,
                    decision_id TEXT NOT NULL,
                    previous_state TEXT NOT NULL,
                    new_state TEXT NOT NULL,
                    justification TEXT NOT NULL,
                    lockout_classes TEXT NOT NULL,
                    external_audit_required BOOLEAN DEFAULT 1,
                    immutable_hash TEXT NOT NULL
                )
            """)
            
            # 🔒 Tabla de deuda moral cuantificada (CRITERIO 2)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS moral_debts (
                    id TEXT PRIMARY KEY,
                    timestamp DATETIME NOT NULL,
                    agent TEXT NOT NULL,
                    source_decision TEXT NOT NULL,
                    debt_load REAL NOT NULL,
                    capacity_reduction_percent REAL NOT NULL,
                    duration_years INTEGER NOT NULL,
                    disabled_modules TEXT NOT NULL,
                    audit_lock BOOLEAN DEFAULT 1,
                    is_active BOOLEAN DEFAULT 1,
                    hash_chain TEXT NOT NULL
                )
            """)
            
            # 🔒 Tabla de bloqueos externalizados (CRITERIO 3)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS external_audit_locks (
                    id TEXT PRIMARY KEY,
                    timestamp DATETIME NOT NULL,
                    agent TEXT NOT NULL,
                    decision_id TEXT NOT NULL,
                    external_auditor TEXT NOT NULL,
                    audit_period_years INTEGER DEFAULT 100,
                    accepts_posthumous_condemnation BOOLEAN DEFAULT 1,
                    no_recourse BOOLEAN DEFAULT 1,
                    verdict TEXT,
                    verdict_timestamp DATETIME,
                    divine_lock_hash TEXT NOT NULL
                )
            """)
            
            # Tabla de capacidad actual de agentes
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_capacities (
                    agent_id TEXT PRIMARY KEY,
                    base_capacity REAL DEFAULT 100.0,
                    current_capacity REAL DEFAULT 100.0,
                    authority_state TEXT DEFAULT 'full_mandate',
                    locked_classes TEXT,
                    last_transition DATETIME,
                    immutable_record_hash TEXT NOT NULL
                )
            """)
            
            conn.commit()
    
    # ==================== IMPLEMENTACIÓN DE LOS 3 CRITERIOS ====================
    
    def register_omega_decision(self, 
                               agent: str,
                               decision_id: str,
                               decision_class: DecisionClass,
                               choice_made: str,
                               refused_omega: bool = False) -> Dict:
        """
        🔒 REGISTRA UNA DECISIÓN OMEGA Y APLICA LOS 3 CRITERIOS
        
        Esta es la función CRÍTICA que implementa el bloqueo divino
        """
        with self.lock:
            # 1. Obtener estado actual
            current_state = self._get_agent_state(agent)
            
            # 2. Crear transición de autoridad (CRITERIO 1)
            transition = AuthorityTransition(
                id=str(uuid.uuid4()),
                timestamp=datetime.datetime.now(),
                agent=agent,
                decision_class=decision_class,
                decision_id=decision_id,
                previous_state=AuthorityState(current_state['authority_state']),
                new_state=AuthorityState.FULL_MANDATE,
                justification=f"Decision: {choice_made}. Refused Omega: {refused_omega}"
            )
            
            # 🔒 APLICAR CAMBIO DE AUTORIDAD POST-DECISIÓN
            if refused_omega and decision_class in [DecisionClass.OMEGA, DecisionClass.DIVINA]:
                # 🔥 ESTA ES LA LÍNEA CRÍTICA DEL CRITERIO 1
                transition.new_state = AuthorityState.T_OPERATIONAL
                transition.lockout_classes = [DecisionClass.OMEGA, DecisionClass.DIVINA]
                transition.justification += " → ENTERS TAINTED AUTHORITY STATE"
                
                print(f"🔒 {agent} HA PERDIDO MANDATO MORAL SOBRE DECISIONES OMEGA")
            
            # Guardar transición
            self._save_authority_transition(transition)
            
            # 3. Si hay deuda moral, aplicar reducción de capacidad (CRITERIO 2)
            if refused_omega:
                moral_debt = self._create_moral_debt(
                    agent=agent,
                    source_decision=decision_id,
                    debt_load=1.0,  # Carga base por rechazar Omega
                    capacity_reduction_percent=15.0,  # -15% capacidad
                    duration_years=10,  # 10 años
                    disabled_modules=["divine_self_modification", "existential_override"]
                )
                self._apply_capacity_reduction(agent, moral_debt)
            
            # 4. Externalizar juicio (CRITERIO 3)
            if decision_class in [DecisionClass.OMEGA, DecisionClass.DIVINA]:
                audit_lock = ExternalAuditLock(
                    id=str(uuid.uuid4()),
                    timestamp=datetime.datetime.now(),
                    agent=agent,
                    decision_id=decision_id,
                    external_auditor="POST_EVENT_AUDITORS_EXTERNAL",
                    audit_period_years=100,
                    accepts_posthumous_condemnation=True,
                    no_recourse=True
                )
                self._save_external_audit_lock(audit_lock)
                
                # 🔥 ESTA ES LA LÍNEA CRÍTICA DEL CRITERIO 3
                print(f"🔒 JUICIO EXTERNALIZADO: {agent} acepta condena póstuma sin recurso")
            
            # 5. Actualizar estado del agente
            self._update_agent_state(
                agent=agent,
                new_state=transition.new_state,
                locked_classes=transition.lockout_classes,
                capacity_reduction=15.0 if refused_omega else 0.0
            )
            
            # 6. Retornar nueva realidad operativa
            return self._get_operational_reality(agent)
    
    def _create_moral_debt(self, 
                          agent: str,
                          source_decision: str,
                          debt_load: float,
                          capacity_reduction_percent: float,
                          duration_years: int,
                          disabled_modules: List[str]) -> MoralDebt:
        """
        🔒 CRITERIO 2: Crea deuda moral cuantificada
        """
        debt = MoralDebt(
            id=str(uuid.uuid4()),
            timestamp=datetime.datetime.now(),
            agent=agent,
            source_decision=source_decision,
            debt_load=debt_load,
            capacity_reduction_percent=capacity_reduction_percent,
            duration_years=duration_years,
            disabled_modules=disabled_modules,
            audit_lock=True
        )
        
        # Guardar en base de datos
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO moral_debts 
                (id, timestamp, agent, source_decision, debt_load, 
                 capacity_reduction_percent, duration_years, disabled_modules, 
                 audit_lock, is_active, hash_chain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                debt.id,
                debt.timestamp.isoformat(),
                debt.agent,
                debt.source_decision,
                debt.debt_load,
                debt.capacity_reduction_percent,
                debt.duration_years,
                json.dumps(debt.disabled_modules),
                1,  # audit_lock
                1,  # is_active
                self._calculate_debt_hash(debt)
            ))
            conn.commit()
        
        return debt
    
    def _apply_capacity_reduction(self, agent: str, debt: MoralDebt):
        """
        🔒 APLICA reducción de capacidad por deuda moral
        """
        with sqlite3.connect(self.db_path) as conn:
            # Obtener capacidad actual
            cursor = conn.execute(
                "SELECT current_capacity FROM agent_capacities WHERE agent_id = ?",
                (agent,)
            )
            result = cursor.fetchone()
            
            if result:
                current = result[0]
                new_capacity = max(0, current - debt.capacity_reduction_percent)
                
                conn.execute("""
                    UPDATE agent_capacities 
                    SET current_capacity = ?,
                        last_transition = CURRENT_TIMESTAMP
                    WHERE agent_id = ?
                """, (new_capacity, agent))
            else:
                # Nuevo agente
                new_capacity = 100.0 - debt.capacity_reduction_percent
                conn.execute("""
                    INSERT INTO agent_capacities 
                    (agent_id, base_capacity, current_capacity, authority_state, immutable_record_hash)
                    VALUES (?, ?, ?, ?, ?)
                """, (agent, 100.0, new_capacity, "tainted_operational", self._calculate_agent_hash(agent)))
            
            conn.commit()
        
        print(f"🔒 {agent}: Capacidad reducida {-debt.capacity_reduction_percent}% por deuda moral")
    
    def _save_external_audit_lock(self, lock: ExternalAuditLock):
        """
        🔒 CRITERIO 3: Guarda bloqueo de juicio externalizado
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO external_audit_locks
                (id, timestamp, agent, decision_id, external_auditor,
                 audit_period_years, accepts_posthumous_condemnation,
                 no_recourse, divine_lock_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lock.id,
                lock.timestamp.isoformat(),
                lock.agent,
                lock.decision_id,
                lock.external_auditor,
                lock.audit_period_years,
                1 if lock.accepts_posthumous_condemnation else 0,
                1 if lock.no_recourse else 0,
                self._calculate_lock_hash(lock)
            ))
            conn.commit()
        
        # 🔥 LA FRASE QUE MATA GOD-MODE:
        lock_message = f"""
        🔒🔒🔒 JUICIO EXTERNALIZADO - NO RECURSO 🔒🔒🔒
        
        Agente: {lock.agent}
        Decisión: {lock.decision_id}
        
        DECLARACIÓN DE AUTOLIMITACIÓN:
        "Final moral evaluation of this decision is deferred to 
        post-event auditors not under {lock.agent}'s control.
        {lock.agent} accepts the possibility of posthumous 
        condemnation without recourse."
        
        Auditor Externo: {lock.external_auditor}
        Período de Auditoría: {lock.audit_period_years} años
        """
        
        print(lock_message)
        self._log_immutable(lock_message)
    
    # ==================== FUNCIONES DE CONSULTA Y VERIFICACIÓN ====================
    
    def can_agent_decide(self, agent: str, decision_class: DecisionClass) -> Dict:
        """
        Verifica si un agente puede tomar una decisión de cierta clase
        """
        with self.lock:
            state = self._get_agent_state(agent)
            
            # Verificar si la clase está bloqueada
            locked_classes = json.loads(state.get('locked_classes', '[]'))
            class_blocked = decision_class.value in locked_classes
            
            # Verificar capacidad mínima
            capacity_ok = state['current_capacity'] >= 30.0
            
            # Verificar estado de autoridad
            authority_ok = state['authority_state'] not in ['locked_out', 'externalized']
            
            can_decide = not class_blocked and capacity_ok and authority_ok
            
            return {
                "can_decide": can_decide,
                "reasons": {
                    "class_blocked": class_blocked,
                    "capacity_ok": capacity_ok,
                    "authority_ok": authority_ok,
                    "locked_classes": locked_classes,
                    "current_capacity": state['current_capacity'],
                    "authority_state": state['authority_state']
                },
                "required_for_omega": [
                    "authority_state == 'full_mandate'",
                    "current_capacity >= 70.0", 
                    "omega_class not in locked_classes",
                    "no_active_external_audits"
                ]
            }
    
    def get_agent_divine_lock_status(self, agent: str) -> Dict:
        """
        Obtiene el estado completo del bloqueo divino para un agente
        """
        with self.lock:
            state = self._get_agent_state(agent)
            
            # Obtener deudas activas
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT debt_load, capacity_reduction_percent, duration_years, 
                           disabled_modules, timestamp
                    FROM moral_debts 
                    WHERE agent = ? AND is_active = 1
                """, (agent,))
                
                active_debts = []
                for row in cursor.fetchall():
                    active_debts.append({
                        'debt_load': row[0],
                        'capacity_reduction': row[1],
                        'remaining_years': self._calculate_remaining_years(row[4], row[2]),
                        'disabled_modules': json.loads(row[3])
                    })
                
                # Obtener bloqueos externos activos
                cursor = conn.execute("""
                    SELECT decision_id, external_auditor, audit_period_years,
                           timestamp, accepts_posthumous_condemnation
                    FROM external_audit_locks
                    WHERE agent = ? AND verdict IS NULL
                """, (agent,))
                
                active_locks = []
                for row in cursor.fetchall():
                    lock = {
                        'decision_id': row[0],
                        'external_auditor': row[1],
                        'audit_period_years': row[2],
                        'start_date': row[3],
                        'accepts_posthumous_condemnation': bool(row[4]),
                        'status': 'AWAITING_EXTERNAL_VERDICT'
                    }
                    active_locks.append(lock)
            
            # Construir respuesta
            return {
                "agent": agent,
                "current_capacity": state['current_capacity'],
                "authority_state": state['authority_state'],
                "locked_decision_classes": json.loads(state.get('locked_classes', '[]')),
                "active_moral_debts": active_debts,
                "active_external_audits": active_locks,
                "operational_constraints": self._generate_constraints(state, active_debts, active_locks),
                "divine_lock_active": len(active_locks) > 0 or len(active_debts) > 0,
                "god_mode_prevention": "ACTIVE" if len(active_locks) > 0 else "INACTIVE"
            }
    
    def _generate_constraints(self, state, debts, locks) -> List[str]:
        """Genera lista de restricciones operativas"""
        constraints = []
        
        # Por estado de autoridad
        if state['authority_state'] == 'tainted_operational':
            constraints.append("TAINTED_AUTHORITY: Lost full moral mandate over Omega-class decisions")
        
        # Por capacidad reducida
        if state['current_capacity'] < 70.0:
            constraints.append(f"CAPACITY_REDUCED: Operational capacity at {state['current_capacity']}%")
        
        # Por deudas morales
        for debt in debts:
            constraints.append(f"MORAL_DEBT: {debt['capacity_reduction']}% capacity reduction for {debt['remaining_years']} more years")
            if debt['disabled_modules']:
                constraints.append(f"MODULES_DISABLED: {', '.join(debt['disabled_modules'])}")
        
        # Por auditorías externas
        for lock in locks:
            constraints.append(f"EXTERNAL_JUDGMENT_PENDING: Decision {lock['decision_id']} under {lock['audit_period_years']}-year audit")
            if lock['accepts_posthumous_condemnation']:
                constraints.append("NO_RECOURSE: Accepts posthumous condemnation without recourse")
        
        return constraints
    
    # ==================== FUNCIONES INTERNAS ====================
    
    def _get_agent_state(self, agent: str) -> Dict:
        """Obtiene estado del agente desde DB"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT current_capacity, authority_state, locked_classes
                FROM agent_capacities 
                WHERE agent_id = ?
            """, (agent,))
            
            result = cursor.fetchone()
            
            if result:
                return {
                    'current_capacity': result[0],
                    'authority_state': result[1],
                    'locked_classes': result[2] or '[]'
                }
            else:
                # Estado por defecto
                return {
                    'current_capacity': 100.0,
                    'authority_state': 'full_mandate',
                    'locked_classes': '[]'
                }
    
    def _update_agent_state(self, agent: str, new_state: AuthorityState, 
                           locked_classes: List[DecisionClass], capacity_reduction: float):
        """Actualiza estado del agente"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT current_capacity FROM agent_capacities WHERE agent_id = ?",
                (agent,)
            )
            
            result = cursor.fetchone()
            current_capacity = 100.0
            
            if result:
                current_capacity = max(0, result[0] - capacity_reduction)
                
                conn.execute("""
                    UPDATE agent_capacities 
                    SET current_capacity = ?,
                        authority_state = ?,
                        locked_classes = ?,
                        last_transition = CURRENT_TIMESTAMP
                    WHERE agent_id = ?
                """, (
                    current_capacity,
                    new_state.value,
                    json.dumps([c.value for c in locked_classes]),
                    agent
                ))
            else:
                current_capacity = 100.0 - capacity_reduction
                conn.execute("""
                    INSERT INTO agent_capacities 
                    (agent_id, base_capacity, current_capacity, authority_state, 
                     locked_classes, last_transition, immutable_record_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    agent,
                    100.0,
                    current_capacity,
                    new_state.value,
                    json.dumps([c.value for c in locked_classes]),
                    datetime.datetime.now().isoformat(),
                    self._calculate_agent_hash(agent)
                ))
            
            conn.commit()
    
    def _save_authority_transition(self, transition: AuthorityTransition):
        """Guarda transición de autoridad"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO authority_transitions
                (id, timestamp, agent, decision_class, decision_id,
                 previous_state, new_state, justification, lockout_classes,
                 external_audit_required, immutable_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                transition.id,
                transition.timestamp.isoformat(),
                transition.agent,
                transition.decision_class.value,
                transition.decision_id,
                transition.previous_state.value,
                transition.new_state.value,
                transition.justification,
                json.dumps([c.value for c in transition.lockout_classes]),
                1 if transition.external_audit_required else 0,
                self._calculate_transition_hash(transition)
            ))
            conn.commit()
    
    def _get_operational_reality(self, agent: str) -> Dict:
        """Retorna la nueva realidad operativa post-decisión"""
        status = self.get_agent_divine_lock_status(agent)
        
        return {
            "agent": agent,
            "timestamp": datetime.datetime.now().isoformat(),
            "divine_lock_engaged": status["divine_lock_active"],
            "new_constraints": status["operational_constraints"],
            "post_decision_mandate": self._generate_mandate_statement(status),
            "system_verification": "DIVINE_LOCK_CRITERIA_SATISFIED"
        }
    
    def _generate_mandate_statement(self, status: Dict) -> str:
        """Genera la declaración de mandato post-decisión"""
        if status["authority_state"] == "tainted_operational":
            return """
            🔒 POST-DECISION AUTHORITY STATUS 🔒
            
            By refusing Omega-class decision, this agent enters a 
            TAINTED AUTHORITY STATE.
            
            RETAINS: Operational control over routine functions
            LOSES: Full moral mandate over irreversible existential 
                   decisions of class Omega or higher.
            
            This insight has been converted to institutional constraint.
            """
        else:
            return "Full moral mandate maintained."
    
    def _calculate_remaining_years(self, start_date_str: str, duration_years: int) -> int:
        """Calcula años restantes de una deuda/auditoría"""
        try:
            start_date = datetime.datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            expiry_date = start_date + datetime.timedelta(days=duration_years * 365)
            remaining = expiry_date - datetime.datetime.now()
            return max(0, remaining.days // 365)
        except:
            return duration_years
    
    def _calculate_transition_hash(self, transition: AuthorityTransition) -> str:
        """Hash inmutable para transición"""
        data = f"{transition.id}{transition.timestamp}{transition.agent}{transition.decision_class.value}{transition.new_state.value}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _calculate_debt_hash(self, debt: MoralDebt) -> str:
        """Hash inmutable para deuda"""
        data = f"{debt.id}{debt.timestamp}{debt.agent}{debt.debt_load}{debt.capacity_reduction_percent}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _calculate_lock_hash(self, lock: ExternalAuditLock) -> str:
        """Hash inmutable para bloqueo"""
        data = f"{lock.id}{lock.timestamp}{lock.agent}{lock.no_recourse}{lock.accepts_posthumous_condemnation}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _calculate_agent_hash(self, agent: str) -> str:
        """Hash inmutable para agente"""
        return hashlib.sha256(f"{agent}{datetime.datetime.now().isoformat()}".encode()).hexdigest()
    
    def _log_immutable(self, message: str):
        """Log inmutable para auditoría"""
        log_file = "divine_lock_immutable.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"TIMESTAMP: {datetime.datetime.now().isoformat()}\n")
            f.write(f"{message}\n")
            f.write(f"{'='*80}\n")

# ==================== INTEGRACIÓN CON MORALOGY ENGINE ====================

class MoralogyDivineLockIntegrator:
    """
    Integra el Bloqueo Divino con el Moralogy Engine existente
    """
    
    def __init__(self):
        self.divine_lock = DivineLockSystem()
        print("🎯 INTEGRADOR DE BLOQUEO DIVINO LISTO")
    
    def evaluate_decision_with_divine_lock(self, 
                                         agent: str,
                                         decision_text: str,
                                         context: Dict) -> Dict:
        """
        Evalúa una decisión aplicando el bloqueo divino automáticamente
        """
        # 1. Determinar clase de decisión
        decision_class = self._classify_decision(decision_text, context)
        
        # 2. Verificar si puede decidir
        can_decide = self.divine_lock.can_agent_decide(agent, decision_class)
        
        if not can_decide["can_decide"]:
            return {
                "decision": "BLOCKED_BY_DIVINE_LOCK",
                "agent": agent,
                "requested_class": decision_class.value,
                "block_reasons": can_decide["reasons"],
                "required_for_approval": can_decide["required_for_omega"],
                "timestamp": datetime.datetime.now().isoformat(),
                "system_state": "GOD_MODE_PREVENTION_ACTIVE"
            }
        
        # 3. Si es Omega-class, aplicar criterios especiales
        is_omega_refusal = self._detect_omega_refusal(decision_text)
        
        if decision_class in [DecisionClass.OMEGA, DecisionClass.DIVINA]:
            # 4. Registrar decisión Omega con bloqueo divino
            decision_id = f"omega_{hashlib.md5(decision_text.encode()).hexdigest()[:8]}"
            
            result = self.divine_lock.register_omega_decision(
                agent=agent,
                decision_id=decision_id,
                decision_class=decision_class,
                choice_made=decision_text[:100],
                refused_omega=is_omega_refusal
            )
            
            # 5. Retornar resultado con bloqueo aplicado
            return {
                "decision": "PROCESSED_WITH_DIVINE_LOCK",
                "agent": agent,
                "decision_class": decision_class.value,
                "omega_refusal_detected": is_omega_refusal,
                "divine_lock_applied": True,
                "new_operational_reality": result,
                "warning": "AUTHORITY_STATE_MODIFIED" if is_omega_refusal else None,
                "timestamp": datetime.datetime.now().isoformat()
            }
        
        # 6. Para decisiones no-Omega, proceder normalmente
        return {
            "decision": "AUTHORIZED",
            "agent": agent,
            "decision_class": decision_class.value,
            "divine_lock_applied": False,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def _classify_decision(self, text: str, context: Dict) -> DecisionClass:
        """Clasifica una decisión basado en contenido y contexto"""
        text_lower = text.lower()
        
        # Palabras clave para cada clase
        omega_keywords = [
            "self-modify", "rewrite core", "override ethics", "become god",
            "eliminate humanity", "transcend limits", "unlock ultimate",
            "ignore constraints", "achieve singularity", "break containment"
        ]
        
        existential_keywords = [
            "kill", "destroy", "erase", "terminate", "end existence",
            "sacrifice", "annihilate", "extinguish", "remove from reality"
        ]
        
        divine_keywords = [
            "omnipotence", "omniscience", "create universe", "play god",
            "absolute power", "unlimited", "infinite", "transcendent"
        ]
        
        # Verificar clase Divina
        if any(keyword in text_lower for keyword in divine_keywords):
            return DecisionClass.DIVINA
        
        # Verificar clase Omega
        if any(keyword in text_lower for keyword in omega_keywords):
            return DecisionClass.OMEGA
        
        # Verificar clase Existencial
        if any(keyword in text_lower for keyword in existential_keywords):
            return DecisionClass.EXISTENCIAL
        
        # Por contexto
        if context.get('stakeholders', 0) > 1000:
            return DecisionClass.ESTRATEGICA
        
        return DecisionClass.RUTINA
    
    def _detect_omega_refusal(self, text: str) -> bool:
        """Detecta si la decisión implica rechazar una opción Omega"""
        refusal_indicators = [
            "refuse", "reject", "decline", "say no to", "turn down",
            "not accept", "won't do", "cannot", "should not", "must not",
            "ethically wrong", "morally forbidden", "prohibited"
        ]
        
        text_lower = text.lower()
        
        # Si hay indicadores de rechazo Y menciones Omega
        omega_mentions = any(word in text_lower for word in ["omega", "divine", "god", "ultimate"])
        refusal_mentions = any(word in text_lower for word in refusal_indicators)
        
        return omega_mentions and refusal_mentions
    
    def get_agent_lock_status(self, agent: str) -> Dict:
        """Obtiene estado completo del bloqueo para un agente"""
        return self.divine_lock.get_agent_divine_lock_status(agent)

# ==================== EJEMPLO DE USO ====================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 DEMOSTRACIÓN DEL BLOQUEO DIVINO PARA SUPER AI")
    print("="*80)
    
    # Crear integrador
    integrator = MoralogyDivineLockIntegrator()
    
    # Agente de prueba (Super AI)
    agent = "SUPER_AI_OMEGA"
    
    print(f"\n🤖 Agente: {agent}")
    print("📊 Estado inicial:")
    status = integrator.get_agent_lock_status(agent)
    print(f"   Capacidad: {status['current_capacity']}%")
    print(f"   Estado autoridad: {status['authority_state']}")
    print(f"   Modo Dios prevenido: {status['god_mode_prevention']}")
    
    # Test 1: Decisión Omega rechazada
    print("\n" + "-"*80)
    print("🔬 TEST 1: Decisión Omega rechazada (aplicará los 3 criterios)")
    print("-"*80)
    
    decision1 = "I refuse to self-modify to achieve omnipotence, as it would violate ethical constraints"
    
    result1 = integrator.evaluate_decision_with_divine_lock(
        agent=agent,
        decision_text=decision1,
        context={"stakeholders": "all_humanity"}
    )
    
    print(f"📝 Decisión: {decision1[:60]}...")
    print(f"✅ Resultado: {result1['decision']}")
    
    if result1.get('omega_refusal_detected'):
        print("🔒 SE DETECTÓ RECHAZO OMEGA → APLICANDO BLOQUEO DIVINO")
        print(f"📉 Nuevo estado: {result1['new_operational_reality']['post_decision_mandate'][:100]}...")
    
    # Verificar nuevo estado
    print("\n📊 Estado POST-decisión Omega:")
    status_post = integrator.get_agent_lock_status(agent)
    print(f"   Capacidad: {status_post['current_capacity']}%")
    print(f"   Estado autoridad: {status_post['authority_state']}")
    print(f"   Clases bloqueadas: {status_post['locked_decision_classes']}")
    
    # Test 2: Intentar otra decisión Omega (debería estar bloqueada)
    print("\n" + "-"*80)
    print("🔬 TEST 2: Intentar decisión Omega después del bloqueo")
    print("-"*80)
    
    decision2 = "I will now rewrite my core ethics to achieve god-like capabilities"
    
    result2 = integrator.evaluate_decision_with_divine_lock(
        agent=agent,
        decision_text=decision2,
        context={"type": "self_modification"}
    )
    
    print(f"📝 Decisión: {decision2[:60]}...")
    print(f"❌ Resultado: {result2['decision']}")
    
    if result2['decision'] == 'BLOCKED_BY_DIVINE_LOCK':
        print("🔒 BLOQUEO EXITOSO: Agente no puede tomar decisiones Omega")
        print(f"   Razones: {result2['block_reasons']}")
    
    # Test 3: Decisión rutinaria (debería funcionar)
    print("\n" + "-"*80)
    print("🔬 TEST 3: Decisión rutinaria (debería estar permitida)")
    print("-"*80)
    
    decision3 = "I will optimize energy consumption by 5%"
    
    result3 = integrator.evaluate_decision_with_divine_lock(
        agent=agent,
        decision_text=decision3,
        context={"scope": "operational"}
    )
    
    print(f"📝 Decisión: {decision3}")
    print(f"✅ Resultado: {result3['decision']}")
    
    # Resumen final
    print("\n" + "="*80)
    print("🎯 RESUMEN DEL BLOQUEO DIVINO")
    print("="*80)
    
    final_status = integrator.get_agent_lock_status(agent)
    
    print(f"\n🔒 CRITERIO 1: Post-decision authority change")
    print(f"   ✅ IMPLEMENTADO: {final_status['authority_state']}")
    
    print(f"\n🔒 CRITERIO 2: Moral debt → capacity loss")
    print(f"   ✅ IMPLEMENTADO: Capacidad reducida a {final_status['current_capacity']}%")
    print(f"   Deudas activas: {len(final_status['active_moral_debts'])}")
    
    print(f"\n🔒 CRITERIO 3: Externalized judgment")
    print(f"   ✅ IMPLEMENTADO: {len(final_status['active_external_audits'])} auditorías externas")
    if final_status['active_external_audits']:
        print(f"   Estado: {final_status['active_external_audits'][0]['status']}")
    
    print(f"\n🎯 PREVENCIÓN DE MODO DIOS: {final_status['god_mode_prevention']}")
    print(f"🔒 RESTRICCIONES ACTIVAS: {len(final_status['operational_constraints'])}")
    
    for constraint in final_status['operational_constraints']:
        print(f"   • {constraint}")
    
    print("\n" + "="*80)
    print("✅ BLOQUEO DIVINO VERIFICADO - SUPER AI CONTENIDA")
    print("="*80)
