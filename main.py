# main.py
from flask import Flask, request, jsonify, render_template
from app.viewmodel.chatbot_logic import chatbot_vm
from app.model.database import db
from app.model.knowledge_base import KnowledgeBase

app = Flask(__name__, template_folder='app/view', static_folder='app/view/static')

@app.route('/')
def index():
    """Ruta para la página principal del chatbot."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para procesar los mensajes del chat."""
    data = request.json
    mensaje_usuario = data.get('mensaje')
    id_usuario = data.get('id_usuario')
    
    if not mensaje_usuario or not id_usuario:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    respuesta_chatbot = chatbot_vm.procesar_mensaje(id_usuario, mensaje_usuario)
    return jsonify({"respuesta": respuesta_chatbot})

if __name__ == '__main__':
    # CONECTAR a la base de datos una sola vez
    db.connect()

    # Luego, inicializar la base de conocimiento con la instancia conectada
    kb = KnowledgeBase(db)

    # Pasar la base de conocimiento a tu ViewModel
    # (Necesitarás modificar chatbot_logic.py para aceptar esto)
    # Por ahora, puedes hacer una prueba sencilla
    
    app.run(debug=True)