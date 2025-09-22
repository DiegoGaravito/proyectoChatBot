import numpy as np
import faiss

class KnowledgeBase:
    def __init__(self, db_instance):
        self.db = db_instance
        self.questions = []
        self.answers = []
        self.index = None
        self.load_knowledge_from_db()

    def load_knowledge_from_db(self, pregunta_admin=None, respuesta_admin=None):
        """Carga la base de conocimiento desde la base de datos."""
        query = "SELECT pregunta, respuesta FROM conocimiento_base"
        resultados = self.db.execute_query(query)

        if resultados:
            for pregunta, respuesta in resultados:
                self.questions.append(pregunta)
                self.answers.append(respuesta)
            self.build_index()
            print("Base de conocimiento cargada y FAISS indexado.")
        else:
            print("No se encontró conocimiento en la base de datos.")
            self.index = None

    def build_index(self):
        """Construye el índice FAISS para las preguntas."""
        # Aquí iría la lógica para generar los embeddings y construir el índice FAISS
        # Por ahora, un índice de ejemplo
        if self.questions:
            dummy_embeddings = np.random.rand(len(self.questions), 768).astype('float32')
            self.index = faiss.IndexFlatL2(768)
            self.index.add(dummy_embeddings)
        else:
            self.index = None

    def agregar_conocimiento(self, pregunta, respuesta):
        """Agrega una nueva pregunta y respuesta a la base de datos y al índice."""
        query = "INSERT INTO conocimiento_base (pregunta, respuesta) VALUES (%s, %s)"
        self.db.execute_query(query, (pregunta, respuesta))
        
        self.questions.append(pregunta)
        self.answers.append(respuesta)
        
        # Opcional: Reconstruir el índice para incluir el nuevo conocimiento
        self.build_index()

    def find_similar_answer(self, user_question):
        """Busca una respuesta similar a la pregunta del usuario."""
        if not self.index:
            return "No tengo información para esa pregunta. Por favor, contacta a un administrador."
        
        # Aquí iría la lógica para buscar en el índice FAISS
        # Por ahora, una simple búsqueda de ejemplo
        if any(keyword in user_question.lower() for keyword in ["hola", "saludo"]):
            return "¡Hola! Estoy aquí para ayudarte con tus preguntas de ciberseguridad. ¿En qué puedo asistirte?"
        
        return self.answers[0] if self.answers else "Lo siento, no tengo una respuesta para eso."