"""
Sistema de creación de monólogos usando LangGraph y Google Gemini
Archivo principal que orquesta todo el sistema
"""
from flow import ejecutar_sistema_monologo


def main():
    """Función principal del sistema"""
    # Inputs de ejemplo
    inputs_ejemplo = {
        "tema": "La soledad en la era digital",
        "tono": "melancólico pero esperanzador",
        "duracion": "3-4 minutos",
        "audiencia": "adultos jóvenes y millennials"
    }
    
    print("🎭 Ejemplo de ejecución del sistema:")
    resultado = ejecutar_sistema_monologo(inputs_ejemplo, max_iteraciones=2)
    
    if resultado:
        print("\n✅ Sistema ejecutado exitosamente")
        print(f"📋 Resumen: Monólogo creado en {resultado['iteracion']} iteraciones")
    else:
        print("\n❌ Error en la ejecución del sistema")


if __name__ == "__main__":
    main()