"""
Nodos del grafo para el sistema de creación de monólogos
"""
from state import MonologoState
from config import get_model
from tools import guardar_monologo
from prompts import PROMPT_CREADOR, PROMPT_REVISOR_A, PROMPT_REVISOR_B, PROMPT_EVALUADOR

# Obtener el modelo configurado
model = get_model()


def nodo_actor(state: MonologoState) -> MonologoState:
    """
    Nodo que simula la entrada del actor (inputs iniciales)
    
    Args:
        state: Estado actual del grafo
    
    Returns:
        Estado actualizado con inputs iniciales
    """
    print("🎭 Actor: Proporcionando inputs para el monólogo...")
    
    # Si no hay inputs, usar valores por defecto
    if not state.get("inputs"):
        state["inputs"] = {
            "tema": "La vida moderna",
            "tono": "reflexivo",
            "duracion": "2-3 minutos",
            "audiencia": "adultos jóvenes"
        }
    
    state["estado"] = "inputs_recibidos"
    return state


def nodo_creador(state: MonologoState) -> MonologoState:
    """
    Nodo creador de monólogos
    
    Args:
        state: Estado actual del grafo
    
    Returns:
        Estado actualizado con el monólogo generado
    """
    print("✍️ Creador: Generando monólogo...")
    
    inputs = state["inputs"]
    
    # Si hay feedback previo, incluirlo en el prompt
    feedback_context = ""
    if state.get("resumen_feedback"):
        feedback_context = f"\n\nFEEDBACK PREVIO A CORREGIR:\n{state['resumen_feedback']}"
    
    prompt_text = PROMPT_CREADOR.format(
        tema=inputs["tema"],
        tono=inputs["tono"],
        duracion=inputs["duracion"],
        audiencia=inputs["audiencia"],
        feedback_context=feedback_context
    )
    response = model.generate_content(prompt_text)
    
    state["monologo"] = response.text
    state["estado"] = "monologo_creado"
    
    if not state.get("iteracion"):
        state["iteracion"] = 1
    else:
        state["iteracion"] += 1
        
    return state


def nodo_revisor_a(state: MonologoState) -> MonologoState:
    """
    Revisor especializado en estructura y narrativa
    
    Args:
        state: Estado actual del grafo
    
    Returns:
        Estado actualizado con feedback de estructura
    """
    print("🔍 Revisor A: Analizando estructura narrativa...")
    
    prompt_text = PROMPT_REVISOR_A.format(monologo=state["monologo"])
    response = model.generate_content(prompt_text)
    state["feedback_a"] = response.text
    return state


def nodo_revisor_b(state: MonologoState) -> MonologoState:
    """
    Revisor especializado en lenguaje y conexión emocional
    
    Args:
        state: Estado actual del grafo
    
    Returns:
        Estado actualizado con feedback de lenguaje y emoción
    """
    print("🎨 Revisor B: Analizando lenguaje y conexión emocional...")
    
    prompt_text = PROMPT_REVISOR_B.format(
        monologo=state["monologo"],
        audiencia=state["inputs"]["audiencia"],
        tono=state["inputs"]["tono"]
    )
    response = model.generate_content(prompt_text)
    state["feedback_b"] = response.text
    return state


def nodo_evaluador(state: MonologoState) -> MonologoState:
    """
    Evaluador que decide si el monólogo está listo o necesita más trabajo
    
    Args:
        state: Estado actual del grafo
    
    Returns:
        Estado actualizado con decisión de evaluación
    """
    print("⚖️ Evaluador: Analizando feedback y tomando decisión...")
    
    prompt_text = PROMPT_EVALUADOR.format(
        feedback_a=state["feedback_a"],
        feedback_b=state["feedback_b"],
        iteracion=state["iteracion"],
        max_iteraciones=state.get("max_iteraciones", 3)
    )
    response = model.generate_content(prompt_text)
    content = response.text
    
    # Parsear la decisión
    if "DECISIÓN: OK" in content or content.strip().upper().startswith("OK"):
        state["estado"] = "aprobado"
        print("✅ Evaluador: Monólogo APROBADO")
    else:
        state["estado"] = "necesita_revision"
        # Extraer el resumen
        if "RESUMEN:" in content:
            state["resumen_feedback"] = content.split("RESUMEN:")[1].strip()
        else:
            state["resumen_feedback"] = content
        print("❌ Evaluador: Monólogo necesita REVISIÓN")
    
    return state


def nodo_mcp(state: MonologoState) -> MonologoState:
    """
    Nodo MCP para guardar el monólogo finalizado
    
    Args:
        state: Estado actual del grafo
    
    Returns:
        Estado actualizado con información del archivo guardado
    """
    print("💾 MCP: Guardando monólogo finalizado...")
    
    # Crear nombre de archivo basado en el tema
    tema_safe = state["inputs"]["tema"].replace(" ", "_").lower()
    nombre_archivo = f"monologo_{tema_safe}_{state['iteracion']}.txt"
    
    # Guardar el monólogo
    resultado = guardar_monologo(state["monologo"], nombre_archivo)
    
    state["archivo_guardado"] = nombre_archivo
    state["estado"] = "finalizado"
    
    print(f"✅ {resultado}")
    return state
