from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from preferences import Preferences


def to_minutes(time: str):
    hours, minutes = time.split(':')
    return int(hours) * 60 + int(minutes)


def date_diff(sooner, later):
    soon = to_minutes(sooner)
    lat = to_minutes(later)
    return abs(lat - soon)


ORIGIN_STATION = 15  # Colón
DESTINATION_STATION = 31  # Paiporta


class Fetcher:
    TARGET_URL = 'https://www.metrovalencia.es/horarios.php?page=143'
    POST_DATA = {
        'origen': ORIGIN_STATION,
        'acceptar': 0,
        'key': 0,
        'destino': DESTINATION_STATION,
        'fetcha': datetime.now().strftime('%d/%m/%Y'),
        'hini': '00:00',
        'hfin': '23:59',
        'calcular': 1
    }

    def __init__(self, settings: Preferences):
        self.settings = settings

    def fetch_times(self):
        res = requests.post(Fetcher.TARGET_URL, data=Fetcher.POST_DATA)
        soup = BeautifulSoup(res.content, 'html.parser')
        divs = soup.find(id='horarios').find('table').find_all('td')
        times = [div.get_text() for div in divs if ':' in div.get_text()]
        now = datetime.now().strftime('%H:%M')
        return [t for t in times if t >= now and t > self.settings.search_start]

    def update_settings(self, notify_time):
        times = self.fetch_times()
        delay = self.settings.warn_advance
        now = datetime.now()
        in_n_mintutes = now + timedelta(minutes=delay)
        notif_times = self.settings.notif_times
        notif_done = self.settings.notif_done
        if len(notif_times) > 0:
            leave_now = in_n_mintutes.strftime("%H:%M")
            for time in notif_times:
                if leave_now >= time:
                    notif_done.add(time)
                    notify_time(time, date_diff(now.strftime("%H:%M"), time))
            for rm in notif_done:
                if rm in notif_times:
                    notif_times.remove(rm)
        return times
