#promedio y estado
notas = []
TAM = 3
sumatoria = 0

for x in range(TAM):
    nota = 0
    while nota < 1 or nota > 5:
        nota = int(input(f"Nota: {x + 1}: "))

    notas.append(nota)


for x in range(len(notas)):
    sumatoria = sumatoria + notas[x]

print("----------ESTADISTICAS----------")
print(f"Promedio: {sumatoria / TAM }")
estado = ""
if(float(sumatoria / TAM) > 1.7):
    estado = "APROBADO"
else:
    estado = "REPROBADO"

print(f"Estado: {estado}")