"""
Definiciones de estado para el sistema de creación de monólogos
"""
from typing import TypedDict, Dict, Any


class MonologoState(TypedDict):
    """Estado del grafo de LangGraph para la creación de monólogos"""
    inputs: Dict[str, Any]  # Inputs del usuario (tema, tono, duración, audiencia)
    monologo: str  # Monólogo generado
    feedback_a: str  # Feedback del revisor A (estructura)
    feedback_b: str  # Feedback del revisor B (lenguaje/emoción)
    resumen_feedback: str  # Resumen de feedback para correcciones
    iteracion: int  # Número de iteración actual
    max_iteraciones: int  # Máximo número de iteraciones permitidas
    estado: str  # Estado actual: "creando", "revisando", "evaluando", "finalizado", "error"
    archivo_guardado: str  # Ruta del archivo guardado
