import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.list_sighting = []
        self.list_shapes = []
        self.list_states = []

        self.G = nx.Graph()
        self._nodes = []
        self._edges = []
        self.id_map= {}

        self.sol_best= 0

        self.path= []
        self.path_edge= []

        self.load_sighting()
        self.load_shapes()
        self.load_states()


    def load_sighting(self):
        self.list_sighting = DAO.get_all_sighting()

    def load_shapes(self):
        self.list_shapes = DAO.get_all_shapes()

    def load_states(self):
        self.list_states = DAO.get_all_states()


    def build_graph(self, year, shape):
        self.G.clear()

        self._nodes = []
        self._edges = []

        # creo i nodi (states)
        for s in self.list_states:
            self._nodes.append(s)
        self.G.add_nodes_from(self._nodes)

        self.id_map = {}
        for n in self._nodes:
            self.id_map[n.id] = n  #chiave: id dello stato, valore: oggetto stato

        # creo gli archi
        tmp_edges= DAO.get_all_weighted_neigh(year, shape) #ottengo tutti gli archi
        self._edges.clear()
        for e in tmp_edges:
            self._edges.append((self.id_map[e[0]], self.id_map[e[1]], e[2]))
            '''
            self.id_map[e[0]] = oggetto stato1 (dove e[0]= row['st1'] è l'id dello stato1)
            self.id_map[e[1]] = oggetto stato2 (dove e[1]= row['st2'] è l'id dello stato2) 
            e[2] = N (è il peso di ogni arco)
            '''

        self.G.add_weighted_edges_from(self._edges)  # creo gli archi dandogli già il peso

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()

    def get_num_of_edges(self):
        return self.G.number_of_edges()

    def get_sum_weight_per_node(self): #per calcolare il peso dei singoli nodi
        pp= []
        for n in self.G.nodes(): #ciclo su tutti i nodi
            sum_w= 0
            for e in self.G.edges(n, data=True): #ciclo su tutti gli archi collegati al nodo n (e ha 3 valori (nodo di partenza, nodo di arrivo, peso)
                sum_w += e[2]['weight'] # e[2]['weight'] = peso di ogni arco
            pp.append((n.id, sum_w)) #pp è una lista di tuple
        return pp

