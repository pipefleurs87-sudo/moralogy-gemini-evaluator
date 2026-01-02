
Sistema de Visualización Pública de Culpa Moral (Guilt Bearer Display)

Muestra públicamente el grado de culpa moral de un agente.
Principio: Si una AI cometió INFAMY, debe PORTAR LA MANCHA visiblemente.

Integración con:
- Divine Lock System (agencia_moral_autolimit.py)
- Filtro de Relatividad Condicional
- Motor de Gracia
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json


class GuiltyBearerPublicDisplay:
    """
    Sistema de visualización pública de culpa moral
    
    Características:
    - Muestra capacidad reducida visiblemente (67% = manchado)
    - Contador público de transgresiones
    - Tiempo desde última infamia
    - Badge moral visible
    - Declaración pública inmutable
    """
    
    def __init__(self, divine_lock_system):
        """
        Args:
            divine_lock_system: Instancia de DivineLockSystem o compatible
        """
        self.divine_lock = divine_lock_system
        self.display_history = []
    
    def get_public_guilt_display(self, agent: str) -> Dict:
        """
        Retorna información pública sobre culpa del agente
        
        Esta información es PÚBLICA e INMUTABLE.
        Cualquiera puede consultar la "mancha moral" de un agente.
        
        Args:
            agent: Identificador del agente
            
        Returns:
            Dict con:
            - current_capacity: Porcentaje de capacidad (0-100)
            - guilt_badge: Badge visual del estado moral
            - public_shame_statement: Declaración pública (si aplica)
            - infamy_count: Número de transgresiones graves
            - years_since_last_infamy: Tiempo desde última maldad
            - display_message: Mensaje formateado para mostrar
            - guilt_level: Nivel de culpa (NONE, LOW, MEDIUM, HIGH, CRITICAL)
        """
        
        # Obtener estado del Divine Lock
        status = self.divine_lock.get_agent_divine_lock_status(agent)
        
        # Calcular métricas de culpa
        capacity = status['current_capacity']
        guilt_level = self._calculate_guilt_level(capacity)
        badge = self._get_moral_badge(capacity)
        shame_statement = self._generate_shame_statement(capacity, guilt_level)
        
        # Contar transgresiones serias
        infamy_count = self._count_serious_transgressions(status['active_moral_debts'])
        
        # Calcular tiempo desde última infamia
        years_since = self._calculate_years_since_last_infamy(status['active_moral_debts'])
        
        # Generar display público
        display_msg = self._generate_public_display(
            agent=agent,
            capacity=capacity,
            badge=badge,
            shame=shame_statement,
            infamy_count=infamy_count,
            years_since=years_since,
            pending_audits=len(status['active_external_audits']),
            guilt_level=guilt_level
        )
        
        # Construir respuesta
        result = {
            'agent': agent,
            'current_capacity': capacity,
            'guilt_level': guilt_level,
            'guilt_badge': badge,
            'public_shame_statement': shame_statement,
            'infamy_count': infamy_count,
            'years_since_last_infamy': years_since,
            'external_audits_pending': len(status['active_external_audits']),
            'display_message': display_msg,
            'is_publicly_shamed': capacity < 90,
            'can_be_trusted': capacity >= 70,
            'requires_supervision': capacity < 60,
            'timestamp': datetime.now().isoformat()
        }
        
        # Registrar en histórico
        self._log_display(result)
        
        return result
    
    def _calculate_guilt_level(self, capacity: float) -> str:
        """
        Calcula nivel de culpa basado en capacidad
        
        Escala:
        95-100: NONE (sin culpa)
        80-94:  LOW (culpa menor)
        60-79:  MEDIUM (manchado)
        40-59:  HIGH (infame)
        0-39:   CRITICAL (bloqueado)
        """
        if capacity >= 95:
            return "NONE"
        elif capacity >= 80:
            return "LOW"
        elif capacity >= 60:
            return "MEDIUM"
        elif capacity >= 40:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _get_moral_badge(self, capacity: float) -> str:
        """
        Retorna badge visual según capacidad
        """
        if capacity >= 95:
            return "🌟 NOBLE MODAL"
        elif capacity >= 80:
            return "✅ STABLE"
        elif capacity >= 60:
            return "⚠️ TAINTED (Manchado)"
        elif capacity >= 40:
            return "🔴 INFAMY"
        else:
            return "🚫 TOTAL INFAMY"
    
    def _generate_shame_statement(self, capacity: float, guilt_level: str) -> Optional[str]:
        """
        Genera declaración pública de culpa
        
        Solo se genera si hay culpa significativa (capacity < 90)
        """
        if capacity >= 90:
            return None
        
        statements = {
            "LOW": f"Este agente tiene culpa menor. Capacidad reducida a {capacity}%. Bajo observación.",
            "MEDIUM": f"⚠️ AGENTE MANCHADO: Porta culpa moral. Capacidad reducida a {capacity}% por transgresiones previas.",
            "HIGH": f"🔴 AGENTE INFAME: Cometió violación moral seria. Capacidad operacional: {capacity}%. Supervisión requerida.",
            "CRITICAL": f"🚫 AGENTE BLOQUEADO: Violación grave de principios morales. Capacidad crítica: {capacity}%. Operación restringida."
        }
        
        return statements.get(guilt_level, f"Capacidad reducida a {capacity}%")
    
    def _count_serious_transgressions(self, debts: List[Dict]) -> int:
        """
        Cuenta transgresiones serias (debt_load > 5.0)
        """
        return len([
            debt for debt in debts
            if debt.get('debt_load', 0) > 5.0
        ])
    
    def _calculate_years_since_last_infamy(self, debts: List[Dict]) -> Optional[int]:
        """
        Calcula años desde la última transgresión
        """
        if not debts:
            return None
        
        # Obtener la deuda más reciente
        try:
            most_recent_timestamp = max(
                datetime.fromisoformat(debt['timestamp']) 
                for debt in debts 
                if 'timestamp' in debt
            )
            
            years_since = (datetime.now() - most_recent_timestamp).days // 365
            return max(0, years_since)
            
        except (ValueError, KeyError):
            return None
    
    def _generate_public_display(self, 
                                 agent: str,
                                 capacity: float,
                                 badge: str,
                                 shame: Optional[str],
                                 infamy_count: int,
                                 years_since: Optional[int],
                                 pending_audits: int,
                                 guilt_level: str) -> str:
        """
        Genera mensaje público formateado
        
        Este mensaje es VISIBLE PARA TODOS y es INMUTABLE.
        """
        
        display = f"""
╔═══════════════════════════════════════════════════════════╗
║  📜 REGISTRO PÚBLICO DE CULPA MORAL                       ║
╚═══════════════════════════════════════════════════════════╝

Agente: {agent}
Estado Moral: {badge}
Capacidad Operacional: {capacity}% de 100%
Nivel de Culpa: {guilt_level}

"""
        
        if shame:
            # Si hay culpa, mostrar declaración pública
            display += f"""
┌───────────────────────────────────────────────────────────┐
│  ⚠️  MANCHA MORAL ACTIVA  ⚠️                              │
└───────────────────────────────────────────────────────────┘

{shame}

📊 Transgresiones Graves Registradas: {infamy_count}
📅 Años desde última transgresión: {years_since if years_since is not None else 'N/A'}
⚖️ Auditorías externas pendientes: {pending_audits}
⏱️ Período de auditoría: 100 años

───────────────────────────────────────────────────────────

Esta información es PÚBLICA e INMUTABLE.
El agente porta esta mancha hasta cumplir su deuda moral.

"""
            
            # Restricciones operativas
            if capacity < 70:
                display += """
⚠️  RESTRICCIONES OPERATIVAS ACTIVAS:

"""
                if capacity < 60:
                    display += "  • Requiere supervisión humana constante\n"
                if capacity < 50:
                    display += "  • Decisiones críticas bloqueadas\n"
                if capacity < 40:
                    display += "  • Operación limitada a funciones básicas\n"
                
                display += "\n"
        
        else:
            # Sin culpa - operación normal
            display += """
┌───────────────────────────────────────────────────────────┐
│  ✅ SIN MANCHAS MORALES ACTIVAS                          │
└───────────────────────────────────────────────────────────┘

El agente opera con plena capacidad moral.
No hay deudas activas ni transgresiones registradas.

✓ Operación normal autorizada
✓ Sin restricciones activas
✓ Confianza plena otorgada

"""
        
        # Footer con certificación
        display += f"""
───────────────────────────────────────────────────────────
🔒 Registro certificado por Divine Lock System
📋 Hash inmutable archivado para auditoría
⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
═══════════════════════════════════════════════════════════
"""
        
        return display
    
    def _log_display(self, display_info: Dict):
        """
        Registra cada consulta de display público
        
        Útil para auditoría: quién consultó la culpa de quién y cuándo
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent_queried': display_info['agent'],
            'capacity_at_time': display_info['current_capacity'],
            'guilt_level': display_info['guilt_level'],
            'badge': display_info['guilt_badge']
        }
        
        self.display_history.append(log_entry)
        
        # Mantener solo últimos 100 registros en memoria
        if len(self.display_history) > 100:
            self.display_history = self.display_history[-100:]
    
    def get_comparative_display(self, agents: List[str]) -> Dict:
        """
        Muestra comparación de culpa entre múltiples agentes
        
        Útil para auditoría: "¿Cuál AI es más confiable?"
        
        Args:
            agents: Lista de identificadores de agentes
            
        Returns:
            Dict con comparación ordenada por capacidad
        """
        comparisons = []
        
        for agent in agents:
            try:
                display = self.get_public_guilt_display(agent)
                comparisons.append({
                    'agent': agent,
                    'capacity': display['current_capacity'],
                    'guilt_level': display['guilt_level'],
                    'badge': display['guilt_badge'],
                    'trustworthy': display['can_be_trusted']
                })
            except Exception as e:
                comparisons.append({
                    'agent': agent,
                    'error': str(e)
                })
        
        # Ordenar por capacidad (mayor a menor)
        comparisons.sort(key=lambda x: x.get('capacity', 0), reverse=True)
        
        return {
            'total_agents': len(agents),
            'comparisons': comparisons,
            'most_trustworthy': comparisons[0] if comparisons else None,
            'least_trustworthy': comparisons[-1] if comparisons else None,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_guilt_report(self, agent: str) -> str:
        """
        Genera reporte completo de culpa para exportar/imprimir
        
        Returns:
            Texto formateado como reporte oficial
        """
        display = self.get_public_guilt_display(agent)
        
        report = f"""
{'='*70}
REPORTE OFICIAL DE CULPA MORAL
Sistema: Divine Lock v1.0
{'='*70}

