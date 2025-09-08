# app/viewmodel/chatbot_logic.py
from ..model.knowledge_base import knowledge_base
from ..model.data_manager import data_manager

class ChatbotViewModel:
    def __init__(self):
        self.data_manager = data_manager

    def procesar_mensaje(self, id_usuario, mensaje):
        """
        Procesa el mensaje del usuario utilizando la base de conocimiento RAG.
        """
        # 1. Recuperación: Buscar la respuesta más relevante
        match = knowledge_base.search_relevant_answer(mensaje)
        
        if match:
            # 2. Generación (simple): La respuesta es la que se encontró
            respuesta_chatbot = match['respuesta']
        else:
            respuesta_chatbot = "Lo siento, no tengo información sobre ese tema. Por favor, intenta de nuevo con otra pregunta o contacta al administrador."
        
        self.data_manager.guardar_historial_chat(id_usuario, mensaje, respuesta_chatbot)
        
        return respuesta_chatbot