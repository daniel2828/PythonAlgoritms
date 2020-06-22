# Importaciones
import unittest
from math import log
def generador_recurrencia(coeficientes, funcion_adicional, iniciales):
    """
    Generador de valores de acuerdo a una recurrencia:
    F(n) = coeficientes[0]*F(n-1) + coeficientes[1]*F(n-2) + ...
         + funcion_adicional(n)
    Los valores iniciales son F(0) = iniciales[0], F(1) = iniciales[1],...
    Los valores que se generan son F(0), F(1), F(2),...
    Se deben generar los valores de uno en uno, no hay que devolver varios.
    Debe generar valores indefinidamente, no hay que poner límites.
    Aunque sea una recurrencia, los valores *no* deben calcularse recursivamente.
    """

    contador = -1
    # Por cada elemento en iniciales sumo uno al contador
    for element in iniciales:
        contador += 1
        # Devuelvo el elemento ya que es parte de la recurrencia
        yield element
    # Bucle infinito para simular la generacion infinita de elementos
    while (True):
        contador += 1
        fValor = 0
        iContadorInterno = 1
        # Hacemos el calculo de la suma de los coeficientes por el valor inicial
        for coef in coeficientes:
            fValor += coef * iniciales[contador - iContadorInterno]
            iContadorInterno += 1
            # A lo calculado, le añadimos el valor del nuevo elemento
        fValor += funcion_adicional(contador)
        iniciales.append(fValor)
        yield fValor


class TestGeneradorRecurrencia(unittest.TestCase):

    @staticmethod
    def comprueba_recurrencia(coeficientes, funcion_adicional, iniciales,
                              funcion_alternativa, numero_comprobaciones=100,
                              epsilon=0.1):
        """
        Dada una recurrencia (definida en términos de sus coeficientes,
        condiciones inciales y la función_adicional) comprueba si los valores
        generados son (aproximadamente) los mismos que los definidos por una función
        alternativa, para un determinado número de comprobaciones.
        """

        iterador = generador_recurrencia(coeficientes, funcion_adicional,
                                         iniciales)
        for n in range(numero_comprobaciones):
            if abs(next(iterador) - funcion_alternativa(n)) > epsilon:
                return False
        return True

    """
    Nomenclatura de los tests: test_X_Y_Z.
        X representa los coeficientes. Usamos "n" para valores negativos.
        Y representa la función. Usamos "d" para la división, "p" para la 
        potencia.
        Z representa las condiciones inciales.
    """

    def test_1_1_0(self):
        # Recurrencia f(0)=0, f(n)=f(n-1)+1, que se corresponde con f(n)=n
        self.assertTrue(self.comprueba_recurrencia([1], lambda n: 1, [0], lambda n: n))

    def test_2_0_1(self):
        # Recurrencia f(0)=1, f(n)=2*f(n-1), que se corresponde con f(n)=2**n
        self.assertTrue(self.comprueba_recurrencia([2], lambda n: 0, [1], lambda n: 2 ** n))

    def test_1_n_0(self):
        # Recurrencia f(0)=0, f(n)=f(n-1)+n, que se corresponde con
        # f(n)=n*(n+1)/2
        self.assertTrue(self.comprueba_recurrencia([1], lambda n: n, [0],
                                                   lambda n: n * (n + 1) / 2))

    def test_1_nd2_0(self):
        # Recurrencia f(0)=0, f(n)=f(n-1)+n/2, que se corresponde con
        # f(n)=n*(n+1)/4
        self.assertTrue(self.comprueba_recurrencia([1], lambda n: n / 2, [0],
                                                   lambda n: n * (n + 1) / 4))

    def test_1_2pn_1(self):
        # Recurrencia f(0)=1, f(n)=f(n-1)+2**n, que se corresponde con
        # f(n)=2**(n+1)-1
        self.assertTrue(self.comprueba_recurrencia([1], lambda n: 2 ** n, [1],
                                                   lambda n: 2 ** (n + 1) - 1))

    def test_4n4_0_01(self):
        # Recurrencia f(0)=0, f(1)=1, f(n)=4f(n-1)-4f(n-2), que se corresponde
        # con f(n)=2**(n-1)*n
        self.assertTrue(self.comprueba_recurrencia([4, -4], lambda n: 0, [0, 1],
                                                   lambda n: 2 ** (n - 1) * n))

    def test_2n1_1_01(self):
        # Recurrencia f(0)=0, f(1)=1, f(n)=2f(n-1)-f(n-2)+1, que se corresponde
        # con f(n)=n*(n+1)/2
        self.assertTrue(self.comprueba_recurrencia([2, -1], lambda n: 1, [0, 1],
                                                   lambda n: n * (n + 1) / 2))

    def test_11n1_0_012(self):
        # Recurrencia f(0)=0, f(1)=1, f(2)=2, f(n)=f(n-1)+f(n-2)-f(n-3), que se
        # corresponde con f(n)=n
        self.assertTrue(self.comprueba_recurrencia([1, 1, -1],
                                                   lambda n: 0, [0, 1, 2],
                                                   lambda n: n))


