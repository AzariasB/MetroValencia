from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QMainWindow, QFormLayout, QLineEdit, QPushButton, QWidget, QSpinBox
from PyQt5.QtGui import QPalette, QColor


class Preferences:

    def __init__(self):
        self.settings = QSettings("Azarias", "Metro Valencia")
        self.notif_times = self.chosen_times
        self.notif_done = set()

    @property
    def warn_advance(self):
        return int(self.settings.value("warn_advance", 20))

    @warn_advance.setter
    def warn_advance(self, value):
        self.settings.setValue("warn_advance", int(value))

    @property
    def chosen_times(self):
        return set(self.settings.value("chosen_times", set()))

    @property
    def search_start(self):
        return str(self.settings.value("search_start", "07:00"))

    @search_start.setter
    def search_start(self, value):
        self.settings.setValue("search_start", value)

    def update_chosen(self, times: set):
        self.settings.setValue("chosen_times", times)


class PrefWindow(QMainWindow):

    def __init__(self, preferences: Preferences):
        super().__init__()
        self.preferences = preferences
        layout = QFormLayout()
        self.center = QWidget()
        self.warn_before = QSpinBox()
        self.search_after = QLineEdit()
        layout.addRow("Me prévenir avant:", self.warn_before)
        layout.addRow("Heure de recherche", self.search_after)
        self.search_after.setInputMask("99:99")

        self.save_btn = QPushButton("Enregistrer")
        self.cancel_btn = QPushButton("Annuler")

        self.save_btn.clicked.connect(self.save_changes)
        self.cancel_btn.clicked.connect(self.cancel)

        layout.addRow(self.save_btn, self.cancel_btn)

        self.center.setLayout(layout)
        self.setCentralWidget(self.center)
        self._reset()

    def _reset(self):
        self.warn_before.setValue(int(self.preferences.warn_advance))
        self.search_after.setText(self.preferences.search_start)
        self.setVisible(False)

    def save_changes(self):
        if self.search_after.hasAcceptableInput():
            self.preferences.warn_advance = self.warn_before.value()
            self.preferences.search_start = self.search_after.text()
            self.setVisible(False)
        else:
            palette = self.search_after.palette()
            palette.setColor(QPalette.Text, Qt.red)
            self.search_after.setToolTip("Mauvais choix d'horaire")
            self.search_after.setPalette(palette)

    def cancel(self):
        self._reset()
