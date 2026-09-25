ingreso_mensual = 4800000
historial_positivo = True
deuda_actual = 50000000

if historial_positivo and ingreso_mensual >= deuda_actual * 3:
    print("Préstamo aprobado")
elif historial_positivo:
    print("Aprobado con monto reducido")
else:
    print("Préstamo rechazado")