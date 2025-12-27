from krita import *
from PyQt5.QtWidgets import (
    QTableView, QDockWidget, QVBoxLayout,
    QPushButton, QAbstractItemView, QWidget
)
from PyQt5.QtCore import QAbstractTableModel, Qt

# Table Model
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
            try:
                return [
                    brush.name() if hasattr(brush, 'name') else "Unbekannt",
                    f"{brush.brushTip().width()}px" if hasattr(brush, 'brushTip') else "0px",
                    f"{brush.opacity()}%" if hasattr(brush, 'opacity') else "100%",
                    brush.category() if hasattr(brush, 'category') else "",
                    ", ".join(brush.tags()) if hasattr(brush, 'tags') else "",
                ][index.column()]
            except:
                return "N/A"

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

# Docker Widget
class BrushManagerDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brush Manager")

        # Widget
        self.mainWidget = QWidget()
        self.layout = QVBoxLayout()

        # Table
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Buttons
        self.btn_create_bundle = QPushButton("Add selection to Bundle")
        self.btn_create_bundle.clicked.connect(self.create_bundle)
        self.btn_create_bundle.setEnabled(False)

        # Layout
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btn_create_bundle)
        self.mainWidget.setLayout(self.layout)
        self.setWidget(self.mainWidget)

        # load all brushes
        self.load_brushes()

    # load all brushes
    def load_brushes(self):
        try:
            application = Krita.instance()
            # Verwende "preset" statt "brush" für Resource-Typ
            brush_resource = application.resources("preset")

            if hasattr(brush_resource, 'resources'):
                self.brushes = list(brush_resource.resources())
                print(f"Geladene Pinsel: {len(self.brushes)}")

                if self.brushes:
                    self.model = BrushTableModel(self.brushes)
                    self.table.setModel(self.model)
                    self.btn_create_bundle.setEnabled(True)
                else:
                    print("Keine Pinsel gefunden")
            else:
                print("Keine resources()-Methode verfügbar")

        except Exception as e:
            print(f"Fehler beim Laden: {e}")
            import traceback
            traceback.print_exc()
            self.brushes = []

    # create new bundle from selected brushes
    def create_bundle(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            print("Keine Pinsel ausgewählt!")
            return

        try:
            # KORREKTUR: Verwende Krita.instance() statt Application
            app = Krita.instance()
            bundle_resource = app.resources("bundle")

            # Neues Bundle erstellen
            bundle = bundle_resource.create("Neues_Bundle")

            # Ausgewählte Pinsel hinzufügen
            for index in selected:
                brush = self.brushes[index.row()]
                bundle.addResource(brush)

            # Speicherdialog anzeigen
            from PyQt5.QtWidgets import QFileDialog
            import os

            # Standard-Pfad für Krita-Bundles
            default_path = os.path.expanduser("~/Neues_Bundle.bundle")

            file_path, _ = QFileDialog.getSaveFileName(
                self.mainWidget,
                "Bundle speichern",
                default_path,
                "Krita Bundles (*.bundle)"
            )

            if file_path:
                if not file_path.endswith('.bundle'):
                    file_path += '.bundle'

                bundle.setFileName(file_path)
                if bundle.save():
                    print(f"Bundle gespeichert: {file_path}")
                else:
                    print("Fehler beim Speichern des Bundles")
            else:
                print("Abgebrochen")

        except Exception as e:
            print(f"Fehler beim Erstellen des Bundles: {e}")
            import traceback
            traceback.print_exc()
