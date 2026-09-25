from urllib import request
from urllib.error import URLError, HTTPError
import unicodedata

lpo = ["coño", "bobo", "culiao", "pinche", "estupido", "estupida"]

def quitar_tildes(texto):
    """Función para eliminar tildes y caracteres diacríticos."""
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def verificar_web(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        req = request.Request(url, headers=headers)
        f = request.urlopen(req)
    except HTTPError as e:
        return f'¡Error HTTP {e.code} al acceder a la URL!'
    except URLError:
        return f'¡La url {url} no existe o no se puede alcanzar!'
    else:
        aux = f.read()
        try:
            contenido = aux.decode('utf-8').lower()
        except UnicodeDecodeError:
            contenido = aux.decode('latin-1').lower()
            
        # Limpiamos de tildes todo el contenido de la web
        contenido_limpio = quitar_tildes(contenido)
        palabras_encontradas = []
        
        for l in lpo:
            # Limpiamos también la palabra de la lista
            palabra_limpia = quitar_tildes(l)
            if palabra_limpia in contenido_limpio:
                palabras_encontradas.append(l)
                
        return palabras_encontradas

url = 'https://es.wiktionary.org/wiki/Wikcionario:Insultos_regionales'
print("\n----------------------------------------\n")
print("Informe de sitio:")
print(verificar_web(url))