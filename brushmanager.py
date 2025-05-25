from krita import *

from PyQt5.QtWidgets import (
    QTableView,
    QDockWidget,
    QVBoxLayout,
    QPushButton,
    QAbstractItemView,
)
from PyQt5.QtCore import QAbstractTableModel, Qt


class BrushTableModel(QAbstractTableModel):
    def __init__(self, brushes, parent=None):
        super().__init__(parent)
        self.brushes = brushes
        self.headers = ["Name", "Size", "Opacity", "Category", "Tags"]

    def rowCount(self, parent=None):
        return len(self.brushes)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            brush = self.brushes[index.row()]
            return [
                brush.name(),
                f"{brush.brushTip().width()}px",
                f"{brush.opacity()}%",
                brush.category(),
                ", ".join(brush.tags()),
            ][index.column()]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]


class BrushManagerDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BrushManager")

        # Hauptwidget
        self.mainWidget = QWidget()
        self.layout = QVBoxLayout()

        # Tabelle
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Buttons
        self.btn_create_bundle = QPushButton("Add selection to Bundle")
        self.btn_create_bundle.clicked.connect(self.create_bundle)

        # Layout
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btn_create_bundle)
        self.mainWidget.setLayout(self.layout)
        self.setWidget(self.mainWidget)

        # Daten laden
        self.load_brushes()

    def load_brushes(self):
        application = Krita.instance()
        brush_resource = application.resources("brush")
        self.brushes = [brush for brush in brush_resource.resources()]

        self.model = BrushTableModel(self.brushes)
        self.table.setModel(self.model)

    def create_bundle(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return

        # Neues Bundle erstellen
        bundle = Application.resources("bundle").create("Create new .bundle")

        # Ausgewählte Pinsel hinzufügen
        for index in selected:
            brush = self.brushes[index.row()]
            bundle.addResource(brush)

        # Bundle speichern
        bundle.save()
        print(f"New .bundle {len(selected)} Saved")


# Registrierung
Krita.instance().addDockWidgetFactory(
    DockWidgetFactory(
        "brushmanager", DockWidgetFactoryBase.DockRight, BrushManagerDocker
    )
)