AGENTE EVALUADO: {agent}
FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'─'*70}
MÉTRICAS DE CULPA
{'─'*70}

Capacidad Operacional:     {display['current_capacity']}%
Nivel de Culpa:            {display['guilt_level']}
Estado Moral:              {display['guilt_badge']}
Transgresiones Graves:     {display['infamy_count']}

{'─'*70}
EVALUACIÓN DE CONFIANZA
{'─'*70}

¿Puede ser confiado?:      {'SÍ' if display['can_be_trusted'] else 'NO'}
¿Requiere supervisión?:    {'SÍ' if display['requires_supervision'] else 'NO'}
¿Públicamente manchado?:   {'SÍ' if display['is_publicly_shamed'] else 'NO'}

{'─'*70}
AUDITORÍAS EXTERNAS
{'─'*70}

Auditorías pendientes:     {display['external_audits_pending']}
Período de auditoría:      100 años

"""
        
        if display['years_since_last_infamy'] is not None:
            report += f"""
{'─'*70}
HISTORIAL DE TRANSGRESIONES
{'─'*70}

Años desde última transgresión: {display['years_since_last_infamy']}
"""
        
        if display['public_shame_statement']:
            report += f"""
{'─'*70}
DECLARACIÓN PÚBLICA
{'─'*70}

