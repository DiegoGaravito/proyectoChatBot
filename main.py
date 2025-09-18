from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_session import Session  # Para manejar sesiones seguras
from app.model.database import db  # Importa la instancia global de Database
from app.model.knowledge_base import KnowledgeBase
from app.model.data_manager import data_manager  # Importa la instancia global de DataManager
from app.viewmodel.chatbot_logic import ChatbotViewModel

# Instancias inicializadas como None para que puedan ser asignadas después
chatbot_vm = None
knowledge_base_instance = None

app = Flask(__name__, template_folder='app/view', static_folder='app/view/static')
app.secret_key = 'KAREN123'  # Cambia esto por una clave segura
app.config['SESSION_TYPE'] = 'filesystem'  # Almacena sesiones en archivos
Session(app)

@app.route('/')
def index():
    """Página principal: Muestra chat si logueado, o redirige a login."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para registrar un nuevo usuario."""
    if request.method == 'POST':
        data = request.form
        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        try:
            user_id = data_manager.crear_usuario(nombre, email, password)
            if user_id:
                flash('Usuario registrado exitosamente. Ahora inicia sesión.')
                return redirect(url_for('login'))
            else:
                flash('Error al registrar. El email ya existe o datos inválidos.')
        except Exception as e:
            flash(f'Error: {str(e)}')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta para iniciar sesión."""
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        user_id = data_manager.verificar_login(email, password)  # Método que agregamos en data_manager
        if user_id:
            session['user_id'] = user_id
            flash('Login exitoso!')
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cierra la sesión."""
    session.pop('user_id', None)
    flash('Sesión cerrada.')
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'])
def chat():
    """Procesa mensajes del chat, solo si logueado."""
    if 'user_id' not in session:
        return jsonify({"error": "Debes iniciar sesión para chatear"}), 401
    
    data = request.json
    mensaje_usuario = data.get('mensaje')
    id_usuario = session['user_id']  # Usa el ID de la sesión
    
    if not mensaje_usuario:
        return jsonify({"error": "Mensaje vacío"}), 400

    if chatbot_vm:
        respuesta_chatbot = chatbot_vm.procesar_mensaje(id_usuario, mensaje_usuario)
        return jsonify({"respuesta": respuesta_chatbot})
    else:
        return jsonify({"error": "El servicio de chatbot no está disponible. Por favor, inténtalo más tarde."}), 503

if __name__ == '__main__':
    # La conexión a BD se hace automáticamente en database.py
    # Pero verificamos si está conectada
    if not db.conn:
        print("Error: No se pudo conectar a la BD. Revisa credenciales en database.py")
        exit(1)
    
    # Inicializar la base de conocimiento SOLO si la conexión fue exitosa
    print("Inicializando base de conocimiento...")
    knowledge_base_instance = KnowledgeBase(db)
    
    # Inicializar el ViewModel solo si la base de conocimiento se cargó correctamente
    if knowledge_base_instance and knowledge_base_instance.index:
        chatbot_vm = ChatbotViewModel(knowledge_base_instance)
        print("Chatbot inicializado correctamente.")
    else:
        print("Error: No se pudo inicializar la base de conocimiento. Verifica datos en BD.")
    
    # Ejecuta el servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)  # Para Codespaces