from ..model.data_manager import data_manager
# Importa solo la clase KnowledgeBase, no la instancia
from ..model.knowledge_base import KnowledgeBase

class ChatbotViewModel:
    def __init__(self, knowledge_base_instance):
        self.data_manager = data_manager
        self.kb_instance = knowledge_base_instance

    def procesar_mensaje(self, id_usuario, mensaje):
        match = self.kb_instance.search_relevant_answer(mensaje)
        
        if match:
            respuesta_chatbot = match['respuesta']
        else:
            respuesta_chatbot = "Lo siento, no tengo información sobre ese tema. Por favor, intenta de nuevo con otra pregunta o contacta al administrador."
        
        self.data_manager.guardar_historial_chat(id_usuario, mensaje, respuesta_chatbot)
        
        return respuesta_chatbot

# Eliminamos la inicialización de chatbot_vm aquí. Se hará en main.py.