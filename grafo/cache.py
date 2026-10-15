import threading
from collections import OrderedDict


def contiene(grande, chico):
    """Cajas como (norte, sur, este, oeste)."""
    return (grande[0] >= chico[0] and grande[1] <= chico[1]
            and grande[2] >= chico[2] and grande[3] <= chico[3])


class CacheGrafos:
    """Caché LRU: una consulta acierta si alguna caja guardada la contiene por completo."""

    def __init__(self, capacidad=4):
        self._capacidad = capacidad
        self._items = OrderedDict()
        self._candado = threading.Lock()

    def buscar(self, caja):
        with self._candado:
            for clave in reversed(self._items):
                if contiene(clave, caja):
                    self._items.move_to_end(clave)
                    return self._items[clave]
        return None

    def guardar(self, caja, grafo):
        with self._candado:
            self._items[caja] = grafo
            while len(self._items) > self._capacidad:
                self._items.popitem(last=False)
