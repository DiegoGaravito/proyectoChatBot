from ..model.data_manager import data_manager

# Eliminamos la importación de knowledge_base_instance de aquí

class ChatbotViewModel:
    def __init__(self, knowledge_base_instance):
        self.data_manager = data_manager
        self.kb_instance = knowledge_base_instance # Asignamos la instancia

    def procesar_mensaje(self, id_usuario, mensaje):
        """
        Procesa el mensaje del usuario utilizando la base de conocimiento.
        """
        match = self.kb_instance.search_relevant_answer(mensaje)
        
        if match:
            respuesta_chatbot = match['respuesta']
        else:
            respuesta_chatbot = "Lo siento, no tengo información sobre ese tema. Por favor, intenta de nuevo con otra pregunta o contacta al administrador."
        
        self.data_manager.guardar_historial_chat(id_usuario, mensaje, respuesta_chatbot)
        
        return respuesta_chatbot
# Eliminamos la inicialización de chatbot_vm aquí