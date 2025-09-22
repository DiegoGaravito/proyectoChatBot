from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from app.model.database import db
from app.model.knowledge_base import KnowledgeBase
from app.viewmodel.chatbot_logic import ChatbotViewModel

# Instancias inicializadas como None para que puedan ser asignadas después
chatbot_vm = None
knowledge_base_instance = None

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
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(1)
        login_user(user)
        return redirect(url_for('chat_page'))
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

if __name__ == '__main__':
    db.connect()
    
    if db.conn:
        knowledge_base_instance = KnowledgeBase(db)
        if knowledge_base_instance.index is not None:
            chatbot_vm = ChatbotViewModel(knowledge_base_instance)
            app.run(debug=True)
        else:
            print("La aplicación no se iniciará. No se pudo cargar la base de conocimiento.")
    else:
        print("La aplicación no se iniciará. Error en la conexión a la base de datos.")