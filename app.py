import uasyncio
import WIFI_CONFIG
from API import DIRECTIONS
import COLORS
import time

class App:
    def __init__(self, network_manager, screen_manager, station_repository, button_controller):
        self.network = network_manager
        self.screen = screen_manager
        self.tram_station = station_repository
        self.buttons = button_controller
        self.sleep = False
        self.last_update_time = 0

        self.connect_wifi()
        self.get_data()


    def connect_wifi(self, retries=0):
        message = ["wait", "for", "wifi"]
        if retries > 0: message.append("retry {retries}".format(retries=retries))
        self.screen.display_message(message, (0, 255, 255))
        try:
            uasyncio.get_event_loop().run_until_complete(self.network.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
        except Exception as e:
            self.screen.display_message(["wifi", "fail"], COLORS.ERROR)
            print(f'Wifi connection failed! {e}')
            time.sleep(10 ^ retries)
            self.connect_wifi(retries+1)

    def get_data(self):
        data = self.tram_station.get()
        self.screen.set_trams(data["trams"])
        self.screen.set_message(data["message"])


    def display_incoming(self):
            self.tram_station.set_destination(DIRECTIONS[0])
            self.screen.display_message(["getting", DIRECTIONS[0], "trams"], COLORS.INFO)
            self.get_data()

    def display_outgoing(self):
            self.tram_station.set_destination(DIRECTIONS[1])
            self.screen.display_message(["getting", DIRECTIONS[1], "trams"], COLORS.INFO)
            self.get_data()

    def handle_sleep(self):
         self.sleep = not self.sleep

    def increase_brightness(self):
        self.screen.increase_brightness()

    def decrease_brightness(self):
        self.screen.decrease_brightness()

    def handle_button_a(self):
         self.screen.default_color = COLORS.WHITE

    def handle_button_b(self):
         self.screen.default_color = COLORS.RED

    def handle_button_c(self):
         self.screen.default_color = COLORS.GREEN

    def handle_button_d(self):
         self.screen.default_color = COLORS.BLUE

    def update(self, time_ms):

        action = self.buttons.update()

        if action:
            getattr(self, action)()
            time.sleep(0.5)

        if not self.sleep:
            if time_ms - self.last_update_time >= 60000:
                if not self.network.isconnected():
                    self.connect_wifi()

                self.last_update_time = time_ms
                data = self.tram_station.get()

                if len(data["trams"]): self.screen.set_trams(data["trams"])
                if not self.screen.message: self.screen.set_message(data["message"])
            
            self.screen.update(time_ms)         
