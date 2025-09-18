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
        return self.db.execute_query(query, (nombre_usuario, email, hash_contrasena))

    def obtener_usuario_por_email(self, email):
        """Busca un usuario por su email."""
        query = "SELECT * FROM usuarios WHERE email = %s"
        resultados = self.db.execute_query(query, (email,))
        return resultados[0] if resultados else None  # Retorna el primer usuario o None

    def verificar_login(self, email, contrasena):
        """Verifica credenciales y retorna ID de usuario si es válido."""
        usuario = self.obtener_usuario_por_email(email)
        if usuario and check_password_hash(usuario[3], contrasena):  # Ajustado a índice 3 si columnas son id=0, nombre=1, email=2, hash=3
            return usuario[0]  # Retorna ID (índice 0)
        return None

    # ------------------ Gestión de Preguntas y Respuestas (PR) ------------------
    def obtener_respuesta_por_pregunta(self, texto_pregunta):
        """Busca una respuesta a una pregunta (fallback si KB falla)."""
        query = "SELECT texto_respuesta FROM preguntas_respuestas WHERE texto_pregunta LIKE %s LIMIT 1"
        resultados = self.db.execute_query(query, (f'%{texto_pregunta}%',))
        return resultados[0][0] if resultados else None

    def insertar_pr(self, texto_pregunta, texto_respuesta, id_tema, id_admin):
        """Inserta una nueva pregunta y respuesta y registra la acción."""
        query = "INSERT INTO preguntas_respuestas (texto_pregunta, texto_respuesta, id_tema) VALUES (%s, %s, %s)"
        id_pr = self.db.execute_query(query, (texto_pregunta, texto_respuesta, id_tema))
        
        if id_pr:  # Registrar en logs si quieres (opcional)
            self.db.execute_query("INSERT INTO registros_pr (id_pr, id_admin, accion) VALUES (%s, %s, 'INSERTAR')", (id_pr, id_admin))
        return id_pr
    
    # ------------------ Gestión de Historial de Chat ------------------
    def guardar_historial_chat(self, id_usuario, mensaje, respuesta):
        """Guarda la conversación en el historial."""
        query = "INSERT INTO historial_chat (id_usuario, texto_mensaje, texto_respuesta) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (id_usuario, mensaje, respuesta))

# Instancia global
data_manager = DataManager()