"""
Configuración del modelo Gemini para el sistema de monólogos
"""
import os
import google.generativeai as genai


# Configuración del modelo Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyAJ25_mMF41Y-Q3GefPGkffIbVIhTzMKM4"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")


def get_model():
    """Retorna la instancia del modelo Gemini configurado"""
    return model
