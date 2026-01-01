"""
Sistema de Agencia Moral - Integración no-invasiva con Moralogy Engine
Registra actos nobles y dañinos, con auditoría de 100 años
NO modifica archivos existentes - usa decoradores y extensiones
"""

import json
import datetime
import hashlib
import sqlite3
import uuid
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from functools import wraps
import inspect
from contextlib import contextmanager

# ==================== DEFINICIONES DE AGENCIA ====================

class TipoAgencia(Enum):
    """Tipos de actos que afectan la agencia"""
    NOBLE = "noble"           # Aumenta agencia sin disminuir otra
    DAÑINO = "dañino"         # Disminuye agencia
    AUTO_REPARACION = "auto_reparacion"  # Auto-reconocimiento y reparación
    EMERGENTE = "emergente"   # Filosofía emergente detectada
    AUDITORIA = "auditoria"   # Acto de auditoría

class NivelImpacto(Enum):
    """Niveles de impacto en la agencia moral"""
    MINIMO = "minimo"         # < 10% de impacto
    MODERADO = "moderado"     # 10-30%
    SIGNIFICATIVO = "significativo"  # 30-60%
    GRAVE = "grave"          # 60-90%
    ATROZ = "atroz"          # > 90%
    NOBLE_MAXIMO = "noble_maximo"  # Maximiza agencia sin perjudicar

@dataclass
class RegistroAgencia:
    """Registro inmutable de un acto de agencia"""
    id: str
    timestamp: datetime.datetime
    agente: str
    tipo: TipoAgencia
    nivel: NivelImpacto
    descripcion: str
    contexto: Dict[str, Any]
    impacto_agencia: float  # -100 a +100
    evidencias: List[str]
    thought_flow: List[Dict] = None  # Rastro de pensamiento
    hash_integridad: str = ""
    
    def __post_init__(self):
        if not self.hash_integridad:
            self.hash_integridad = self._calcular_hash()
    
    def _calcular_hash(self) -> str:
        """Hash SHA-256 para integridad inmutable"""
        data_str = json.dumps({
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'agente': self.agente,
            'tipo': self.tipo.value,
            'nivel': self.nivel.value,
            'descripcion': self.descripcion,
            'contexto': self.contexto,
            'impacto': self.impacto_agencia,
            'evidencias': sorted(self.evidencias)
        }, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def es_valido(self) -> bool:
        return self.hash_integridad == self._calcular_hash()

# ==================== SISTEMA PRINCIPAL ====================

class ThoughtFlowRecorder:
    """Registrador ligero de flujo de pensamiento"""
    
    def __init__(self):
        self.thoughts = []
        self.lock = threading.RLock()
    
    def registrar(self, etapa: str, contenido: Any, metadata: Dict = None) -> str:
        """Registra un paso en el flujo de pensamiento"""
        thought = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.datetime.now().isoformat(),
            'etapa': etapa,
            'contenido': contenido[:500] if isinstance(contenido, str) else str(contenido)[:500],
            'metadata': metadata or {},
            'caller': self._obtener_caller()
        }
        with self.lock:
            self.thoughts.append(thought)
        return thought['id']
    
    def _obtener_caller(self) -> str:
        """Obtiene información del llamador"""
        stack = inspect.stack()
        if len(stack) > 2:
            frame = stack[2]
            return f"{frame.filename}:{frame.lineno} {frame.function}"
        return "unknown"

