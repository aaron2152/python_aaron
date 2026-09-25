import mysql.connector

class ModeloTraduccion:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bd_traducciones_aaron"
        )

    def agregar_palabra(self, espanol, ingles):
        cursor = self.conexion.cursor()
        # Uso de consultas preparadas (%s) para evitar inyección SQL
        sql = "INSERT INTO traducciones VALUES (DEFAULT, %s, %s)"
        cursor.execute(sql, (espanol, ingles))
        self.conexion.commit()
        cursor.close()

    def buscar_palabra(self, espanol):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM traducciones WHERE palabra_espanol = %s"
        cursor.execute(sql, (espanol,))
        
        # Obtenemos la fila directamente
        resultado = cursor.fetchone()
        cursor.close()
        
        # Si encuentra la palabra, retorna solo la traducción (asumiendo que la columna 2 es el inglés)
        if resultado:
            return resultado[2]  # O la tupla completa 'resultado' si la prefieres
        
        return None