import uasyncio # type: ignore
import WIFI_CONFIG
from API import Direction
import COLORS
import time

class App:
    def __init__(self, network_manager, screen_manager, station_repository):
        self.network = network_manager
        self.screen = screen_manager
        self.tram_station = station_repository
        self.last_update_time = 0
        self.direction = Direction.INCOMING

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

    def get_data(self, updateNow=False):
        data = self.tram_station.get(updateNow)
        self.screen.set_trams(data["trams"], self.direction)
        self.screen.set_message(data["message"])


    def display_incoming(self):
            self.direction = Direction.INCOMING
            self.tram_station.set_destination(self.direction)
            self.screen.display_message(["getting", self.direction, "trams"], COLORS.INFO)
            self.get_data(updateNow=True)

    def display_outgoing(self):
            self.direction = Direction.OUTGOING
            self.tram_station.set_destination(self.direction)
            self.screen.display_message(["getting", self.direction, "trams"], COLORS.INFO)
            self.get_data(updateNow=True)

    def update(self, time_ms):

        if time_ms - self.last_update_time >= 60000:
            if not self.network.isconnected():
                self.connect_wifi()

            self.last_update_time = time_ms
            data = self.tram_station.get()

            if len(data["trams"]): self.screen.set_trams(data["trams"], self.direction)
            if not self.screen.message: self.screen.set_message(data["message"])
        
        self.screen.update(time_ms)         
