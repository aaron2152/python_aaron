class Chatbot:
    def __init__(self, nombre):
        self.nombre = nombre
        self.base_conocimiento = {
            "hola": "Hola, ¿En qué puedo ayudarte?",
            "python": "Python es un lenguaje de programación fácil de aprender y muy usado en IA, automatización y web.",
            "programacion": "La programación es el proceso de escribir instrucciones para que una computadora resuelva tareas.",
            "algoritmo": "Un algoritmo es una serie ordenada de pasos para resolver un problema o realizar una tarea.",
            "poo": "La POO (Programación Orientada a Objetos) organiza el código en clases y objetos para reutilizar lógica y modelar entidades del mundo real.",
            "variable": "Una variable es un espacio de memoria que guarda un valor, como un número, texto o lista.",
            "funcion": "Una función es un bloque reutilizable de código que realiza una tarea específica y puede recibir parámetros.",
            "lista": "Una lista es una estructura de datos que permite guardar varios elementos en un orden determinado.",
            "bucle": "Un bucle permite repetir instrucciones varias veces, como un for o un while.",
            "condicion": "Una condición evalúa si algo es verdadero o falso y decide qué acción ejecutar.",
            "if": "El if se usa para ejecutar un bloque de código cuando una condición es verdadera.",
            "for": "El for sirve para recorrer colecciones de datos o ejecutar una acción repetida un número definido de veces.",
            "while": "El while repite un bloque de código mientras una condición siga siendo verdadera.",
            "clase": "Una clase es un plano o plantilla que define atributos y comportamientos para crear objetos.",
            "objeto": "Un objeto es una instancia de una clase que tiene estado y puede realizar acciones mediante sus métodos.",
            "metodo": "Un método es una función dentro de una clase que describe el comportamiento de un objeto.",
            "base de datos": "Una base de datos es un sistema para guardar, organizar y consultar información de forma estructurada.",
            "sql": "SQL es un lenguaje utilizado para gestionar y consultar bases de datos relacionales.",
            "html": "HTML es el lenguaje de marcado que define la estructura de una página web.",
            "css": "CSS se usa para dar estilo visual a una página web, como colores, tamaños y layouts.",
            "javascript": "JavaScript permite agregar interactividad a páginas web y controlar eventos en el navegador.",
            "aplicacion": "Una aplicación es un programa diseñado para cumplir una función útil para usuarios, como una app o un sitio web.",
            "depuracion": "La depuración es el proceso de detectar y corregir errores en el código para que el programa funcione correctamente."
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

        if self.usuario:
            return f"{self.usuario} No entendí tu mensaje, ¿Podrías reformularlo?"

        return "No entendi tu mensaje, ¿Podrías reformularlo?"
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
