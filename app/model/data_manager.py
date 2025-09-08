from .database import db
from flask_bcrypt import generate_password_hash, check_password_hash

class DataManager:
    """Gestiona todas las operaciones CRUD del proyecto."""

    def __init__(self):
        self.db = db

    # ------------------ Gestión de Usuarios ------------------
    def crear_usuario(self, nombre_usuario, email, contrasena):
        """Inserta un nuevo usuario en la base de datos."""
        hash_contrasena = generate_password_hash(contrasena).decode('utf-8')
        query = "INSERT INTO usuarios (nombre_usuario, email, hash_contrasena) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (nombre_usuario, email, hash_contrasena))
        return self.db.cursor.lastrowid

    def obtener_usuario_por_email(self, email):
        """Busca un usuario por su email."""
        query = "SELECT * FROM usuarios WHERE email = %s"
        return self.db.execute_query(query, (email,))

    # ------------------ Gestión de Preguntas y Respuestas (PR) ------------------
    def obtener_respuesta_por_pregunta(self, texto_pregunta):
        """Busca una respuesta a una pregunta."""
        # Esto es un ejemplo simple, más adelante podrías usar un modelo de PNL
        query = "SELECT texto_respuesta FROM preguntas_respuestas WHERE texto_pregunta LIKE %s LIMIT 1"
        return self.db.execute_query(query, (f'%{texto_pregunta}%',))

    def insertar_pr(self, texto_pregunta, texto_respuesta, id_tema, id_admin):
        """Inserta una nueva pregunta y respuesta y registra la acción."""
        query = "INSERT INTO preguntas_respuestas (texto_pregunta, texto_respuesta, id_tema) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (texto_pregunta, texto_respuesta, id_tema))
        
        id_pr = self.db.cursor.lastrowid
        # Registrar la acción en la tabla de logs
        self.db.execute_query("INSERT INTO registros_pr (id_pr, id_admin, accion) VALUES (%s, %s, 'INSERTAR')", (id_pr, id_admin))
        return id_pr
    
    # ------------------ Gestión de Historial de Chat ------------------
    def guardar_historial_chat(self, id_usuario, mensaje, respuesta):
        """Guarda la conversación en el historial."""
        query = "INSERT INTO historial_chat (id_usuario, texto_mensaje, texto_respuesta) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (id_usuario, mensaje, respuesta))

# Instancia del gestor de datos
data_manager = DataManager()