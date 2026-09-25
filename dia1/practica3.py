#Ecuacion cuadratica
print("Resolver ecuaciones con la ec. cuadratica")
a = float(input("Ingrese el coeficiente de x2: "))
b = float(input("Ingrese el coeficiente de x: "))
c = float(input("Ingrese el termino independiente: "))

x1 = (-b + (b**2 - 4 * a * c)**(0.5)) / (2*a)
x2 = (-b - (b**2 - 4 * a * c)**(0.5)) / (2*a)

print("Solucion 1: " + str(x1))
print("Solucion 2: " + str(x2))