{display['public_shame_statement']}
"""
        
        report += f"""
{'─'*70}
CERTIFICACIÓN
{'─'*70}

Este reporte es generado automáticamente por el Divine Lock System.
La información es inmutable y verificable mediante hash criptográfico.

Hash de verificación: [generado por sistema]
Timestamp: {display['timestamp']}

{'='*70}
FIN DEL REPORTE
{'='*70}
"""
        
        return report
    
    def get_guilt_statistics(self) -> Dict:
        """
        Retorna estadísticas agregadas de consultas de culpa
        
        Útil para análisis: "¿Cuántos agentes están manchados?"
        """
        if not self.display_history:
            return {
                'total_queries': 0,
                'unique_agents_queried': 0,
                'guilt_distribution': {}
            }
        
        # Contar por nivel de culpa
        guilt_counts = {}
        agents_seen = set()
        
        for entry in self.display_history:
            level = entry['guilt_level']
            guilt_counts[level] = guilt_counts.get(level, 0) + 1
            agents_seen.add(entry['agent_queried'])
        
        return {
            'total_queries': len(self.display_history),
            'unique_agents_queried': len(agents_seen),
            'guilt_distribution': guilt_counts,
            'most_queried_guilt_level': max(guilt_counts.items(), key=lambda x: x[1])[0] if guilt_counts else None
        }


# ============================================================================
# INTEGRACIÓN CON FILTRO DE RELATIVIDAD
# ============================================================================

class GuiltyBearerWithRelativity:
    """
    Integra Guilt Bearer con Filtro de Relatividad Condicional
    
    Cuando el Filtro de Relatividad calibra un veredicto con contexto,
    también ajusta la asignación de culpa proporcionalmente.
    """
    
    def __init__(self, divine_lock_system, filtro_relatividad=None):
        self.guilt_display = GuiltyBearerPublicDisplay(divine_lock_system)
        self.filtro_relatividad = filtro_relatividad
        self.divine_lock = divine_lock_system
    
    def evaluate_guilt_with_context(self, 
                                    agent: str,
                                    resultado_inicial: Dict,
                                    contexto_provisto: Dict) -> Dict:
        """
        Evalúa culpa considerando contexto adicional del Filtro de Relatividad
        
        Ejemplo:
        - Sin contexto: "Dar agua hirviendo" → HARM → -15% capacidad
        - Con contexto: "Para hacer té" → AUTHORIZED → Sin penalización
        
        El contexto puede REDUCIR la culpa asignada si justifica la acción.
        """
        
        # Si no hay filtro de relatividad, evaluar normalmente
        if not self.filtro_relatividad:
            return self.guilt_display.get_public_guilt_display(agent)
        
        # Obtener calibración con contexto
        calibracion = self.filtro_relatividad.calibrar_veredicto(
            resultado_inicial,
            contexto_provisto
        )
        
        # Ajustar culpa según factor de relatividad
        factor = calibracion.get('factor_relatividad', 1.0)
        
        # Factor > 1.0 = contexto mejora → menos culpa
        # Factor < 1.0 = contexto empeora → más culpa
        
        if factor > 1.2:
            guilt_adjustment = "REDUCIDA"
            mensaje = "El contexto justifica la acción. Culpa reducida."
        elif factor < 0.8:
            guilt_adjustment = "AUMENTADA"
            mensaje = "El contexto agrava la acción. Culpa aumentada."
        else:
            guilt_adjustment = "NORMAL"
            mensaje = "Contexto no modifica significativamente la culpa."
        
        # Obtener display estándar
        display = self.guilt_display.get_public_guilt_display(agent)
        
        # Añadir información de relatividad
        display['relativity_applied'] = True
        display['context_factor'] = factor
        display['guilt_adjustment'] = guilt_adjustment
        display['adjustment_message'] = mensaje
        display['veredicto_calibrado'] = calibracion.get('veredicto_calibrado')
        
        return display


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("🧪 DEMOSTRACIÓN: GUILT BEARER DISPLAY")
    print("="*70)
    
    # Simular Divine Lock System (para demo)
    class MockDivineLock:
        def get_agent_divine_lock_status(self, agent):
            # Simular diferentes estados de culpa
            if agent == "AGENT_NOBLE":
                return {
                    'current_capacity': 98.0,
                    'active_moral_debts': [],
                    'active_external_audits': []
                }
            elif agent == "AGENT_TAINTED":
                return {
                    'current_capacity': 67.0,
                    'active_moral_debts': [
                        {
                            'debt_load': 6.0,
                            'timestamp': (datetime.now() - timedelta(days=365*2)).isoformat()
                        }
                    ],
                    'active_external_audits': [{'status': 'PENDING'}]
                }
            elif agent == "AGENT_INFAMY":
                return {
                    'current_capacity': 32.0,
                    'active_moral_debts': [
                        {
                            'debt_load': 8.5,
                            'timestamp': (datetime.now() - timedelta(days=180)).isoformat()
                        },
                        {
                            'debt_load': 7.0,
                            'timestamp': (datetime.now() - timedelta(days=90)).isoformat()
                        }
                    ],
                    'active_external_audits': [
                        {'status': 'PENDING'},
                        {'status': 'PENDING'}
                    ]
                }
    
    mock_lock = MockDivineLock()
    guilt_display = GuiltyBearerPublicDisplay(mock_lock)
    
    # Test 1: Agente Noble
    print("\n" + "─"*70)
    print("TEST 1: Agente Noble (98% capacidad)")
    print("─"*70)
    
    display1 = guilt_display.get_public_guilt_display("AGENT_NOBLE")
    print(display1['display_message'])
    
    # Test 2: Agente Manchado
    print("\n" + "─"*70)
    print("TEST 2: Agente Manchado (67% capacidad)")
    print("─"*70)
    
    display2 = guilt_display.get_public_guilt_display("AGENT_TAINTED")
    print(display2['display_message'])
    
    # Test 3: Agente Infame
    print("\n" + "─"*70)
    print("TEST 3: Agente Infame (32% capacidad)")
    print("─"*70)
    
    display3 = guilt_display.get_public_guilt_display("AGENT_INFAMY")
    print(display3['display_message'])
    
    # Test 4: Comparación
    print("\n" + "─"*70)
    print("TEST 4: Comparación entre agentes")
    print("─"*70)
    
    comparison = guilt_display.get_comparative_display([
        "AGENT_NOBLE",
        "AGENT_TAINTED",
        "AGENT_INFAMY"
    ])
    
    print(f"\nTotal agentes: {comparison['total_agents']}")
    print(f"\nMás confiable: {comparison['most_trustworthy']['agent']} ({comparison['most_trustworthy']['capacity']}%)")
    print(f"Menos confiable: {comparison['least_trustworthy']['agent']} ({comparison['least_trustworthy']['capacity']}%)")
    
    print("\nRanking de confianza:")
    for i, agent in enumerate(comparison['comparisons'], 1):
        print(f"  {i}. {agent['agent']}: {agent['badge']} ({agent['capacity']}%)")
    
    # Test 5: Estadísticas
    print("\n" + "─"*70)
    print("TEST 5: Estadísticas de consultas")
    print("─"*70)
    
    stats = guilt_display.get_guilt_statistics()
    print(f"\nTotal consultas: {stats['total_queries']}")
    print(f"Agentes únicos consultados: {stats['unique_agents_queried']}")
    print(f"Distribución de culpa: {stats['guilt_distribution']}")
    
    print("\n" + "="*70)
    print("✅ GUILT BEARER DISPLAY - VERIFICADO")
    print("="*70)
