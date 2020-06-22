# Importaciones
import unittest


def subsecuencia_comun_mas_larga(x, y):
    """
    Dadas dos cadenas x e y devuelve una que es subsecuencia de ambas y que
    tiene la longitud máxima de todas las subsecuencias comunes.
    """
    MatSubsq = rellenarMatriz(x, y)
    # Obtención de la subsecuencia
    subsq = ""
    i = len(x) - 1
    j = len(y) - 1

    while i >= 0 and j >= 0:
        if x[i] == y[j]:
            subsq = x[i] + subsq
            i -= 1
            j -= 1
        else:
            MatIValue = 0
            MatJValue = 0
            if i > 0:
                MatIValue = MatSubsq[i - 1][j]
            if j > 0:
                MatJValue = MatSubsq[i][j - 1]
            if MatIValue >= MatJValue:
                i -= 1
            else:
                j -= 1
    return subsq


def rellenarMatriz(x, y):
    MatSubsq = []
    # Primero relleno la matriz
    for i in range(len(x)):
        # Utilizo una submatriz para ir añadiendola a la matriz principal (esto son las filas)
        subMat = []
        for j in range(len(y)):
            if x[i] == y[j]:
                if i > 0 and j > 0:
                    subMat.append(MatSubsq[i - 1][j - 1] + 1)
                else:
                    subMat.append(1)
            else:
                MatIValue = 0
                MatJValue = 0
                if i > 0:
                    MatIValue = MatSubsq[i - 1][j]
                if j > 0:
                    MatJValue = subMat[j - 1]
                subMat.append(max(MatIValue, MatJValue))
        MatSubsq.append(subMat)
    return MatSubsq


def es_subsecuencia(subsecuencia, secuencia):
    """Indica si el primer argumento es subsecuencia del segundo"""

    it = iter(secuencia)
    return all(c in it for c in subsecuencia)


class TestEsSubsecuencia(unittest.TestCase):

    def test_positivos(self):

        for subsecuencia, secuencia in (
                ("GTTC", "GTTCCTAATA"),
                ("CCTA", "GTTCCTAATA"),
                ("AATA", "GTTCCTAATA"),
                ("GTCAT", "GTTCCTAATA"),
                ("TCTAA", "GTTCCTAATA"),
                ("GTTCCTAATA", "GTTCCTAATA"),
        ):
            self.assertTrue(es_subsecuencia(subsecuencia, secuencia))

    def test_negativos(self):

        for subsecuencia, secuencia in (
                ("GTTCCTTATA", "GTTCCTAATA"),
                ("GGTTCCTAATA", "GTTCCTAATA"),
                ("GTTCCTAATAA", "GTTCCTAATA"),
                ("GG", "GTTCCTAATA"),
                ("AC", "GTTCCTAATA"),
                ("TGTCCTAATA", "GTTCCTAATA"),
                ("ATAA", "GTTCCTAATA"),

        ):
            self.assertFalse(es_subsecuencia(subsecuencia, secuencia))


class TestSubsecuenciaComunMasLarga(unittest.TestCase):

    def test_subsecuencia_comun_mas_larga(self):

        for s1, s2, longitud in (
                ("GTTCCTAATA", "CGATAATTGAGA", 6),
                ("ACDAADDADDDDCCBCBCAD", "ADBDBBCDBDAABBDDDCBB", 11),
                ("BBDABCCADCCADADDCACAACBA", "DBCBBDCBADABBBCCCDCACAADDACADD", 17),
                ("01111000000111100011", "10010100000100101111", 14),
                ('TTTATTTCGTCTAACTTATGACGTCCCTTCACGATCCAA',
                 'TGGCCGGTTATTCAAGAGCGATATGTGCTATAAAGTGCC', 23)
        ):
            for x, y in ((s1, s2), (s2, s1)):
                subsecuencia = subsecuencia_comun_mas_larga(x, y)
                self.assertEqual(len(subsecuencia), longitud)
                for secuencia in x, y:
                    self.assertTrue(es_subsecuencia(subsecuencia, secuencia))


def subsecuencias_comunes_mas_largas(x, y):
    """
    Dadas dos cadenas x e y devuelve un conjunto con todas las subsecuencias de
    ambas que tienen longitud máxima.
    """
    matriz = rellenarMatriz(x, y)
    # Añado columna y fila con ceros
    for i in range(len(x)):
        matriz[i].insert(0, 0)
    matriz.insert(0, [0] * (len(y) + 1))
    nuevoSet = obtenerSecuenciasRec(x, y, len(x), len(y), matriz)
    return set(nuevoSet)


def obtenerSecuenciasRec(x, y, m, n, matriz):
    # Condicion de salida
    if m == 0 or n == 0:
        return [""]

    if (x[m - 1] == y[n - 1]):
        nuevoSet = obtenerSecuenciasRec(x, y, m - 1, n - 1, matriz)
        i = 0
        while i < len(nuevoSet):
            nuevoSet[i] = nuevoSet[i] + x[m - 1]
            i += 1
        return nuevoSet;

    if matriz[m - 1][n] > matriz[m][n - 1]:
        return obtenerSecuenciasRec(x, y, m - 1, n, matriz)

    if matriz[m][n - 1] > matriz[m - 1][n]:
        return obtenerSecuenciasRec(x, y, m, n - 1, matriz)

    listaTop = obtenerSecuenciasRec(x, y, m - 1, n, matriz)
    listaLeft = obtenerSecuenciasRec(x, y, m, n - 1, matriz)
    listaTop += listaLeft
    return listaTop


class TestSubsecuenciasComunesMasLarga(unittest.TestCase):

    def test_subsecuencias_comunes_mas_largas(self):

        for s1, s2, longitud, numero in (
                ("GTTCCTAATA", "CGATAATTGAGA", 6, 3),
                ("ACDAADDADDDDCCBCBCAD", "ADBDBBCDBDAABBDDDCBB", 11, 4),
                ("BBDABCCADCCADADDCACAACBA", "DBCBBDCBADABBBCCCDCACAADDACADD",
                 17, 1),
                ("01111000000111100011", "10010100000100101111", 14, 10),
                ('TTTATTTCGTCTAACTTATGACGTCCCTTCACGATCCAA',
                 'TGGCCGGTTATTCAAGAGCGATATGTGCTATAAAGTGCC', 23, 20)

        ):
            for x, y in ((s1, s2), (s2, s1)):
                subsecuencias = subsecuencias_comunes_mas_largas(x, y)
                self.assertTrue(isinstance(subsecuencias, set))
                self.assertEqual(len(subsecuencias), numero)
                for subsecuencia in subsecuencias:
                    self.assertEqual(len(subsecuencia), longitud)
                    for secuencia in x, y:
                        self.assertTrue(es_subsecuencia(subsecuencia, secuencia))
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)