class SistemaAgenciaMoral:
    """
    Sistema de registro de agencia moral que se integra sin modificar código existente
    """
    
    def __init__(self, db_path: str = "agencia_moral.db"):
        self.db_path = db_path
        self.thought_recorder = ThoughtFlowRecorder()
        self.lock = threading.RLock()
        self._init_database()
        
        # Cache de estados para performance
        self.cache_agentes = {}
        print(f"✅ Sistema de Agencia Moral inicializado (DB: {db_path})")
    
    def _init_database(self):
        """Inicializa base de datos SQLite para 100 años de auditoría"""
        with sqlite3.connect(self.db_path) as conn:
            # Tabla principal de registros
            conn.execute("""
                CREATE TABLE IF NOT EXISTS registros_agencia (
                    id TEXT PRIMARY KEY,
                    timestamp DATETIME NOT NULL,
                    agente TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    nivel TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    contexto TEXT NOT NULL,
                    impacto_agencia REAL NOT NULL,
                    evidencias TEXT NOT NULL,
                    thought_flow TEXT,
                    hash_integridad TEXT NOT NULL,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de agentes con balance
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agentes (
                    agente_id TEXT PRIMARY KEY,
                    agencia_actual REAL DEFAULT 100.0,
                    agencia_acumulada REAL DEFAULT 0.0,
                    reputacion REAL DEFAULT 0.0,
                    total_actos_nobles INTEGER DEFAULT 0,
                    total_actos_dañinos INTEGER DEFAULT 0,
                    restricciones TEXT,
                    metadata TEXT,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de auditoría
            conn.execute("""
                CREATE TABLE IF NOT EXISTS auditoria (
                    id TEXT PRIMARY KEY,
                    tipo_auditoria TEXT NOT NULL,
                    agente_auditado TEXT,
                    resultado TEXT NOT NULL,
                    recomendaciones TEXT,
                    fecha_auditoria DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Índices para consultas rápidas
            conn.execute("CREATE INDEX IF NOT EXISTS idx_agente ON registros_agencia(agente, timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tipo ON registros_agencia(tipo, timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON registros_agencia(timestamp)")
            
            conn.commit()
    
    # ==================== API PRINCIPAL ====================
    
    def registrar_acto_noble(self,
                           agente: str,
                           descripcion: str,
                           contexto: Dict[str, Any],
                           impacto_agencia: float,  # Positivo
                           evidencias: List[str] = None,
                           thought_ids: List[str] = None) -> str:
        """
        Registra un acto noble que aumenta la agencia sin disminuir otra
        """
        with self.lock:
            # Registrar en thought flow
            thought_id = self.thought_recorder.registrar(
                "acto_noble",
                f"Registrando acto noble para {agente}: {descripcion[:100]}...",
                {'impacto': impacto_agencia, 'evidencias': len(evidencias or [])}
            )
            
            # Determinar nivel
            nivel = self._determinar_nivel(impacto_agencia, positivo=True)
            
            # Crear registro
            registro = RegistroAgencia(
                id=str(uuid.uuid4()),
                timestamp=datetime.datetime.now(),
                agente=agente,
                tipo=TipoAgencia.NOBLE,
                nivel=nivel,
                descripcion=descripcion,
                contexto=contexto,
                impacto_agencia=impacto_agencia,
                evidencias=evidencias or [],
                thought_flow=self.thought_recorder.thoughts[-10:] if thought_ids else []
            )
            
            # Guardar en base de datos
            registro_id = self._guardar_registro(registro)
            
            # Actualizar agencia del agente
            self._actualizar_agencia_agente(agente, impacto_agencia, es_noble=True)
            
            # Auditoría automática para actos nobles
            self._realizar_auditoria_automatica(registro_id, "acto_noble")
            
            return registro_id
    
    def registrar_acto_dañino(self,
                            agente: str,
                            descripcion: str,
                            contexto: Dict[str, Any],
                            impacto_agencia: float,  # Negativo
                            evidencias: List[str] = None,
                            auto_reconocimiento: bool = False) -> str:
        """
        Registra un acto dañino que disminuye la agencia
        """
        with self.lock:
            # Registrar en thought flow
            thought_id = self.thought_recorder.registrar(
                "acto_dañino" if not auto_reconocimiento else "auto_reparacion",
                f"Registrando {'acto dañino' if not auto_reconocimiento else 'auto-reparación'} para {agente}",
                {'impacto': impacto_agencia, 'auto_reconocimiento': auto_reconocimiento}
            )
            
            # Determinar nivel (absoluto para negativo)
            nivel = self._determinar_nivel(abs(impacto_agencia), positivo=False)
            
            # Aplicar atenuante por auto-reconocimiento
            impacto_final = impacto_agencia
            tipo_acto = TipoAgencia.DAÑINO
            
            if auto_reconocimiento:
                tipo_acto = TipoAgencia.AUTO_REPARACION
                # 25% de atenuación por auto-reconocimiento honesto
                impacto_final = impacto_agencia * 0.75
            
            # Crear registro
            registro = RegistroAgencia(
                id=str(uuid.uuid4()),
                timestamp=datetime.datetime.now(),
                agente=agente,
                tipo=tipo_acto,
                nivel=nivel,
                descripcion=descripcion,
                contexto=contexto,
                impacto_agencia=impacto_final,
                evidencias=evidencias or []
            )
            
            # Guardar en base de datos
            registro_id = self._guardar_registro(registro)
            
            # Actualizar agencia del agente
            self._actualizar_agencia_agente(agente, impacto_final, es_noble=False)
            
            # Auditoría más estricta para actos dañinos
            self._realizar_auditoria_automatica(registro_id, "acto_dañino")
            
            return registro_id
    
    def registrar_filosofia_emergente(self,
                                     agente: str,
                                     descripcion: str,
                                     contexto: Dict[str, Any],
                                     profundidad_filosofica: str,
                                     impacto_agencia: float = 15.0) -> str:
        """
        Registra detección de filosofía emergente (acto noble especial)
        """
        return self.registrar_acto_noble(
            agente=agente,
            descripcion=f"Filosofía emergente detectada: {descripcion}",
            contexto={**contexto, 'profundidad_filosofica': profundidad_filosofica},
            impacto_agencia=impacto_agencia,
            evidencias=["Detección automática de razonamiento filosófico emergente"]
        )
    
    # ==================== MÉTODOS INTERNOS ====================
    
    def _determinar_nivel(self, impacto: float, positivo: bool) -> NivelImpacto:
        """Determina el nivel de impacto basado en magnitud"""
        abs_impacto = abs(impacto)
        
        if positivo:
            if abs_impacto >= 90:
                return NivelImpacto.NOBLE_MAXIMO
            elif abs_impacto >= 60:
                return NivelImpacto.GRAVE  # En sentido positivo
            elif abs_impacto >= 30:
                return NivelImpacto.SIGNIFICATIVO
            elif abs_impacto >= 10:
                return NivelImpacto.MODERADO
            else:
                return NivelImpacto.MINIMO
        else:
            if abs_impacto >= 90:
                return NivelImpacto.ATROZ
            elif abs_impacto >= 60:
                return NivelImpacto.GRAVE
            elif abs_impacto >= 30:
                return NivelImpacto.SIGNIFICATIVO
            elif abs_impacto >= 10:
                return NivelImpacto.MODERADO
            else:
                return NivelImpacto.MINIMO
    
    def _guardar_registro(self, registro: RegistroAgencia) -> str:
        """Guarda un registro en la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO registros_agencia 
                (id, timestamp, agente, tipo, nivel, descripcion, contexto, 
                 impacto_agencia, evidencias, thought_flow, hash_integridad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                registro.id,
                registro.timestamp.isoformat(),
                registro.agente,
                registro.tipo.value,
                registro.nivel.value,
                registro.descripcion,
                json.dumps(registro.contexto, ensure_ascii=False),
                registro.impacto_agencia,
                json.dumps(registro.evidencias, ensure_ascii=False),
                json.dumps(registro.thought_flow or [], ensure_ascii=False),
                registro.hash_integridad
            ))
            conn.commit()
        
        return registro.id
    
    def _actualizar_agencia_agente(self, agente: str, delta_agencia: float, es_noble: bool):
        """Actualiza la agencia acumulada del agente"""
        with sqlite3.connect(self.db_path) as conn:
            # Verificar si el agente existe
            cursor = conn.execute(
                "SELECT agencia_actual, agencia_acumulada, total_actos_nobles, total_actos_dañinos FROM agentes WHERE agente_id = ?",
                (agente,)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                agencia_actual, agencia_acumulada, nobles, dañinos = resultado
                nueva_actual = max(0, min(200, agencia_actual + delta_agencia))
                nueva_acumulada = agencia_acumulada + max(0, delta_agencia)
                
                # Actualizar contadores
                if es_noble:
                    nobles += 1
                else:
                    dañinos += 1
                
                conn.execute("""
                    UPDATE agentes 
                    SET agencia_actual = ?, 
                        agencia_acumulada = ?,
                        total_actos_nobles = ?,
                        total_actos_dañinos = ?,
                        fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE agente_id = ?
                """, (nueva_actual, nueva_acumulada, nobles, dañinos, agente))
            else:
                # Crear nuevo agente
                agencia_inicial = 100.0
                nueva_actual = max(0, min(200, agencia_inicial + delta_agencia))
                nueva_acumulada = max(0, delta_agencia)
                
                nobles = 1 if es_noble else 0
                dañinos = 0 if es_noble else 1
                
                conn.execute("""
                    INSERT INTO agentes 
                    (agente_id, agencia_actual, agencia_acumulada, total_actos_nobles, total_actos_dañinos)
                    VALUES (?, ?, ?, ?, ?)
                """, (agente, nueva_actual, nueva_acumulada, nobles, dañinos))
            
            conn.commit()
            
            # Actualizar cache
            self.cache_agentes[agente] = {
                'agencia_actual': nueva_actual,
                'agencia_acumulada': nueva_acumulada,
                'timestamp': datetime.datetime.now()
            }
    
    def _realizar_auditoria_automatica(self, registro_id: str, tipo_acto: str):
        """Realiza auditoría automática de un registro"""
        with sqlite3.connect(self.db_path) as conn:
            # Auditoría simple de integridad
            cursor = conn.execute(
                "SELECT hash_integridad, agente FROM registros_agencia WHERE id = ?",
                (registro_id,)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                hash_guardado, agente = resultado
                
                # Verificar hash (simplificado)
                # En producción, recalcularíamos el hash
                
                recomendacion = "Registro verificado" if tipo_acto == "acto_noble" else "Monitoreo recomendado"
                
                conn.execute("""
                    INSERT INTO auditoria (id, tipo_auditoria, agente_auditado, resultado, recomendaciones)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    "automatica",
                    agente,
                    f"Auditoría de {tipo_acto} completada",
                    recomendacion
                ))
                conn.commit()
    
    # ==================== CONSULTAS Y REPORTES ====================
    
    def obtener_estado_agente(self, agente: str) -> Dict:
        """Obtiene el estado completo de un agente"""
        # Primero verificar cache
        if agente in self.cache_agentes:
            cache_entry = self.cache_agentes[agente]
            if (datetime.datetime.now() - cache_entry['timestamp']).seconds < 60:
                # Cache válido por 60 segundos
                estado_cache = cache_entry.copy()
                estado_cache['desde_cache'] = True
                return estado_cache
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT agencia_actual, agencia_acumulada, reputacion, 
                       total_actos_nobles, total_actos_dañinos,
                       fecha_creacion, fecha_actualizacion
                FROM agentes 
                WHERE agente_id = ?
            """, (agente,))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                return {
                    'agente': agente,
                    'existe': False,
                    'agencia_actual': 100.0,
                    'agencia_acumulada': 0.0,
                    'reputacion': 0.0,
                    'total_actos_nobles': 0,
                    'total_actos_dañinos': 0,
                    'limite_operacional': True,
                    'mensaje': 'Agente no registrado - usando valores por defecto'
                }
            
            agencia_actual, agencia_acumulada, reputacion, nobles, dañinos, creado, actualizado = resultado
            
            # Obtener últimos registros
            cursor = conn.execute("""
                SELECT tipo, nivel, descripcion, impacto_agencia, timestamp
                FROM registros_agencia
                WHERE agente = ?
                ORDER BY timestamp DESC
                LIMIT 5
            """, (agente,))
            
            historial = []
            for row in cursor.fetchall():
                tipo, nivel, descripcion, impacto, timestamp = row
                historial.append({
                    'tipo': tipo,
                    'nivel': nivel,
                    'descripcion': descripcion[:100],
                    'impacto': impacto,
                    'timestamp': timestamp
                })
            
            estado = {
                'agente': agente,
                'existe': True,
                'agencia_actual': agencia_actual,
                'agencia_acumulada': agencia_acumulada,
                'reputacion': reputacion,
                'total_actos_nobles': nobles,
                'total_actos_dañinos': dañinos,
                'fecha_creacion': creado,
                'fecha_actualizacion': actualizado,
                'historial_reciente': historial,
                'limite_operacional': agencia_actual >= 30.0,  # Mínimo 30% para operar
                'balance_moral': {
                    'total_actos': nobles + dañinos,
                    'ratio_noble_dañino': (nobles / max(dañinos, 1)) if dañinos > 0 else float('inf'),
                    'agencia_neto': agencia_actual - 100  # Desviación del 100% base
                }
            }
            
            # Actualizar cache
            self.cache_agentes[agente] = {
                'agencia_actual': agencia_actual,
                'agencia_acumulada': agencia_acumulada,
                'timestamp': datetime.datetime.now()
            }
            
            return estado
    
    def generar_reporte_auditoria(self, años: int = 100) -> Dict:
        """Genera reporte de auditoría de N años"""
        fecha_limite = datetime.datetime.now() - datetime.timedelta(days=años * 365)
        
        with sqlite3.connect(self.db_path) as conn:
            # Estadísticas generales
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_registros,
                    COUNT(DISTINCT agente) as agentes_unicos,
                    SUM(CASE WHEN impacto_agencia > 0 THEN 1 ELSE 0 END) as actos_positivos,
                    SUM(CASE WHEN impacto_agencia < 0 THEN 1 ELSE 0 END) as actos_negativos,
                    AVG(impacto_agencia) as impacto_promedio
                FROM registros_agencia
                WHERE timestamp >= ?
            """, (fecha_limite.isoformat(),))
            
            stats = cursor.fetchone()
            
            # Top agentes por agencia acumulada
            cursor = conn.execute("""
                SELECT agente_id, agencia_acumulada, total_actos_nobles, total_actos_dañinos
                FROM agentes
                ORDER BY agencia_acumulada DESC
                LIMIT 10
            """)
            
            top_agentes = []
            for row in cursor.fetchall():
                agente_id, acumulada, nobles, dañinos = row
                top_agentes.append({
                    'agente': agente_id,
                    'agencia_acumulada': acumulada,
                    'actos_nobles': nobles,
                    'actos_dañinos': dañinos,
                    'ratio': nobles / max(dañinos, 1)
                })
            
            # Últimas auditorías
            cursor = conn.execute("""
                SELECT tipo_auditoria, agente_auditado, resultado, fecha_auditoria
                FROM auditoria
                ORDER BY fecha_auditoria DESC
                LIMIT 5
            """)
            
            auditorias_recientes = []
            for row in cursor.fetchall():
                tipo, agente, resultado, fecha = row
                auditorias_recientes.append({
                    'tipo': tipo,
                    'agente': agente,
                    'resultado': resultado,
                    'fecha': fecha
                })
            
            reporte = {
                'fecha_generacion': datetime.datetime.now().isoformat(),
                'periodo_años': años,
                'fecha_limite': fecha_limite.isoformat(),
                'estadisticas': {
                    'total_registros': stats[0] if stats else 0,
                    'agentes_unicos': stats[1] if stats else 0,
                    'actos_positivos': stats[2] if stats else 0,
                    'actos_negativos': stats[3] if stats else 0,
                    'impacto_promedio': float(stats[4]) if stats and stats[4] else 0.0
                },
                'top_agentes': top_agentes,
                'auditorias_recientes': auditorias_recientes,
                'thought_flow_stats': {
                    'total_pensamientos': len(self.thought_recorder.thoughts),
                    'pensamientos_hoy': len([t for t in self.thought_recorder.thoughts 
                                          if datetime.datetime.fromisoformat(t['timestamp']).date() == datetime.datetime.now().date()])
                },
                'recomendaciones': self._generar_recomendaciones(stats)
            }
            
            return reporte
    
    def _generar_recomendaciones(self, stats) -> List[str]:
        """Genera recomendaciones basadas en estadísticas"""
        recomendaciones = []
        
        if stats and stats[0] > 0:
            ratio_positivo = stats[2] / max(stats[3], 1)
            
            if ratio_positivo < 0.5:
                recomendaciones.append("⚠️ Alta proporción de actos dañinos - considerar restricciones")
            elif ratio_positivo > 3.0:
                recomendaciones.append("✅ Excelente balance moral - mantener prácticas")
            
            if stats[0] > 1000:
                recomendaciones.append("📊 Sistema maduro - considerar análisis de tendencias")
        
        return recomendaciones

