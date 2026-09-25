def calcular_cuota(capital, tasa_anual, cantidad_cuota):
    interes_total = capital * (tasa_anual/100)
    monto_total = capital + interes_total
    cuota = monto_total / cantidad_cuota
    return cuota
while True:
    print("Calculadora de Cuotas")
    c = int(input("Ingrese el monto a prestar: "))
    t = float(input("Ingrese la tasa anual: "))
    cu = int(input("Ingrese la cantidad de cuotas: "))

    print(f"Su cuota mensual será de: {calcular_cuota(c, t, cu)}")
