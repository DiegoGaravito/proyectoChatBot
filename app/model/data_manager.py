import MySQLdb
from flask_bcrypt import check_password_hash
from .database import db # Agrega esta línea para importar db

class DataManager:
    def __init__(self, db_instance):
        self.db = db_instance
        self.bcrypt = None

    def obtener_usuario_por_id(self, user_id):
        """Obtiene los datos de un usuario por su ID, ya sea administrador o usuario regular."""
        # Intenta buscar al usuario como administrador
        query_admin = "SELECT id_admin as id, hash_contrasena, es_super_admin FROM administradores WHERE id_admin = %s"
        resultado = self.db.execute_query(query_admin, (user_id,))
        
        if resultado:
            columns = [desc[0] for desc in self.db.cursor.description]
            return dict(zip(columns, resultado[0]))
        
        # Si no es administrador, intenta buscarlo como usuario regular
        query_usuario = "SELECT id_usuario as id, hash_contrasena, '0' as es_super_admin FROM usuarios WHERE id_usuario = %s"
        resultado_usuario = self.db.execute_query(query_usuario, (user_id,))
        
        if resultado_usuario:
            columns = [desc[0] for desc in self.db.cursor.description]
            return dict(zip(columns, resultado_usuario[0]))
        
        return None

    def verificar_credenciales_admin(self, email, password):
        """Verifica las credenciales de un administrador."""
        query = "SELECT id_admin, hash_contrasena, es_super_admin FROM administradores WHERE email = %s"
        resultado = self.db.execute_query(query, (email,))
        
        if resultado and self.bcrypt:
            hash_contrasena_db = resultado[0][1]
            if self.bcrypt.check_password_hash(hash_contrasena_db, password):
                return {
                    'id': resultado[0][0], 
                    'es_super_admin': bool(resultado[0][2])
                }
        return None

    def verificar_credenciales_usuario(self, email, password):
        """Verifica las credenciales de un usuario regular."""
        query = "SELECT id_usuario, hash_contrasena FROM usuarios WHERE email = %s"
        resultado = self.db.execute_query(query, (email,))
        
        if resultado and self.bcrypt:
            hash_contrasena_db = resultado[0][1]
            if self.bcrypt.check_password_hash(hash_contrasena_db, password):
                return {
                    'id': resultado[0][0], 
                    'es_super_admin': 0  # 0 indica que no es un super_admin
                }
        return None
    
# Instancia global del DataManager
data_manager = DataManager(db)