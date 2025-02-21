import machine
from network_manager import NetworkManager, wifi_status_handler
import time # type: ignore
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_128X64 # type: ignore
from repository import Station
from screen_controller import Screen
from app import App

import WIFI_CONFIG
import CONFIG
from API import *

network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=wifi_status_handler)

tram_repository = Station(URL, CONFIG.TRAM_STATION, CONFIG.API_KEY, DIRECTIONS[0])

i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_128X64)
graphics = i75.display

screen = Screen(i75, graphics, time.ticks_ms())

app = App(network_manager, screen, tram_repository)

if __name__ == "__main__":

    while True:

        try:
            time_ms = time.ticks_ms()

            app.update(time_ms)
            time.sleep(0.001)
        except Exception:
            machine.reset()

