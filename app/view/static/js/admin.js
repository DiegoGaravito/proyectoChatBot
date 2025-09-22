document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('add-knowledge-form');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const question = document.getElementById('question').value;
        const answer = document.getElementById('answer').value;
        
        const response = await fetch('/add_knowledge', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question, answer })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = data.mensaje;
            form.reset(); // Limpia el formulario
        } else {
            messageDiv.textContent = 'Error: ' + data.error;
        }
    });
});