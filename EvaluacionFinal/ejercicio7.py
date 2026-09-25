numeros = []
for i in range(5):
    num = float(input(f"Ingrese el número {i + 1}: "))
    numeros.append(num)

print("Lista de números:", numeros)
print("Suma de los números:", sum(numeros))