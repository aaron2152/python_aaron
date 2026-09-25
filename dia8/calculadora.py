class Calculadora:
    numero1 = None
    numero2 = None

    def __init__(self):
        self.numero1 = 0
        self.numero2 = 0

    def sumar(self):
        return self.numero1 + self.numero2
    
    def restar(self):
        return self.numero1 - self.numero2
    
    def multiplicar(self):
        return self.numero1 * self.numero2
    
    def dividir(self):
        if self.numero1 != 0:
            return self.numero1 / self.numero2
        else:
            return f"el divisor no puede ser cero"

class CalculadoraCientifica(Calculadora):
    """Calculadora cientifica hereda de calculadora"""
    historial = None

    def __init__(self):
        super()
        self.historial = []

    def factorial(self, n):
        fact = 1
        for x in range(2,n+1):
            fact = fact * x
        self.historial.append(f"{n}! = {fact}")
        return fact
    
class CalculadoraProgramador(Calculadora):

    def __init__(self):
        super().__init__()

    def a_binario(self,n):
        return bin(n)
    
casio = Calculadora()
casio.numero1 = 10
casio.numero2 = 3
print(casio.sumar())
print(casio.restar())
print(casio.multiplicar())
print(casio.dividir())

print("Calculadora cientifica")
casiofx = CalculadoraCientifica()

casiofx.numero1 = 20
casiofx.numero2 = 5
print(casiofx.sumar())
print(casiofx.restar())
print(casiofx.multiplicar())
print(casiofx.dividir())
print(casiofx.factorial(5))

print("-----------------------")
print(casiofx.historial)

print("Calculadora Programador")

calcufxp = CalculadoraProgramador()
n = 10
print(f"Decimal {n} a binario {calcufxp.a_binario(n)}")