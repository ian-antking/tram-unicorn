import machine # type: ignore
import WIFI_CONFIG
from network_manager import NetworkManager, wifi_status_handler
import time
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_128X64, SWITCH_A, SWITCH_B # type: ignore
import WIFI_CONFIG
from repository import Station
from screen_controller import Screen
from app import App
from API import Direction
from update import perform_update

import WIFI_CONFIG
import CONFIG
from API import *

network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=wifi_status_handler)

tram_repository = Station(URL, CONFIG.TRAM_STATION, CONFIG.API_KEY, Direction.INCOMING)

i75 = Interstate75(display=DISPLAY_INTERSTATE75_128X64)
graphics = i75.display

screen = Screen(i75, graphics, time.ticks_ms())

app = App(network_manager, screen, tram_repository)
perform_update(screen)

if __name__ == "__main__":

    while True:

        if i75.switch_pressed(SWITCH_A):
            app.display_incoming()

        if i75.switch_pressed(SWITCH_B):
            app.display_outgoing()

        try:
            time_ms = time.ticks_ms()

            app.update(time_ms)
            time.sleep(0.001)
        except Exception as e:
            print(e)
            machine.reset()
