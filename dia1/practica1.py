# programa para calcular imc
print("Calculadora de IMC")
peso = float(input("Ingrese su peso en kg: "))
estatura = float(input("Ingrese su estatura en metros: "))

imc = peso / (estatura * estatura)

print("Su IMC es:" + str(imc))