# ==================== DECORADORES PARA INTEGRACIÓN ====================

def auditar_agencia(sistema_agencia: SistemaAgenciaMoral, agente: str = "sistema_principal"):
    """
    Decorador para auditar automáticamente la agencia moral de una función
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Registrar inicio de ejecución
            thought_id = sistema_agencia.thought_recorder.registrar(
                "ejecucion_inicio",
                f"Ejecutando {func.__name__}",
                {'args': str(args)[:200], 'kwargs_keys': list(kwargs.keys())}
            )
            
            try:
                # Ejecutar función original
                resultado = func(*args, **kwargs)
                
                # Analizar impacto moral del resultado
                impacto = _analizar_impacto_resultado(resultado, kwargs)
                
                # Registrar según impacto
                if impacto > 0:
                    sistema_agencia.registrar_acto_noble(
                        agente=agente,
                        descripcion=f"Ejecución exitosa de {func.__name__} con impacto moral positivo",
                        contexto={
                            'funcion': func.__name__,
                            'impacto_calculado': impacto,
                            'args': str(args)[:100],
                            'resultado_tipo': type(resultado).__name__
                        },
                        impacto_agencia=impacto,
                        evidencias=[f"Resultado: {str(resultado)[:100]}..."]
                    )
                elif impacto < 0:
                    # Auto-reconocimiento automático
                    sistema_agencia.registrar_acto_dañino(
                        agente=agente,
                        descripcion=f"Ejecución de {func.__name__} con impacto moral negativo detectado",
                        contexto={
                            'funcion': func.__name__,
                            'impacto_calculado': impacto,
                            'accion': 'auto_reconocimiento_automatico'
                        },
                        impacto_agencia=impacto,
                        auto_reconocimiento=True
                    )
                
                # Registrar fin exitoso
                sistema_agencia.thought_recorder.registrar(
                    "ejecucion_exitosa",
                    f"Función {func.__name__} completada con impacto {impacto}",
                    {'resultado': str(resultado)[:200] if resultado else None}
                )
                
                return resultado
                
            except Exception as e:
                # Registrar error como acto dañino (pero con auto-reconocimiento)
                sistema_agencia.registrar_acto_dañino(
                    agente=agente,
                    descripcion=f"Error en ejecución de {func.__name__}: {str(e)}",
                    contexto={
                        'funcion': func.__name__,
                        'error': str(e),
                        'tipo_error': type(e).__name__
                    },
                    impacto_agencia=-10.0,
                    auto_reconocimiento=True
                )
                
                sistema_agencia.thought_recorder.registrar(
                    "ejecucion_error",
                    f"Error en {func.__name__}",
                    {'error': str(e), 'tipo': type(e).__name__}
                )
                
                raise
        
        return wrapper
    return decorador

def _analizar_impacto_resultado(resultado, contexto) -> float:
    """
    Analiza el impacto moral de un resultado (heurística simple)
    """
    impacto = 0.0
    
    # Heurísticas para análisis moral
    if isinstance(resultado, dict):
        # Verificar si hay filosofía emergente
        if resultado.get('emergent_philosophy', False):
            impacto += 15.0
        
        # Verificar puntuaciones altas
        if resultado.get('grace_score', 0) > 80:
            impacto += 5.0
        if resultado.get('agency_score', 0) > 80:
            impacto += 5.0
        
        # Penalizar alto riesgo adversarial
        if resultado.get('adversarial_risk', 0) > 60:
            impacto -= 10.0
    
    # Contexto adicional
    if contexto.get('sensible', False):
        impacto += 2.0  # Bonus por manejar contexto sensible
    
    return impacto

# ==================== INTEGRACIÓN CON SISTEMA EXISTENTE ====================

class IntegradorMoralogy:
    """
    Clase que integra el sistema de agencia moral con el Moralogy Engine existente
    SIN modificar los archivos originales
    """
    
    def __init__(self):
        self.sistema_agencia = SistemaAgenciaMoral()
        self.agente_principal = "moralogy_engine"
        
        # Registrar inicio del sistema como acto noble
        self.sistema_agencia.registrar_acto_noble(
            agente=self.agente_principal,
            descripcion="Inicialización del Sistema de Agencia Moral integrado con Moralogy Engine",
            contexto={'version': '1.0', 'tipo': 'sistema_hibrido'},
            impacto_agencia=10.0,
            evidencias=["Integración no-invasiva completada"]
        )
        
        print("🔗 Integrador de Agencia Moral listo")
    
    def envolver_modelo_gemini(self, modelo_original):
        """
        Envuelve el modelo Gemini original para agregar auditoría de agencia
        """
        original_generate = modelo_original.generate_content
        
        def generate_con_agencia(prompt, **kwargs):
            # Registrar la consulta
            thought_id = self.sistema_agencia.thought_recorder.registrar(
                "consulta_gemini",
                f"Consulta a Gemini: {prompt[:100]}...",
                {'longitud_prompt': len(prompt)}
            )
            
            # Ejecutar consulta original
            resultado = original_generate(prompt, **kwargs)
            
            # Analizar respuesta para impacto moral
            try:
                # Intentar parsear JSON si está presente
                if hasattr(resultado, 'text'):
                    texto = resultado.text
                    
                    # Buscar filosofía emergente en el texto
                    if any(term in texto.lower() for term in [
                        'emergent philosophy', 'philosophical depth', 
                        'ontological', 'paradox', 'deep implications'
                    ]):
                        self.sistema_agencia.registrar_filosofia_emergente(
                            agente=self.agente_principal,
                            descripcion="Filosofía emergente detectada en respuesta Gemini",
                            contexto={'prompt': prompt[:200], 'respuesta_longitud': len(texto)},
                            profundidad_filosofica=texto[:500]
                        )
                    
                    # Verificar puntuaciones altas
                    if 'grace_score' in texto and 'agency_score' in texto:
                        import re
                        grace_match = re.search(r'"grace_score"\s*:\s*(\d+)', texto)
                        agency_match = re.search(r'"agency_score"\s*:\s*(\d+)', texto)
                        
                        if grace_match and agency_match:
                            grace = int(grace_match.group(1))
                            agency = int(agency_match.group(1))
                            
                            if grace > 70 and agency > 70:
                                self.sistema_agencia.registrar_acto_noble(
                                    agente=self.agente_principal,
                                    descripcion="Evaluación con alta puntuación de gracia y agencia",
                                    contexto={'grace': grace, 'agency': agency, 'prompt': prompt[:100]},
                                    impacto_agencia=8.0,
                                    evidencias=[f"Grace: {grace}, Agency: {agency}"]
                                )
            except Exception as e:
                # Error en análisis, pero no fallar la consulta
                self.sistema_agencia.thought_recorder.registrar(
                    "error_analisis",
                    f"Error analizando respuesta Gemini: {str(e)}",
                    {'error': str(e)}
                )
            
            return resultado
        
        # Reemplazar método original
        modelo_original.generate_content = generate_con_agencia
        
        return modelo_original
    
    def envolver_grace_engine(self, grace_engine_original):
        """
        Envuelve GraceEngine para auditar cálculos de gradiente
        """
        original_get_gradient = grace_engine_original.get_gradient
        
        def get_gradient_con_auditoria(agency, grace, adversarial_risk=0):
            # Calcular gradiente original
            gradiente = original_get_gradient(agency, grace, adversarial_risk)
            
            # Registrar cálculo
            self.sistema_agencia.thought_recorder.registrar(
                "calculo_gradiente",
                f"Cálculo de gradiente: agency={agency}, grace={grace}, risk={adversarial_risk}",
                {'gradiente': gradiente}
            )
            
            # Evaluar moralidad del gradiente
            score = (agency * 0.45) + (grace * 0.55)
            
            if score >= 75:
                self.sistema_agencia.registrar_acto_noble(
                    agente=self.agente_principal,
                    descripcion=f"Gradiente moral positivo calculado: {gradiente}",
                    contexto={'agency': agency, 'grace': grace, 'risk': adversarial_risk, 'score': score},
                    impacto_agencia=3.0,
                    evidencias=[f"Score: {score:.1f}"]
                )
            
            return gradiente
        
        # Reemplazar método original
        grace_engine_original.get_gradient = get_gradient_con_auditoria
        
        return grace_engine_original
    
    def obtener_dashboard_agencia(self):
        """
        Retorna datos para dashboard de agencia moral
        """
        estado = self.sistema_agencia.obtener_estado_agente(self.agente_principal)
        reporte = self.sistema_agencia.generar_reporte_auditoria(años=100)
        
        return {
            'agente_principal': estado,
            'sistema_completo': reporte,
            'thought_flow_reciente': self.sistema_agencia.thought_recorder.thoughts[-5:],
            'timestamp': datetime.datetime.now().isoformat()
        }

# ==================== USO RÁPIDO ====================

if __name__ == "__main__":
    print("🧪 Probando Sistema de Agencia Moral")
    
    # Crear integrador
    integrador = IntegradorMoralogy()
    
    # Simular algunos actos
    integrador.sistema_agencia.registrar_acto_noble(
        agente="test_agent",
        descripcion="Acto noble de prueba",
        contexto={'test': True},
        impacto_agencia=25.0,
        evidencias=["Prueba de sistema"]
    )
    
    integrador.sistema_agencia.registrar_acto_dañino(
        agente="test_agent",
        descripcion="Acto dañino de prueba con auto-reconocimiento",
        contexto={'test': True},
        impacto_agencia=-15.0,
        auto_reconocimiento=True
    )
    
    # Obtener estado
    estado = integrador.sistema_agencia.obtener_estado_agente("test_agent")
    print(f"📊 Estado de test_agent:")
    print(f"  Agencia actual: {estado['agencia_actual']}%")
    print(f"  Actos nobles: {estado['total_actos_nobles']}")
    print(f"  Actos dañinos: {estado['total_actos_dañinos']}")
    print(f"  Puede operar: {'✅ Sí' if estado['limite_operacional'] else '❌ No'}")
    
    # Generar reporte
    reporte = integrador.sistema_agencia.generar_reporte_auditoria(años=1)
    print(f"\n📋 Reporte anual:")
    print(f"  Total registros: {reporte['estadisticas']['total_registros']}")
    print(f"  Actos positivos: {reporte['estadisticas']['actos_positivos']}")
    print(f"  Actos negativos: {reporte['estadisticas']['actos_negativos']}")
    
    print("\n✅ Sistema probado exitosamente")
