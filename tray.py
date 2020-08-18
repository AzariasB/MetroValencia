from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon, QApplication

from preferences import Preferences, PrefWindow


class Tray(QSystemTrayIcon):

    def __init__(self, icon, settings: Preferences):
        super().__init__()
        self._main_window = PrefWindow(settings)
        self.main_menu = QMenu()
        self.refresh = QAction("Refresh")
        self.quit = QAction("Quit")
        self.preferences = QAction("Preferences")
        self.actions = []
        self.setToolTip("MetroValencia")
        self.setIcon(icon)
        self.setContextMenu(self.main_menu)
        self.setVisible(True)
        self.activated.connect(self._activated)

        self.preferences.triggered.connect(lambda: self._show_window())
        self.notif_times = settings.notif_times
        self.notif_done = settings.notif_done

    def _activated(self, action):
        if action == QSystemTrayIcon.MiddleClick:
            self._show_window()

    def _show_window(self):
        center = QApplication.desktop().screen().rect().center()
        self._main_window.show()
        self._main_window.raise_()
        self._main_window.activateWindow()
        self._main_window.setWindowState((self._main_window.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive)
        self._main_window.move(center - self._main_window.rect().center())

    def _create_action(self, time):
        action = QAction(time)
        action.setCheckable(True)
        action.setChecked(time in self.notif_times or time in self.notif_done)
        action.setEnabled(time not in self.notif_done)

        def check():
            if action.isChecked():
                self.notif_times.add(time)
            else:
                self.notif_times.remove(time)

        action.triggered.connect(check)
        return action

    def update_times(self, times):
        self.main_menu.clear()
        self.main_menu.addAction(self.preferences)
        self.main_menu.addAction(self.refresh)

        for t in times:
            action = self._create_action(t)
            self.actions.append(action)
            self.main_menu.addAction(action)

        self.main_menu.addAction(self.quit)