class RecurrenciaMaestra:
    """
    Clase que representa una recurrencia de las que se consideran en el
    teorema maestro, de la forma T(n)=aT(n/b)+n^k. Se interpreta que en n/b
    la división es entera.
    Además de los métodos que aparecen a continuación, tienen que funcionar
    los siguientes operadores:
        ==, !=,
        str(): la representación como cadena debe ser 'aT(n/b)+n^k'
        []: el parámetro entre corchetes es el valor de n para calcular T(n).
    """

    def __init__(self, a, b, k, inicial=0):
        """
        Constructor de la clase, los parámetros a, b, y k son los que
        aparecen en la fórmula aT(n/b)+n^k. El parámetro inicial es el valor
        para T(0).
        """
        self.a = a
        self.b = b
        self.k = k
        self.inicial = inicial

    def metodo_maestro(self):
        """
        Devuelve una cadena con el tiempo de la recurrencia de acuerdo al
        método maestro. La salida está en el formato "O(n^x)" o "O(n^x*log(n))",
        siendo x un número.
        """
        sOgrande = ""
        if (self.a < self.b ** self.k):
            sOgrande = "O(n^" + str(self.k) + ")"
        elif (self.a == self.b ** self.k):
            sOgrande = "O(n^" + str(self.k) + "*log(n))"
        else:
            sOgrande = "O(n^" + str(math.log(self.a, self.b)) + ")"
        return sOgrande

    def __iter__(self):
        """
        Generador de valores de la recurrencia: T(0), T(1), T(2), T(3)...,
        indefinidamente.
        Aunque sea una recurrencia, los valores *no* deben calcularse
        recursivamente.
        """
        self.contador = 0
        return self

    def __getitem__(self, key):
        # Método para obtener un elemento concreto
        num = self.inicial
        if (key > 0):
            num = self.a * self.__getitem__(int(key / self.b)) + key ** self.k
        return num

    def __next__(self):
        # Método para obtener los elementos del iterador de manera infinita
        cont = self.contador
        num = self.inicial

        if (cont > 0):
            num = self.a * self[int(cont / self.b)] + cont ** self.k
        self.contador += 1
        return num

    def __str__(self):
        # Método para obtener la cadena
        return str(self.a) + "T(n/" + str(self.b) + ")+n^" + str(self.k)

    def __eq__(self, recu):
        # Método para comparar objetos
        return self.a == recu.a and self.b == recu.b and self.k == recu.k


class TestRecurrenciaMaestra(unittest.TestCase):

    def test_teorema_3_2_2(self):
        # Recurrencia T(n)=3T(n/2)+O(n^2)
        resultado = RecurrenciaMaestra(3, 2, 2).metodo_maestro()
        self.assertEqual(resultado, "O(n^2)")

    def test_teorema_2_2_1(self):
        # Recurrencia T(n)=2T(n/2)+O(n)
        resultado = RecurrenciaMaestra(2, 2, 1).metodo_maestro()
        self.assertEqual(resultado, "O(n^1*log(n))")

    def test_teorema_3_2_1(self):
        # Recurrencia T(n)=3T(n/2)+O(n)
        resultado = RecurrenciaMaestra(3, 2, 1).metodo_maestro()
        # esperamos algo parecido a "O(n^1.5849625007211563)"
        self.assertTrue("O(n^1.58" in resultado)
        self.assertTrue("log" not in resultado)

    def test_operador_eq(self):
        # Tests para los operadores == y !=

        r = RecurrenciaMaestra(2, 2, 2)
        self.assertTrue(r == RecurrenciaMaestra(2, 2, 2))
        self.assertFalse(r != RecurrenciaMaestra(2, 2, 2))
        for a, b, k in ((1, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1)):
            self.assertTrue(r != RecurrenciaMaestra(a, b, k))
            self.assertFalse(r == RecurrenciaMaestra(a, b, k))

    def test_operador_str(self):
        # Tests para str()
        self.assertEqual(str(RecurrenciaMaestra(2, 2, 2)), "2T(n/2)+n^2")
        self.assertEqual(str(RecurrenciaMaestra(7, 4, 3)), "7T(n/4)+n^3")

    # Tests para []

    def test_operador_getitem_222(self):

        r = RecurrenciaMaestra(2, 2, 2)
        for n, valor in enumerate((0, 1, 6, 11, 28, 37, 58, 71, 120, 137, 174,
                                   195, 260, 285, 338, 367, 496, 529, 598, 635)):
            self.assertEqual(r[n], valor)

    def test_operador_getitem_1201(self):

        r = RecurrenciaMaestra(1, 2, 0, 1)
        for n, valor in enumerate((1, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5,
                                   5, 6, 6, 6, 6)):
            self.assertEqual(r[n], valor)

    def test_operador_getitem_431(self):

        r = RecurrenciaMaestra(4, 3, 1)
        for n, valor in enumerate((0, 1, 2, 7, 8, 9, 14, 15, 16, 37, 38, 39, 44,
                                   45, 46, 51, 52, 53, 74, 75)):
            self.assertEqual(r[n], valor)

    # Casos de prueba para la generación sobre RecurrenciaMaestra.

    def comprueba_generacion(self, recurrencia, valores):
        it = iter(recurrencia)
        for v in valores:
            self.assertEqual(v, next(it))

    def test_generacion_222(self):
        self.comprueba_generacion(
            RecurrenciaMaestra(2, 2, 2),
            (0, 1, 6, 11, 28, 37, 58, 71, 120, 137, 174, 195, 260, 285, 338,
             367, 496, 529, 598, 635))

    def test_generacion_1201(self):
        self.comprueba_generacion(
            RecurrenciaMaestra(1, 2, 0, 1),
            (1, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6))

    def test_generacion_431(self):
        self.comprueba_generacion(
            RecurrenciaMaestra(4, 3, 1),
            (0, 1, 2, 7, 8, 9, 14, 15, 16, 37, 38, 39, 44, 45, 46, 51, 52, 53,
             74, 75))

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)