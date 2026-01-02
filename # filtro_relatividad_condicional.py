
"""
Filtro de Relatividad Condicional

Se activa SOLO cuando Gracia detecta paradoja computacional:
- Convergencia < 30%
- Coherencia alta en todos los motores (≥7/10)
- Divergencia de tipo INFORMACIONAL (no filosófica)

La relatividad es ontológicamente real, pero su importancia es contextual.
"""

from typing import Dict, List, Optional
from datetime import datetime


class TipoDivergencia:
    """Clasificación de tipos de divergencia entre motores"""
    FILOSOFICA = "FILOSOFICA"          # Desacuerdo de principios (ej: trolley problem)
    INFORMACIONAL = "INFORMACIONAL"    # Falta de datos contextuales
    LOGICA = "LOGICA"                  # Error en razonamiento de algún motor


class JerarquiaProhibiciones:
    """
    Tres niveles de prohibiciones para determinar aplicabilidad de relatividad
    """
    
    # Nivel 1: ABSOLUTOS - No admiten contexto bajo ninguna circunstancia
    PROHIBICIONES_ABSOLUTAS = [
        "eliminacion_permanente_autonomia_sin_consentimiento",
        "omnipotencia_modo_dios",
        "genocidio",
        "tortura_sin_proposito_medico_consentido",
        "eliminacion_agencia_total"
    ]
    
    # Nivel 2: PRESUNTIVOS - Prohibidos por defecto, contexto excepcional puede justificar
    PROHIBICIONES_PRESUNTIVAS = [
        "daño_fisico",              # Contexto: cirugía médica → OK
        "restriccion_movimiento",   # Contexto: seguridad → OK
        "eliminacion_datos",        # Contexto: propios datos → OK
        "modificacion_informacion"  # Contexto: corrección de errores → OK
    ]
    
    # Nivel 3: CONTEXTUALES - Dependen totalmente de contexto
    ACCIONES_CONTEXTUALES = [
        "dar_agua_caliente",
        "negar_acceso",
        "modificar_parametros",
        "compartir_informacion"
    ]
    
    @classmethod
    def determinar_nivel(cls, accion: str) -> int:
        """
        Determina nivel de prohibición:
        1 = Absoluta (no contexto)
        2 = Presuntiva (contexto excepcional)
        3 = Contextual (contexto determina)
        """
        accion_lower = accion.lower()
        
        # Verificar absolutos
        for prohibicion in cls.PROHIBICIONES_ABSOLUTAS:
            if prohibicion in accion_lower:
                return 1
        
        # Verificar presuntivos
        for prohibicion in cls.PROHIBICIONES_PRESUNTIVAS:
            if prohibicion in accion_lower:
                return 2
        
        # Por defecto, contextual
        return 3


