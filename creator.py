from datetime import datetime

def generar_html(tema, tipo_conversacion, min_respuestas, conversacion, texto_academico):
    """
    Genera un archivo HTML que contiene la conversación y el texto académico.

    Args:
        tema (str): El tema de la conversación.
        tipo_conversacion (str): El tipo de conversación (amigos, trabajo, academicos).
        min_respuestas (int): El número mínimo de respuestas en la conversación.
        conversacion (list): Una lista de tuplas que representan la conversación.
        texto_academico (str): El texto académico generado.

    Returns:
        str: El contenido HTML generado.
    """
    # Obtiene la fecha y hora actual
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S")

    # Construye el contenido HTML
    html = f"""
<!DOCTYPE html>
<html>
  <head>
    <title>Conversación sobre {tema} - {timestamp}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
      .chat-container {{
        max-height: 500px;
        overflow-y: auto;
      }}
      .chat-message {{
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
      }}
      .user-message {{
        background-color: #e2e2e2;
        text-align: right;
      }}
      .assistant-message {{
        background-color: #f2f2f2;
        text-align: left;
      }}
      .copy-button {{
        margin-top: 10px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Conversación sobre {tema}</h1>
      <div class="chat-container">
    """

    # Agrega cada mensaje de la conversación al HTML
    for mensaje in conversacion:
        if mensaje[0] == "Tú:":
            html += f"""
        <div class="chat-message user-message">
          <p>{mensaje[1]}</p>
        </div>
            """
        else:
            html += f"""
        <div class="chat-message assistant-message">
          <p>{mensaje[1]}</p>
        </div>
            """

    # Agrega el texto académico y los botones para copiar al HTML
    html += f"""
      </div>
      <button class="btn btn-primary copy-button" onclick="copyConversation()">Copiar conversación</button>
      <h2>Texto académico sobre el tema</h2>
      <div class="academic-text">
        {texto_academico}
        <button class="btn btn-primary copy-button" onclick="copyAcademicText()">Copiar texto académico</button>
      </div>
    </div>
    <script>
      function copyConversation() {{
        const conversationContainer = document.querySelector('.chat-container');
        const conversationText = conversationContainer.innerText;
        navigator.clipboard.writeText(conversationText)
          .then(() => showCopyMessage('Conversación copiada al portapapeles'))
          .catch(err => console.error('Error al copiar la conversación:', err));
      }}

      function copyAcademicText() {{
        const academicText = document.querySelector('.academic-text').innerText;
        navigator.clipboard.writeText(academicText)
          .then(() => showCopyMessage('Texto académico copiado al portapapeles'))
          .catch(err => console.error('Error al copiar el texto académico:', err));
      }}

      function showCopyMessage(message) {{
        const copyMessage = document.createElement('div');
        copyMessage.textContent = message;
        copyMessage.style.position = 'fixed';
        copyMessage.style.bottom = '20px';
        copyMessage.style.left = '50%';
        copyMessage.style.transform = 'translateX(-50%)';
        copyMessage.style.backgroundColor = '#28a745';
        copyMessage.style.color = '#fff';
        copyMessage.style.padding = '10px';
        copyMessage.style.borderRadius = '5px';
        document.body.appendChild(copyMessage);

        setTimeout(() => {{
          copyMessage.remove();
        }}, 3000);
      }}
    </script>
  </body>
</html>
"""

    return html
