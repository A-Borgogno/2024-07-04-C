from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

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
                if u.id >= v.id:
                    continue
                if u.state == v.state:
                    if u.longitude < v.longitude:
                        weight = v.longitude - u.longitude
                        self._graph.add_edge(u, v, weight=weight)
                    elif u.longitude > v.longitude:
                        weight = u.longitude - v.longitude
                        self._graph.add_edge(v, u, weight=weight)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getBestArchi(self):
        return list(sorted(list(self._graph.edges(data=True)), key=lambda x: x[2]["weight"])[:5])