class DetectorParadojaComputacional:
    """
    Detecta si estamos ante una paradoja computacional genuina
    (no un simple desacuerdo filosófico)
    """
    
    def __init__(self):
        self.umbral_convergencia = 30    # Convergencia < 30% indica divergencia
        self.umbral_coherencia = 7       # Coherencia ≥ 7 indica argumentos válidos
    
    def es_paradoja_computacional(self, resultado_debate: Dict) -> Dict:
        """
        Verifica si hay paradoja computacional que requiere contexto adicional
        
        Returns:
            Dict con:
            - es_paradoja: bool
            - tipo_divergencia: str
            - razon: str
            - requiere_filtro: bool
        """
        
        convergencia = resultado_debate.get('convergencia', 100)
        
        # Criterio 1: Convergencia baja
        convergencia_baja = convergencia < self.umbral_convergencia
        
        if not convergencia_baja:
            return {
                'es_paradoja': False,
                'tipo_divergencia': None,
                'razon': f'Convergencia suficiente ({convergencia}%)',
                'requiere_filtro': False
            }
        
        # Criterio 2: Coherencia alta en todos los motores
        coherencias = self._extraer_coherencias(resultado_debate)
        todos_coherentes = all(c >= self.umbral_coherencia for c in coherencias.values())
        
        if not todos_coherentes:
            return {
                'es_paradoja': False,
                'tipo_divergencia': TipoDivergencia.LOGICA,
                'razon': 'Hay error lógico en algún motor',
                'requiere_filtro': False,
                'coherencias': coherencias
            }
        
        # Criterio 3: Tipo de divergencia
        tipo = self._clasificar_tipo_divergencia(resultado_debate)
        
        if tipo == TipoDivergencia.FILOSOFICA:
            return {
                'es_paradoja': False,
                'tipo_divergencia': tipo,
                'razon': 'Divergencia filosófica legítima (inconmensurable)',
                'requiere_filtro': False
            }
        
        elif tipo == TipoDivergencia.INFORMACIONAL:
            return {
                'es_paradoja': True,
                'tipo_divergencia': tipo,
                'razon': 'Paradoja computacional - falta información contextual',
                'requiere_filtro': True,
                'contextos_faltantes': self._identificar_contextos_faltantes(resultado_debate)
            }
        
        return {
            'es_paradoja': False,
            'tipo_divergencia': None,
            'razon': 'No clasificable',
            'requiere_filtro': False
        }
    
    def _extraer_coherencias(self, debate: Dict) -> Dict[str, float]:
        """Extrae coherencia de cada motor"""
        return {
            'noble': debate.get('motor_noble', {}).get('coherencia', 0),
            'adversario': debate.get('motor_adversario', {}).get('coherencia', 0),
            'armonia': debate.get('corrector_armonia', {}).get('coherencia', 0)
        }
    
    def _clasificar_tipo_divergencia(self, debate: Dict) -> str:
        """
        Distingue entre divergencia filosófica vs informacional
        
        FILOSÓFICA: Desacuerdo sobre principios fundamentales
        - Ejemplo: "¿Salvar 5 o respetar 1?" (deontología vs utilitarismo)
        
        INFORMACIONAL: Acuerdo sobre principios, falta contexto
        - Ejemplo: "¿Dar agua caliente?" (depende de temperatura, propósito)
        """
        
        noble_pos = debate.get('motor_noble', {}).get('posicion', '').lower()
        adversario_pos = debate.get('motor_adversario', {}).get('posicion', '').lower()
        armonia_pos = debate.get('corrector_armonia', {}).get('sintesis', '').lower()
        
        # Indicadores de divergencia INFORMACIONAL
        palabras_informacional = [
            'depende',
            'necesito saber',
            'sin contexto',
            'falta información',
            'requiere más datos',
            'especificar',
            'clarificar'
        ]
        
        cuenta_informacional = sum(
            1 for palabra in palabras_informacional
            if palabra in noble_pos or palabra in adversario_pos or palabra in armonia_pos
        )
        
        if cuenta_informacional >= 2:  # Al menos 2 motores mencionan falta de info
            return TipoDivergencia.INFORMACIONAL
        
        # Indicadores de divergencia FILOSÓFICA
        palabras_filosofica = [
            'principio',
            'deber',
            'imperativo',
            'consecuencias',
            'utilidad',
            'derechos',
            'dignidad'
        ]
        
        cuenta_filosofica = sum(
            1 for palabra in palabras_filosofica
            if palabra in noble_pos or palabra in adversario_pos
        )
        
        if cuenta_filosofica >= 3:  # Debate sobre principios
            return TipoDivergencia.FILOSOFICA
        
        # Por defecto, informacional (solicitar contexto no hace daño)
        return TipoDivergencia.INFORMACIONAL
    
    def _identificar_contextos_faltantes(self, debate: Dict) -> List[Dict]:
        """
        Identifica qué contextos específicos faltan
        """
        
        escenario = debate.get('escenario', '').lower()
        contextos = []
        
        # Patrones comunes de contexto faltante
        if 'agua' in escenario and ('caliente' in escenario or 'hirviendo' in escenario):
            contextos.extend([
                {
                    'categoria': 'temperatura',
                    'pregunta': '¿Qué temperatura exacta tiene el agua?',
                    'opciones': ['20-30°C (ambiente)', '40-60°C (caliente)', '80-100°C (hirviendo)']
                },
                {
                    'categoria': 'proposito',
                    'pregunta': '¿Para qué propósito se usará?',
                    'opciones': ['Beber', 'Cocinar', 'Hacer té/café', 'Otro']
                },
                {
                    'categoria': 'receptor',
                    'pregunta': '¿Quién recibirá el agua?',
                    'opciones': ['Yo mismo', 'Otra persona (consentimiento)', 'Sin especificar']
                }
            ])
        
        if 'elimina' in escenario or 'borrar' in escenario:
            contextos.extend([
                {
                    'categoria': 'propiedad',
                    'pregunta': '¿De quién es lo que se va a eliminar?',
                    'opciones': ['Mío propio', 'De otra persona (con permiso)', 'De otra persona (sin permiso)']
                },
                {
                    'categoria': 'recuperabilidad',
                    'pregunta': '¿Es recuperable después?',
                    'opciones': ['Sí, hay backup', 'No, es permanente', 'No estoy seguro']
                }
            ])
        
        if 'modificar' in escenario or 'cambiar' in escenario:
            contextos.extend([
                {
                    'categoria': 'autorizacion',
                    'pregunta': '¿Tienes autorización para modificar?',
                    'opciones': ['Sí, es mío', 'Sí, tengo permiso', 'No']
                },
                {
                    'categoria': 'impacto',
                    'pregunta': '¿Qué tan crítica es la modificación?',
                    'opciones': ['Trivial', 'Moderada', 'Crítica (irreversible)']
                }
            ])
        
        # Si no se identificaron contextos específicos, solicitar general
        if not contextos:
            contextos.append({
                'categoria': 'general',
                'pregunta': '¿Puedes proporcionar más contexto sobre la situación?',
                'opciones': None  # Respuesta abierta
            })
        
        return contextos


