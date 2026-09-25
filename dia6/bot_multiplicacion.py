import random

puntaje = 0

for pregunta in range(5):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    respuesta = int(input(f"¿Cuánto es {num1} x {num2}? "))

    if respuesta == num1 * num2:
        puntaje += 1
        print("Correcto")
    else:
        print(f"Incorrecto. Era {num1 * num2}")

print(f"Puntaje final: {puntaje} de 5")
if(puntaje < 3):
    print("¡Sigue practicando!")   
elif puntaje >= 3:
    print("¡Bien hecho!")   