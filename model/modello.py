import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self._bestSol = []
        self._maxScore = 0

    def getYears(self):
        return DAO.getYears()

    def getShapes(self):
        return DAO.getShapes()

    def buildGraph(self, year, shape):
        self._graph.clear()
        self._idMap = {}

        nodes = DAO.getNodes(year, shape)
        for node in nodes:
            self._idMap[node.id] = node
        self._graph.add_nodes_from(nodes)

        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u.id < v.id:
                    if u.state == v.state:
                        if u.longitude < v.longitude:
                            peso = v.longitude - u.longitude
                            self._graph.add_edge(u, v, weight=peso)
                        elif u.longitude > v.longitude:
                            peso = u.longitude - v.longitude
                            self._graph.add_edge(v, u, weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getBestArchi(self):
        return list(sorted(list(self._graph.edges(data=True)), key=lambda x: x[2]["weight"], reverse=True)[:5])

    def getBestPath(self):
        self._bestSol = []
        self._maxScore = 0

        for node in self._graph.nodes:
            self._ricorsione([node], node)

        return self._bestSol, self._maxScore

    def _ricorsione(self, parziale, source):
        if (score:=self._calcolaScore(parziale)) > self._maxScore:
            self._bestSol = copy.deepcopy(parziale)
            self._maxScore = score
        for n in self._graph.neighbors(source):
            if n not in parziale:
                if self._nodoAmmissibile(parziale, n):
                    parziale.append(n)
                    self._ricorsione(parziale, n)
                    parziale.pop()

    def _nodoAmmissibile(self, parziale, n: Sighting):
        if len(parziale) < 3:
            return True
        if parziale[-3].datetime.month == parziale[-2].datetime.month == parziale[-1].datetime.month:
            return parziale[-1].datetime.month != n.datetime.month
        return True

    def _calcolaScore(self, percorso):
        totale = 0
        for i in range(len(percorso)):
            if i == 0:
                totale += 100
            else:
                totale += 100
                if percorso[i].datetime.month == percorso[i-1].datetime.month:
                    totale += 200
        return totale
