import wikipedia

wikipedia.set_lang("es")

class Chatbot:
    def __init__(self, nombre):
        self.nombre = nombre
        self.base_conocimiento = {
            "hola": "Hola, ¿En qué puedo ayudarte?",
            "python": "Python es un lenguaje de programación fácil de aprender y muy usado en IA, automatización y web.",
            "programacion": "La programación es el proceso de escribir instrucciones para que una computadora resuelva tareas.",
        }
        self.historial = []
        self.usuario = None

    def responder(self, mensaje):
        mensaje_original = mensaje.strip()
        mensaje = mensaje.lower().strip()
        self.historial.append(mensaje)

        if mensaje in ("historial", "mi historial", "ver historial"):
            if len(self.historial) <= 1:
                return "Todavía no hay mensajes en tu historial."

            historial_formateado = "\n".join(
                f"{i + 1}. {texto}" for i, texto in enumerate(self.historial[:-1])
            )
            return f"Historial de conversación:\n{historial_formateado}"

        if mensaje.startswith("me llamo "):
            nombre = mensaje_original[len("me llamo "):].strip()
            if nombre:
                self.usuario = nombre
                return f"Hola, {self.usuario}! ¿En qué puedo ayudarte?"

        for clave, respuesta in self.base_conocimiento.items():
            if clave in mensaje:
                if self.usuario:
                    return f"{respuesta}"
                return respuesta
        try:
            return wikipedia.summary(mensaje, sentences=2)
        except Exception:
            return "No entendí tu mensaje, ¿Podrías reformularlo?"
        
    def agregar_conocimiento(self, clave, respuesta):
        self.base_conocimiento[clave.lower()] = respuesta

def main():
    bot = Chatbot("Miki")
    print(f"{bot.nombre}: Hola, ¿en que puedo ayudarte?")

    while True:
        entrada = input("Tú: ")
        if entrada.lower() == "salir":
            print(f"{bot.nombre}: ¡Hasta pronto!")
            break

        respuesta = bot.responder(entrada)
        print(f"{bot.nombre}: {respuesta}")


if __name__ == "__main__":
    main()
