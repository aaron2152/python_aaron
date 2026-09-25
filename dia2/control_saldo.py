saldo_disponible = 25000000
saldo_transferencia = int(input("Ingrese el monto a transferir: "))

if saldo_transferencia > saldo_disponible:
    print("Saldo insuficiente")
else:

    saldo_disponible -= saldo_transferencia
    print("Transferencia realizada con éxito")
    print("Su saldo disponible es: " + str(saldo_disponible))