import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self._list_year= []
        self._list_shape= []

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # TODO

        sighting_list= self._model.list_sighting
        self._list_shape= self._model.list_shapes

        #popolo la lista di anni
        for n in sighting_list:
            if n.s_datetime.year not in self._list_year:
                self._list_year.append(n.s_datetime.year) #s_datetime.year mi consente di prendere solo l'anno

        #popolo dropdown di forme(shapes)
        for shape in self._list_shape:
            self._view.dd_shape.options.append(ft.dropdown.Option(shape))

        #popolo il dropdown di anni
        for year in self._list_year:
            self._view.dd_year.options.append(ft.dropdown.Option(year))

        self._view.update()


    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        selected_year= self._view.dd_year.value
        selected_shape= self._view.dd_shape.value

        #pulisco area risultato
        self._view.lista_visualizzazione_1.controls.clear()

        #costruisco grafo con i parametri selezionati
        self._model.build_graph(selected_year, selected_shape)

        #mostra info grafo
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(
                f"Numero di vertici: {self._model.get_num_of_nodes()}"
                f"Numero di archi: {self._model.get_num_of_edges()}"
            )
        )
        #mostra somma pesi per nodo
        for node_info in self._model.get_sum_weight_per_node():
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f"Nodo {node_info[0]}, somma pesi su archi = {node_info[1]}") #node_info[1] = peso totale
            )

        self._view.update()


    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
