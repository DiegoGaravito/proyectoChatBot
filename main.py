from flask import Flask, request, jsonify, render_template
from app.model.database import db
from app.model.knowledge_base import KnowledgeBase
from app.viewmodel.chatbot_logic import ChatbotViewModel

# Instancias inicializadas como None para que puedan ser asignadas después
chatbot_vm = None
knowledge_base_instance = None

app = Flask(__name__, template_folder='app/view', static_folder='app/view/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    mensaje_usuario = data.get('mensaje')
    id_usuario = data.get('id_usuario')
    
    if not mensaje_usuario or not id_usuario:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    if chatbot_vm:
        respuesta_chatbot = chatbot_vm.procesar_mensaje(id_usuario, mensaje_usuario)
        return jsonify({"respuesta": respuesta_chatbot})
    else:
        return jsonify({"error": "El servicio de chatbot no está disponible. Por favor, inténtalo más tarde."}), 503

if __name__ == '__main__':
    # Conectar a la base de datos una sola vez
    db.connect()
    
    # Inicializar la base de conocimiento SOLO si la conexión fue exitosa
    if db.conn:
        knowledge_base_instance = KnowledgeBase(db)
        
        # Inicializar el ViewModel solo si la base de conocimiento se cargó
        if knowledge_base_instance.index:
            chatbot_vm = ChatbotViewModel(knowledge_base_instance)
        
    app.run(debug=True)