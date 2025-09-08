import MySQLdb

class Database:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establece la conexión con la base de datos."""
        try:
            self.conn = MySQLdb.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                db=self.db,
                autocommit=True # Para que los cambios se guarden automáticamente
            )
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos exitosa.")
        except MySQLdb.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL y retorna los resultados."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except MySQLdb.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

# Instancia global de la base de datos
# Reemplaza los valores con tu configuración de MySQL
db = Database(
    host="bxqbroqqqkbw54z7f0ke-mysql.services.clever-cloud.com",
    user="uzejlwvrdvvnnbxn",
    password="pVMUV7bJoIk2BdbQ6LUa",
    db="bxqbroqqqkbw54z7f0ke"
)