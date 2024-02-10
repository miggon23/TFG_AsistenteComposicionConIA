ticksPerQuarter = 2**4 * 3

class TimeSignature:

    def __init__(self, numerator =  4, denominator = 4):
        self.numerator = numerator
        self.denominator = denominator

    def measure_size(self):
        return self.numerator * (4 / self.denominator)
    
    def set_weights(self, weights):
        if len(weights) != self.numerator:
            raise Exception("El número de pesos debe ser igual al numerador")
        for weight in weights:
            if weight is not None and weight < 1:
                raise Exception("Existe al menos un peso cuyo valor es menor que 1")
        self.weights = weights

        return self