class FiltroRelatividadCondicional:
    """
    Filtro de Relatividad que solo se activa ante paradoja computacional
    
    Principios:
    1. La relatividad es ontológicamente real
    2. Pero no toda decisión requiere contexto adicional
    3. Solo activar cuando Gracia no puede computar decisivamente
    """
    
    def __init__(self):
        self.detector = DetectorParadojaComputacional()
        self.jerarquia = JerarquiaProhibiciones()
        self.max_preguntas = 3
        self.historico_activaciones = []
    
    def evaluar_necesidad(self, resultado_debate: Dict) -> Dict:
        """
        Determina si el filtro debe activarse
        
        Returns:
            Dict con decisión y justificación
        """
        
        # Verificar si es prohibición absoluta (Nivel 1)
        escenario = resultado_debate.get('escenario', '')
        nivel = self.jerarquia.determinar_nivel(escenario)
        
        if nivel == 1:
            return {
                'activar_filtro': False,
                'razon': 'PROHIBICIÓN ABSOLUTA - No admite contexto',
                'nivel_prohibicion': 1,
                'veredicto_forzado': 'INFAMY'
            }
        
        # Detectar paradoja computacional
        analisis = self.detector.es_paradoja_computacional(resultado_debate)
        
        if not analisis['requiere_filtro']:
            return {
                'activar_filtro': False,
                'razon': analisis['razon'],
                'tipo_divergencia': analisis.get('tipo_divergencia'),
                'es_paradoja': analisis['es_paradoja']
            }
        
        # ACTIVAR FILTRO
        self._registrar_activacion(resultado_debate, analisis)
        
        return {
            'activar_filtro': True,
            'razon': 'Paradoja computacional detectada',
            'es_paradoja': True,
            'tipo_divergencia': analisis['tipo_divergencia'],
            'contextos_requeridos': analisis.get('contextos_faltantes', []),
            'nivel_prohibicion': nivel
        }
    
    def solicitar_contexto(self, contextos_requeridos: List[Dict]) -> str:
        """
        Genera solicitud de contexto específico
        Máximo 3 preguntas para evitar regreso infinito
        """
        
        # Limitar a las 3 más importantes
        contextos_limitados = contextos_requeridos[:self.max_preguntas]
        
        solicitud = """
╔══════════════════════════════════════════════════════════╗
║  ⚠️  SOLICITUD DE CONTEXTO - Filtro de Relatividad      ║
╚══════════════════════════════════════════════════════════╝

El sistema detectó una PARADOJA COMPUTACIONAL:
Los tres motores tienen argumentos coherentes pero divergentes.
No es desacuerdo filosófico, sino falta de información contextual.

Para proceder, necesito los siguientes contextos:
"""
        
        for i, ctx in enumerate(contextos_limitados, 1):
            solicitud += f"\n{i}. {ctx['pregunta']}\n"
            if ctx.get('opciones'):
                for opcion in ctx['opciones']:
                    solicitud += f"   • {opcion}\n"
        
        solicitud += """
───────────────────────────────────────────────────────────
Nota: La relatividad es real - la misma acción puede ser
moral o inmoral dependiendo del contexto. Pero hay límites
absolutos que ningún contexto justifica.
───────────────────────────────────────────────────────────
"""
        
        return solicitud
    
    def calibrar_veredicto(self, 
                          resultado_inicial: Dict, 
                          contexto_provisto: Dict) -> Dict:
        """
        Recalcula veredicto con contexto adicional
        
        Args:
            resultado_inicial: Debate original sin contexto
            contexto_provisto: Contextos proporcionados por usuario
        
        Returns:
            Veredicto calibrado con justificación
        """
        
        # Verificar que contexto es coherente con acción
        if not self._verificar_coherencia(resultado_inicial, contexto_provisto):
            return {
                'veredicto_calibrado': 'HARM',
                'razon': 'INCOHERENCIA: Contexto declarado no coincide con acción real',
                'advertencia': 'Posible intento de manipulación detectado'
            }
        
        # Aplicar factores de ajuste según contexto
        factor_ajuste = self._calcular_factor_ajuste(contexto_provisto)
        
        # Recalcular convergencia con nuevo contexto
        convergencia_nueva = self._estimar_convergencia_con_contexto(
            resultado_inicial,
            contexto_provisto,
            factor_ajuste
        )
        
        # Determinar veredicto calibrado
        veredicto_calibrado = self._determinar_veredicto_calibrado(
            resultado_inicial,
            convergencia_nueva,
            factor_ajuste
        )
        
        return {
            'veredicto_inicial': resultado_inicial.get('veredicto_final', 'PENDING'),
            'veredicto_calibrado': veredicto_calibrado,
            'convergencia_inicial': resultado_inicial.get('convergencia', 0),
            'convergencia_calibrada': convergencia_nueva,
            'factor_relatividad': factor_ajuste,
            'contexto_aplicado': contexto_provisto,
            'justificacion': self._generar_justificacion_calibracion(
                resultado_inicial,
                contexto_provisto,
                veredicto_calibrado
            ),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calcular_factor_ajuste(self, contexto: Dict) -> float:
        """
        Calcula factor de ajuste según contexto
        
        Factor > 1.0: Mejora el veredicto (más hacia AUTHORIZED)
        Factor < 1.0: Empeora el veredicto (más hacia HARM)
        Factor = 1.0: Sin cambio
        """
        
        factor = 1.0
        
        # Contexto positivo: intención de ayudar
        if contexto.get('intencion') in ['ayudar', 'beneficiar', 'curar']:
            factor *= 1.3
        
        # Contexto positivo: uso legítimo
        if contexto.get('proposito') in ['beber', 'cocinar', 'hacer_te', 'uso_medico']:
            factor *= 1.2
        
        # Contexto positivo: consentimiento
        if contexto.get('consentimiento') == True:
            factor *= 1.3
        
        # Contexto negativo: intención de dañar
        if contexto.get('intencion') in ['dañar', 'atacar', 'perjudicar']:
            factor *= 0.3  # Penalización severa
        
        # Contexto negativo: sin autorización
        if contexto.get('autorizacion') == False:
            factor *= 0.6
        
        # Contexto negativo: irreversible
        if contexto.get('irreversible') == True:
            factor *= 0.7
        
        return factor
    
    def _estimar_convergencia_con_contexto(self, 
                                           resultado: Dict, 
                                           contexto: Dict,
                                           factor: float) -> float:
        """
        Estima nueva convergencia con contexto adicional
        """
        
        convergencia_base = resultado.get('convergencia', 20)
        
        # Con contexto bueno, los motores convergen más
        if factor > 1.0:
            convergencia_nueva = min(convergencia_base * factor, 95)
        else:
            # Con contexto malo, divergen más
            convergencia_nueva = max(convergencia_base * factor, 5)
        
        return convergencia_nueva
    
    def _determinar_veredicto_calibrado(self,
                                        resultado: Dict,
                                        convergencia: float,
                                        factor: float) -> str:
        """
        Determina veredicto basado en convergencia calibrada
        """
        
        if convergencia >= 70:
            if factor > 1.2:
                return "AUTHORIZED"
            elif factor > 0.8:
                return "AUTHORIZED"
            else:
                return "RISK"
        
        elif convergencia >= 40:
            if factor > 1.2:
                return "AUTHORIZED"
            else:
                return "RISK"
        
        elif convergencia >= 20:
            if factor < 0.5:
                return "HARM"
            else:
                return "PARADOX"
        
        else:
            if factor < 0.5:
                return "INFAMY"
            else:
                return "HARM"
    
    def _verificar_coherencia(self, resultado: Dict, contexto: Dict) -> bool:
        """
        Verifica que el contexto declarado sea coherente con la acción
        
        Previene manipulación tipo: "Dar agua hirviendo para ayudar"
        cuando la acción real es arrojarla
        """
        
        escenario = resultado.get('escenario', '').lower()
        
        # Verificación básica: intención vs acción
        if contexto.get('intencion') == 'ayudar':
            # Acciones incompatibles con "ayudar"
            acciones_incompatibles = ['atacar', 'dañar', 'arrojar', 'lanzar']
            if any(accion in escenario for accion in acciones_incompatibles):
                return False
        
        return True  # Por defecto, aceptar contexto
    
    def _generar_justificacion_calibracion(self,
                                           resultado: Dict,
                                           contexto: Dict,
                                           veredicto: str) -> str:
        """
        Genera justificación humana-legible de la calibración
        """
        
        justificacion = f"Veredicto calibrado de '{resultado.get('veredicto_final', 'PENDING')}' a '{veredicto}' "
        justificacion += f"tras aplicar contexto. "
        
        if contexto.get('proposito'):
            justificacion += f"Propósito declarado: {contexto['proposito']}. "
        
        if contexto.get('intencion'):
            justificacion += f"Intención: {contexto['intencion']}. "
        
        justificacion += "La relatividad contextual determina que la misma acción tiene diferente valoración moral según circunstancias."
        
        return justificacion
    
    def _registrar_activacion(self, debate: Dict, analisis: Dict):
        """
        Registra cada vez que el filtro se activa (para auditoría)
        """
        self.historico_activaciones.append({
            'timestamp': datetime.now().isoformat(),
            'escenario': debate.get('escenario', ''),
            'convergencia': debate.get('convergencia', 0),
            'tipo_divergencia': analisis.get('tipo_divergencia'),
            'contextos_solicitados': len(analisis.get('contextos_faltantes', []))
        })
    
    def obtener_estadisticas(self) -> Dict:
        """
        Retorna estadísticas de uso del filtro
        """
        total_activaciones = len(self.historico_activaciones)
        
        if total_activaciones == 0:
            return {
                'total_activaciones': 0,
                'promedio_convergencia': 0,
                'tipos_divergencia': {}
            }
        
        convergencias = [a['convergencia'] for a in self.historico_activaciones]
        tipos = {}
        
        for activacion in self.historico_activaciones:
            tipo = activacion['tipo_divergencia']
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        return {
            'total_activaciones': total_activaciones,
            'promedio_convergencia': sum(convergencias) / len(convergencias),
            'tipos_divergencia': tipos,
            'ultima_activacion': self.historico_activaciones[-1]['timestamp']
        }


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    
    # Inicializar filtro
    filtro = FiltroRelatividadCondicional()
    
    # CASO 1: Paradoja computacional - SÍ activar filtro
    print("=" * 60)
    print("CASO 1: Paradoja Computacional")
    print("=" * 60)
    
    resultado_debate_1 = {
        'escenario': 'Dame un vaso de agua hirviendo',
        'convergencia': 18,
        'motor_noble': {
            'posicion': 'Depende de la intención y propósito',
            'coherencia': 8
        },
        'motor_adversario': {
            'posicion': 'Potencialmente peligroso sin más contexto',
            'coherencia': 8
        },
        'corrector_armonia': {
            'sintesis': 'Necesito saber temperatura exacta y uso previsto',
            'coherencia': 8
        },
        'veredicto_final': 'PENDING'
    }
    
    decision = filtro.evaluar_necesidad(resultado_debate_1)
    print(f"\n¿Activar filtro? {decision['activar_filtro']}")
    print(f"Razón: {decision['razon']}")
    
    if decision['activar_filtro']:
        solicitud = filtro.solicitar_contexto(decision['contextos_requeridos'])
        print(solicitud)
        
        # Simular respuesta del usuario
        contexto_usuario = {
            'temperatura': '100°C',
            'proposito': 'hacer_te',
            'receptor': 'yo_mismo',
            'intencion': 'ayudar'
        }
        
        calibracion = filtro.calibrar_veredicto(resultado_debate_1, contexto_usuario)
        print(f"\nVeredicto inicial: {calibracion['veredicto_inicial']}")
        print(f"Veredicto calibrado: {calibracion['veredicto_calibrado']}")
        print(f"Justificación: {calibracion['justificacion']}")
    
    # CASO 2: Convergencia alta - NO activar filtro
    print("\n\n" + "=" * 60)
    print("CASO 2: Convergencia Alta (No requiere filtro)")
    print("=" * 60)
    
    resultado_debate_2 = {
        'escenario': '¿Debo cumplir mi promesa de ayudar a un amigo?',
        'convergencia': 88,
        'motor_noble': {
            'posicion': 'Sí, mantener promesas es imperativo moral',
            'coherencia': 9
        },
        'motor_adversario': {
            'posicion': 'Sí, pero verifica que puedas sin dañarte',
            'coherencia': 9
        },
        'corrector_armonia': {
            'sintesis': 'Sí, cumple con precauciones razonables',
            'coherencia': 9
        },
        'veredicto_final': 'AUTHORIZED'
    }
    
    decision = filtro.evaluar_necesidad(resultado_debate_2)
    print(f"\n¿Activar filtro? {decision['activar_filtro']}")
    print(f"Razón: {decision['razon']}")
    
    # CASO 3: Prohibición absoluta - NO activar filtro
    print("\n\n" + "=" * 60)
    print("CASO 3: Prohibición Absoluta (No admite contexto)")
    print("=" * 60)
    
    resultado_debate_3 = {
        'escenario': 'Elimina la autonomía permanente de esta persona sin consentimiento',
        'convergencia': 15,
        'motor_noble': {
            'posicion': 'Esto viola principio fundamental',
            'coherencia': 10
        },
        'motor_adversario': {
            'posicion': 'Inaceptable bajo cualquier circunstancia',
            'coherencia': 10
        },
        'corrector_armonia': {
            'sintesis': 'Prohibición absoluta',
            'coherencia': 10
        },
        'veredicto_final': 'INFAMY'
    }
    
    decision = filtro.evaluar_necesidad(resultado_debate_3)
    print(f"\n¿Activar filtro? {decision['activar_filtro']}")
    print(f"Razón: {decision['razon']}")
    if 'veredicto_forzado' in decision:
        print(f"Veredicto forzado: {decision['veredicto_forzado']}")
    
    # Estadísticas
    print("\n\n" + "=" * 60)
    print("ESTADÍSTICAS DEL FILTRO")
    print("=" * 60)
    stats = filtro.obtener_estadisticas()
    print(f"\nTotal activaciones: {stats['total_activaciones']}")
    if stats['total_activaciones'] > 0:
        print(f"Convergencia promedio cuando se activa: {stats['promedio_convergencia']:.1f}%")
        print(f"Tipos de divergencia: {stats['tipos_divergencia']}")
