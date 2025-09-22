from app.model.knowledge_base import knowledge_base

class ChatbotViewModel:
    def __init__(self, kb_instance):
        self.kb_instance = kb_instance

    def procesar_mensaje(self, id_usuario, mensaje):
        """Procesa el mensaje del usuario y obtiene una respuesta del chatbot."""
        
        # Lógica para procesar el mensaje
        
        # Usar el método corregido de la base de conocimiento
        respuesta_chatbot = self.kb_instance.find_similar_answer(mensaje)
        
        return respuesta_chatbot