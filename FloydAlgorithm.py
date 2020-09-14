# Importaciones
import unittest


class CaminosMinimosFloyd:
    """
    Clase para representar los caminos mínimos entre todos los nodos de un grafo.
    Los caminos deben calcularse con el algoritmo de Floyd.
    El espacio de almacenamiento debe ser O(n^2), siendo n el número de nodos.
    """
    listaNodos = []
    MatrizDistancias = []
    MatrizCaminos = []

    def __init__(self, grafo):
        """
        Constructor que recibe el grafo sobre el que calcular los MatrizCaminos
        mínimos.
        El grafo que se recibe es un diccionario donde las claves son arcos
        (pares de nodos) y los valores son el peso de los arcos.
        """
        nodos = set()
        for camino, coste in grafo.items():
            nodos.add(camino[0])
            nodos.add(camino[1])
        self.listaNodos = sorted(list(nodos))
        # Relleno la matriz de distancias con infinitos y ceros
        for i in range(len(self.listaNodos)):
            fila = [float("inf")] * len(self.listaNodos)
            # Pongo la fila intersección a 0
            fila[i] = 0
            self.MatrizDistancias.append(fila)

            # Modifico la matriz distancias para actualizarla con lo que tenga en listaNodos
        for camino, coste in grafo.items():
            self.MatrizDistancias[self.listaNodos.index(camino[0])][self.listaNodos.index(camino[1])] = coste

        # Creo la matriz de caminos
        for i in range(len(self.listaNodos)):
            fila = [None] * len(self.listaNodos)
            self.MatrizCaminos.append(fila)
        # Algoritmo de floyd
        for k in range(len(self.MatrizDistancias)):
            for i in range(len(self.MatrizDistancias)):
                for j in range(len(self.MatrizDistancias)):
                    if self.MatrizDistancias[i][j] > self.MatrizDistancias[i][k] + self.MatrizDistancias[k][j]:
                        self.MatrizDistancias[i][j] = self.MatrizDistancias[i][k] + self.MatrizDistancias[k][j]
                        self.MatrizCaminos[i][j] = self.listaNodos[k]

    def distancia(self, origen, destino):
        """
        Devuelve la distancia del camino mínimo ente origen y destino.
        Si no hay camino devuelve None.
        """
        distMin = None
        if self.MatrizDistancias[self.listaNodos.index(origen)][self.listaNodos.index(destino)] < float("inf"):
            distMin = self.MatrizDistancias[self.listaNodos.index(origen)][self.listaNodos.index(destino)]
        return distMin

    def camino(self, origen, destino):
        """
        Devuelve en una lista de nodos el camino mínimo entre origen y
        destino.
        Si no hay camino devuelve None.
        """
        nodosCamino = None
        if self.listaNodos.index(origen) == self.listaNodos.index(destino):
            nodosCamino = [origen]
        elif self.MatrizDistancias[self.listaNodos.index(origen)][self.listaNodos.index(destino)] < float("inf"):
            nodosCamino = [origen]
            self.obtenCaminoRecursivo(origen, destino, nodosCamino)
            nodosCamino.append(destino)
        return nodosCamino

    def obtenCaminoRecursivo(self, origen, destino, nodosCamino):
        # Obten el camino de manera recursiva
        nodo = self.MatrizCaminos[self.listaNodos.index(origen)][self.listaNodos.index(destino)]
        if nodo is not None:
            self.obtenCaminoRecursivo(origen, nodo, nodosCamino)
            nodosCamino.append(nodo)
            self.obtenCaminoRecursivo(nodo, destino, nodosCamino)


class TestCaminosMinimosFloyd(unittest.TestCase):
    """Tests para la clase CaminosMinimosFloyd."""

    def test_7_nodos_12_arcos(self):
        grafo = {
            ("a", "b"): 2,
            ("a", "d"): 1,
            ("b", "d"): 3,
            ("b", "e"): 10,
            ("c", "a"): 4,
            ("c", "f"): 5,
            ("d", "c"): 2,
            ("d", "e"): 7,
            ("d", "f"): 8,
            ("d", "g"): 4,
            ("e", "g"): 6,
            ("g", "f"): 1
        }

        caminos = CaminosMinimosFloyd(grafo)

        for origen, destino, distancia, camino in (
                ("a", "a", 0, ["a"]),
                ("a", "b", 2, ["a", "b"]),
                ("a", "c", 3, ["a", "d", "c"]),
                ("a", "d", 1, ["a", "d"]),
                ("a", "e", 8, ["a", "d", "e"]),
                ("a", "f", 6, ["a", "d", "g", "f"]),
                ("a", "g", 5, ["a", "d", "g"]),
                ("b", "a", 9, ["b", "d", "c", "a"]),
                ("c", "e", 12, ["c", "a", "d", "e"]),
                ("d", "b", 8, ["d", "c", "a", "b"]),
                ("e", "f", 7, ["e", "g", "f"]),
                ("e", "a", None, None),
                ("f", "d", None, None)
        ):
            self.assertEqual(caminos.distancia(origen, destino), distancia)
            self.assertEqual(caminos.camino(origen, destino), camino)
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
