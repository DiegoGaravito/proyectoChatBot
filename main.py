from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

# Importa la instancia de la base de datos
from app.model.database import db

# Importa la CLASE KnowledgeBase
from app.model.knowledge_base import KnowledgeBase

# Importa la instancia de data_manager
from app.model.data_manager import data_manager

# Importa el ViewModel
from app.viewmodel.chatbot_logic import ChatbotViewModel

# Instancias inicializadas
bcrypt = None
knowledge_base = None
chatbot_vm = None

app = Flask(__name__, template_folder='app/view', static_folder='app/view/static')
app.secret_key = 'una_clave_super_secreta' 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, is_admin=False):
        self.id = id
        self.is_admin = is_admin

    def is_admin_user(self):
        return self.is_admin

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    user_data = data_manager.obtener_usuario_por_id(user_id)
    if user_data:
        return User(user_data['id'], is_admin=bool(user_data['es_super_admin']))
    return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Intenta verificar las credenciales del administrador
        user_data = data_manager.verificar_credenciales_admin(email, password)
        
        # Si no es un admin, intenta con las credenciales de un usuario regular
        if not user_data:
            user_data = data_manager.verificar_credenciales_usuario(email, password)

        if user_data:
            user = User(user_data['id'], is_admin=bool(user_data['es_super_admin']))
            login_user(user)
            
            if user.is_admin_user():
                return redirect(url_for('admin_page'))
            else:
                return redirect(url_for('chat_page'))
        else:
            return render_template('login.html', error="Credenciales incorrectas")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def chat_page():
    return render_template('chatbot.html')

@app.route('/admin')
@login_required
def admin_page():
    if not current_user.is_admin_user():
        return "Acceso denegado", 403
    return render_template('admin.html')

@app.route('/chat_api', methods=['POST'])
@login_required
def chat_api():
    data = request.json
    mensaje_usuario = data.get('mensaje')
    id_usuario = current_user.id
    
    if not mensaje_usuario:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    if chatbot_vm:
        respuesta_chatbot = chatbot_vm.procesar_mensaje(id_usuario, mensaje_usuario)
        return jsonify({"respuesta": respuesta_chatbot})
    else:
        return jsonify({"error": "El servicio de chatbot no está disponible. Por favor, inténtalo más tarde."}), 503

@app.route('/add_knowledge', methods=['POST'])
@login_required
def add_knowledge():
    if not current_user.is_admin_user():
        return jsonify({"error": "Acceso denegado"}), 403

    data = request.get_json()
    pregunta = data.get('question')
    respuesta = data.get('answer')
    
    if not pregunta or not respuesta:
        return jsonify({"error": "La pregunta y la respuesta no pueden estar vacías"}), 400

    try:
        knowledge_base.agregar_conocimiento(pregunta, respuesta)
        return jsonify({"mensaje": "Conocimiento agregado con éxito."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    db.connect()
    
    if db.conn:
        bcrypt = Bcrypt(app)
        data_manager.bcrypt = bcrypt
        
        # Ahora, instancia la clase KnowledgeBase después de la conexión a la base de datos
        knowledge_base = KnowledgeBase(db)
        
        # Inicializa el ViewModel
        chatbot_vm = ChatbotViewModel(knowledge_base)
        
        app.run(debug=True)
    else:
        print("La aplicación no se iniciará. Error en la conexión a la base de datos.")