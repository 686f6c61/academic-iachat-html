import os
import openai
import re
from creator import generar_html
import markdown

# Configura tu clave de API de OpenAI
openai.api_key = "API_KEY_OPENAI"

def openai_response(tema, ultima_respuesta, tipo_conversacion, conversacion):
    """
    Genera una respuesta de OpenAI basada en el tema, la última respuesta, el tipo de conversación y la conversación previa.

    Args:
        tema (str): El tema de la conversación.
        ultima_respuesta (str): La última respuesta en la conversación.
        tipo_conversacion (str): El tipo de conversación (amigos, trabajo, academicos).
        conversacion (list): Una lista de tuplas que representan la conversación previa.

    Returns:
        str: La respuesta generada por OpenAI.
    """
    if not ultima_respuesta:
        # Genera un prompt inicial basado en el tipo de conversación
        if tipo_conversacion == "amigos":
            prompt = f"Respuesta de un amigo sobre {tema}. Es un tema interesante, ¿qué opinas?"
        elif tipo_conversacion == "trabajo":
            prompt = f"Respuesta de un compañero de trabajo sobre {tema}. Es un tema relevante para nuestra empresa, ¿cuál es tu perspectiva?"
        else:
            prompt = f"Respuesta de un académico especialista sobre {tema}. Es un tema complejo con múltiples facetas, ¿cuál es tu análisis?"
    else:
        # Genera un prompt basado en la última respuesta
        prompt = f"Respuesta sobre {tema} en respuesta a: {ultima_respuesta}. Tienes un punto interesante, pero también hay que considerar... [Agrega otro punto/perspectiva relevante]."

    # Llama a la API de OpenAI para generar una respuesta
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente inteligente que mantiene una conversación sobre un tema específico. Usa muletillas y frases naturales para que tus respuestas parezcan más humanas. Por ejemplo: 'Como te digo', 'Esto que a mí me parece es...', 'Y así', etc."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    respuesta = response.choices[0].message.content.strip()

    # Eliminar repeticiones de palabras o muletillas
    respuesta = re.sub(r'\b(\w+)\s+\1\b', r'\1', respuesta)

    # Agrega un resumen al final de la conversación si se han cubierto los puntos principales
    if len(conversacion) >= 2 * (len(conversacion) // 2):
        respuesta += " En resumen, creo que hemos cubierto los puntos principales sobre este tema."

    return respuesta

def generar_texto_academico(tema, conversacion):
    """
    Genera un texto académico basado en el tema y la conversación previa.

    Args:
        tema (str): El tema de la conversación.
        conversacion (list): Una lista de tuplas que representan la conversación previa.

    Returns:
        str: El texto académico generado por OpenAI.
    """
    # Construye el prompt para OpenAI
    prompt = f"Genera un texto académico sobre el tema '{tema}' basado en la siguiente conversación:\n\n"
    for mensaje in conversacion:
        prompt += f"{mensaje[0]}: {mensaje[1]}\n"
    prompt += "\nEl texto debe ser adecuado para publicarse en una revista científica. La introducción debe tener aproximadamente 300 palabras. La sección principal debe tener alrededor de 700 palabras. La conclusión debe tener aproximadamente 700 palabras. Incluye referencias al final."

    # Llama a la API de OpenAI para generar el texto académico
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente académico experto en generar textos académicos para publicaciones científicas."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    texto_academico = response.choices[0].message.content.strip()

    # Imprime el número de palabras del texto académico generado
    palabras = texto_academico.split()
    num_palabras = len(palabras)
    print(f"El texto académico generado tiene {num_palabras} palabras.")

    return texto_academico

def main():
    """
    Función principal del programa.
    """
    # Solicita al usuario el tema, el número mínimo de respuestas y el tipo de conversación
    tema = input("Introduce un tema para la conversación: ")
    min_respuestas = int(input("Introduce el número mínimo de respuestas: "))
    tipo_conversacion = input("Introduce el tipo de conversación (amigos, trabajo, academicos): ")

    conversacion = []
    ultima_respuesta = ""
    for _ in range(min_respuestas):
        # Genera una respuesta y la agrega a la conversación
        respuesta = openai_response(tema, ultima_respuesta, tipo_conversacion, conversacion)
        conversacion.append(("Tú:", ultima_respuesta))
        conversacion.append(("Asistente:", respuesta))
        print(f"Tú: {ultima_respuesta}")
        print(f"Asistente: {respuesta}")
        ultima_respuesta = respuesta

    # Genera el texto académico basado en la conversación
    texto_academico = generar_texto_academico(tema, conversacion)

    # Genera el archivo HTML con la conversación y el texto académico
    html = generar_html(tema, tipo_conversacion, min_respuestas, conversacion, markdown.markdown(texto_academico))

    # Crea el directorio "chats" si no existe
    os.makedirs("chats", exist_ok=True)

    # Guarda el archivo HTML
    filename = f"chats/conversacion_{tema.replace(' ', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"El archivo '{filename}' ha sido generado con éxito.")

if __name__ == "__main__":
    main()
