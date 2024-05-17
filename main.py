import machine
from button_controller import ButtonController
from network_manager import NetworkManager, wifi_status_handler
import time # type: ignore
from cosmic import CosmicUnicorn # type: ignore
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY # type: ignore
from repository import Station
from screen_controller import Screen
from app import App

import WIFI_CONFIG
import CONFIG
from API import *

network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=wifi_status_handler)

tram_repository = Station(URL, CONFIG.TRAM_STATION, CONFIG.API_KEY, DIRECTIONS[0])

cu = CosmicUnicorn()
graphics = PicoGraphics(DISPLAY)

screen = Screen(cu, graphics, time.ticks_ms())
buttons = ButtonController(cu)

app = App(network_manager, screen, tram_repository, buttons)

if __name__ == "__main__":

    while True:

        try:
            time_ms = time.ticks_ms()

            app.update(time_ms)
            time.sleep(0.001)
        except Exception:
            machine.reset()

