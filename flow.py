"""
Definición del flujo de LangGraph para el sistema de creación de monólogos
"""
from langgraph.graph import StateGraph, END
from state import MonologoState
from nodes import (
    nodo_actor,
    nodo_creador,
    nodo_revisor_a,
    nodo_revisor_b,
    nodo_evaluador,
    nodo_mcp
)
from tools import decidir_siguiente_paso


def crear_grafo_monologo():
    """
    Crea y configura el grafo de LangGraph
    
    Returns:
        Grafo compilado listo para ejecutar
    """
    # Crear el grafo de estado
    workflow = StateGraph(MonologoState)
    
    # Agregar nodos
    workflow.add_node("actor", nodo_actor)
    workflow.add_node("creador", nodo_creador)
    workflow.add_node("revisor_a", nodo_revisor_a)
    workflow.add_node("revisor_b", nodo_revisor_b)
    workflow.add_node("evaluador", nodo_evaluador)
    workflow.add_node("mcp", nodo_mcp)
    
    # Definir el flujo
    workflow.set_entry_point("actor")
    workflow.add_edge("actor", "creador")
    workflow.add_edge("creador", "revisor_a")
    workflow.add_edge("creador", "revisor_b")
    workflow.add_edge("revisor_a", "evaluador")
    workflow.add_edge("revisor_b", "evaluador")
    
    # Decisión condicional desde el evaluador
    workflow.add_conditional_edges(
        "evaluador",
        decidir_siguiente_paso,
        {
            "creador": "creador",
            "mcp": "mcp"
        }
    )
    
    workflow.add_edge("mcp", END)
    
    return workflow.compile()


def ejecutar_sistema_monologo(inputs_usuario=None, max_iteraciones=3):
    """
    Ejecuta el sistema completo de creación de monólogos
    
    Args:
        inputs_usuario: Diccionario con inputs del usuario (tema, tono, etc.)
        max_iteraciones: Número máximo de iteraciones permitidas
    
    Returns:
        Resultado final del proceso o None si hay error
    """
    print("🎭 Iniciando sistema de creación de monólogos...")
    print("=" * 50)
    
    # Estado inicial
    estado_inicial = {
        "inputs": inputs_usuario,
        "monologo": "",
        "feedback_a": "",
        "feedback_b": "",
        "resumen_feedback": "",
        "iteracion": 0,
        "max_iteraciones": max_iteraciones,
        "estado": "iniciando",
        "archivo_guardado": ""
    }
    
    # Crear y ejecutar el grafo
    grafo = crear_grafo_monologo()
    
    try:
        # Ejecutar el flujo
        resultado_final = grafo.invoke(estado_inicial)
        
        print("\n" + "=" * 50)
        print("🎉 PROCESO COMPLETADO")
        print("=" * 50)
        print(f"📊 Iteraciones realizadas: {resultado_final['iteracion']}")
        print(f"📁 Archivo guardado: {resultado_final.get('archivo_guardado', 'No guardado')}")
        print(f"📝 Estado final: {resultado_final['estado']}")
        
        print("\n📖 MONÓLOGO FINAL:")
        print("-" * 30)
        print(resultado_final['monologo'])
        
        return resultado_final
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {str(e)}")
        return None
