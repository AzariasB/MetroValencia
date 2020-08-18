from os import system, path

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from fetcher import Fetcher
from preferences import Preferences
from tray import Tray

app = QApplication([])


ICON_PATH = f"{path.abspath(path.curdir)}/icon.png"
# Create the icon
icon = QIcon(ICON_PATH)

app.setQuitOnLastWindowClosed(False)

# Create the tray
settings = Preferences()
tray = Tray(icon, settings)
fetcher = Fetcher(settings)
# tray.activated.connect(lambda ev: print(ev))
timer = QTimer()
timer.setSingleShot(False)
timer.setInterval(60 * 1000)


def notify_time(time, delay=None):
    if not delay:
        command = f"notify-send -i {ICON_PATH} '{time}'"
    else:
        command = f"notify-send -i {ICON_PATH} 'Le métro de {time} part dans {delay} minutes'"
    system(command)


def update():
    times = fetcher.update_settings(notify_time)
    tray.update_times(times)


timer.timeout.connect(update)
tray.quit.triggered.connect(app.quit)
tray.refresh.triggered.connect(update)

if __name__ == "__main__":
    update()
    timer.start()
    notify_time("Starting valencia")
    app.exec_()
