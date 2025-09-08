import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from .database import db

class KnowledgeBase:
    def __init__(self, database_instance):
        self.db = database_instance
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') 
        self.index = None
        self.knowledge_data = []
        self.load_knowledge_from_db()

    def load_knowledge_from_db(self):
        """Carga los datos de la base de datos y crea el índice de búsqueda."""
        if self.db.conn is None:
            print("Error: La conexión a la base de datos no está activa. No se puede cargar el conocimiento.")
            return

        query = "SELECT id_pr, texto_pregunta, texto_respuesta FROM preguntas_respuestas"
        resultados = self.db.execute_query(query)
        
        if not resultados:
            print("No hay datos para cargar en la base de conocimiento.")
            return

        self.knowledge_data = [{'id': row[0], 'pregunta': row[1], 'respuesta': row[2]} for row in resultados]
        
        questions = [item['pregunta'] for item in self.knowledge_data]
        embeddings = self.model.encode(questions)
        
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype('float32'))
        print("Base de conocimiento cargada y FAISS indexado.")

    def search_relevant_answer(self, query, k=1):
        """Busca la respuesta más relevante para una consulta."""
        if self.index is None:
            print("Error: El índice de la base de conocimiento no está cargado.")
            return None

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        
        if indices.size > 0:
            best_match_index = indices[0][0]
            return self.knowledge_data[best_match_index]
        return None