import networkx as nx
from geopy import distance
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
        self.path_node= []
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


    def compute_path(self):
        self.path_node = []
        self.path_edge = []
        self.sol_best = 0 #mi darà il cammino massimo

        partial_node= [] #lista in cui man mano inserisco tutti i nodi
        for n in self.get_nodes(): #esploro tutte le possibili soluzioni partendo da tutti i possibili nodi
            partial_node.clear()
            partial_node.append(n)
            self._ricorsione(partial_node, [])

    def _ricorsione(self, partial_node, partial_edge):
        n_last= partial_node[-1] #ultimo nodo nella mia lista di nodi

        neighbors= self.get_admissible_neighbs(n_last, partial_edge) #ottengo tutti i vicini di un determinato nodo

        #condizioni finali
        if len(neighbors) == 0: #ho esplorato tutti i possibili vicini del mio nodo di partenza
            weight_path= self.compute_weight_path(partial_edge)
            if weight_path > self.sol_best:
                self.sol_best = weight_path + 0.0
                self.path_node= partial_node[:]
                self.path_edge= partial_edge[:]
            return

        #ciclo di ricorsione
        for n in neighbors: #da tutti i nodi di possibili vicini che posso raggiungere esploro tutte le possibili alternative
            partial_edge.append((n_last, n, self.G.get_edge_data(n_last, n)['weight'])) #(nodo di partenza, nodo di arrivo, peso)
            partial_node.append(n)

            self._ricorsione(partial_node, partial_edge)

            partial_node.pop()
            partial_edge.pop()

    def get_nodes(self):
        return self.G.nodes()

    def get_admissible_neighbs(self, n_last, partial_edge): #partial_edge sono quelli che ho già visitato
        all_neigh= self.G.edges(n_last, data=True) #tutti i nodi collegati al mio nodo di partenza
        result= []
        for e in all_neigh:
            if len(partial_edge) != 0:
                # trovare la soluzione migliore man mano che il peso degli archi sia sempre maggiore
                if e[2]['weight'] > partial_edge[-1][2]: #verifico che il peso sia maggiore
                    result.append(e[1])
            else: #se sono all'inizio e quindi ho solo un nodo, lo aggiungo di default perché non posso confrontare il peso
                result.append(e[1])
        return result

    def compute_weight_path(self, mylist): #distanza tra un nodo e l'altro
        weight= 0
        for e in mylist:
            weight += distance.geodesic((e[0].lat, e[0].lng), (e[1].lat, e[1].lng)).km
        return weight

    def get_distance_weight(self, e):
        return distance.geodesic((e[0].lat, e[0].lng),
                                 (e[1].lat, e[1].lng)).km


