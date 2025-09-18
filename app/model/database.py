import MySQLdb

class Database:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.conn = None
        self.cursor = None
        self.connect()  # Auto-conectar al inicializar

    def connect(self):
        """Establece la conexión con la base de datos."""
        try:
            self.conn = MySQLdb.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                db=self.db,
                autocommit=True
            )
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos exitosa.")
        except MySQLdb.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conn = None

    def disconnect(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL. Para SELECT retorna resultados; para otros, commit y lastrowid."""
        if not self.conn:
            print("No hay conexión activa.")
            return None
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return self.cursor.lastrowid  # Para INSERTs
        except MySQLdb.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            if self.conn:
                self.conn.rollback()
            return None

# Instancia global (tu config de Clever Cloud)
db = Database(
    host="bxqbroqqqkbw54z7f0ke-mysql.services.clever-cloud.com",
    user="uzejlwvrdvvnnbxn",
    password="pVMUV7bJoIk2BdbQ6LUa",
    db="bxqbroqqqkbw54z7f0ke"
)