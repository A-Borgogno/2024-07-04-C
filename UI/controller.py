import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDs(self):
        self._view.ddyear.options.clear()
        self._view.ddshape.options.clear()
        years = self._model.getYears()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        shapes = self._model.getShapes()
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        year = self._view.ddyear.value
        if not year:
            self._view.txt_result1.controls.append(ft.Text("Selezionare l'anno", color="red"))
            self._view.update_page()
            return
        shape = self._view.ddshape.value
        if not shape:
            self._view.txt_result1.controls.append(ft.Text("Selezionare la forma", color="red"))
            self._view.update_page()
            return
        nodes, edges = self._model.buildGraph(year, shape)
        self._view.txt_result1.controls.append(ft.Text("Grafo costruito correttamente"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nodes}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {edges}"))
        self._view.btn_path.disabled = False
        self._view.update_page()



    def handle_path(self, e):
        pass
