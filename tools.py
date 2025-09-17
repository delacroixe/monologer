"""
Herramientas y utilidades para el sistema de monólogos
"""


def guardar_monologo(monologo: str, nombre_archivo: str = None) -> str:
    """
    Simula el guardado de un monólogo usando MCP
    
    Args:
        monologo: El texto del monólogo a guardar
        nombre_archivo: Nombre del archivo (opcional)
    
    Returns:
        Mensaje de confirmación o error
    """
    if nombre_archivo is None:
        nombre_archivo = f"monologo_{hash(monologo) % 10000}.txt"
    
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(monologo)
        return f"Monólogo guardado exitosamente en: {nombre_archivo}"
    except Exception as e:
        return f"Error al guardar el archivo: {str(e)}"


def decidir_siguiente_paso(state) -> str:
    """
    Decide el siguiente paso basándose en la evaluación
    
    Args:
        state: Estado actual del grafo
    
    Returns:
        Nombre del siguiente nodo a ejecutar
    """
    if state["estado"] == "aprobado":
        return "mcp"
    elif state["iteracion"] >= state.get("max_iteraciones", 3):
        print("⚠️ Máximo de iteraciones alcanzado. Finalizando proceso.")
        return "mcp"
    else:
        return "creador"
