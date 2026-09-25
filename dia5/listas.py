dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
ventas = [1200,1450,980,1600,1750,2100,1330]

total = sum(ventas)

promedio = sum(ventas) / len(ventas)

indice_mayor = ventas.index(max(ventas))
print(f"Total de ventas de la semana: {total}")
print(f"Promedio de ventas diarias: {promedio:.2f}")
print(f"El día con más ventas: {dias[indice_mayor]}")
