notas = {"Juan": 85, "María": 90, "Pedro": 78, "Ana": 92}

nombre = input("Ingrese el nombre del estudiante: ")

if nombre in notas:
    print(f"La nota de {nombre} es {notas[nombre]}")
else:
    print("Estudiante no encontrado.")