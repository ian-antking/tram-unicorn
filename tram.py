import COLORS
import time

STEP_TIME = 1

class Tram:
    def __init__(self, destination, wait, status, index, graphics):
        dest_len = len(destination)
        self.destination = destination
        self.wait = wait
        self.status = status
        self.destination_x = 0
        self.wait_x = 105
        self.y = index * 8
        self.graphics = graphics
    
    def get_wait_text(self):
        text = "{wait}min".format(wait=self.wait) if len(self.wait) == 2 else " {wait}min".format(wait=self.wait)

        if self.wait == "0":
            text = self.status
        
        self.wait_x = 128 - self.graphics.measure_text(text, 1)

        return text
    
    def get_status_color(self):
        if self.status == "Arrived" or self.status == "Departing":
            return COLORS.INFO
        
        if self.status == "Due":
            return COLORS.OK
        
        if self.status == "Delay":
            return COLORS.WARNING
        
        return COLORS.ERROR
