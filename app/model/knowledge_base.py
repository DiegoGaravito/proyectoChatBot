# app/model/knowledge_base.py
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
# No importes 'db' directamente aquí
from .database import db # Mantén esta línea para la instancia global

class KnowledgeBase:
    def __init__(self, database_instance):
        self.db = database_instance # Asigna la instancia de la base de datos
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.index = None
        self.knowledge_data = []
        self.load_knowledge_from_db()

    def load_knowledge_from_db(self):
        """Carga los datos de la base de datos y crea el índice de búsqueda."""
        # Usa la instancia pasada al constructor, ya conectada
        query = "SELECT id_pr, texto_pregunta, texto_respuesta FROM preguntas_respuestas"
        resultados = self.db.execute_query(query)
        
        if not resultados:
            print("No hay datos para cargar en la base de conocimiento.")
            return

        self.knowledge_data = [{'id': row[0], 'pregunta': row[1], 'respuesta': row[2]} for row in resultados]
        
        # Crear embeddings para las preguntas
        questions = [item['pregunta'] for item in self.knowledge_data]
        embeddings = self.model.encode(questions)
        
        # Crear un índice FAISS para la búsqueda rápida
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype('float32'))
        print("Base de conocimiento cargada y FAISS indexado.")

# NO crees la instancia global aquí, la haremos en main.py