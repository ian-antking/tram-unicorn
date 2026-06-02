import COLORS

STEP_TIME = 1
MAX_DESTINATION_WIDTH = 100  # pixels; leaves room for wait time on 128px wide display

class Tram:
    def __init__(self, destination, wait, status, index, graphics):
        self.destination = destination
        self.wait = wait
        self.status = status
        self.destination_x = 1
        self.wait_x = 105
        self.y = (index * 10) + 12
        self.graphics = graphics

    def get_destination_text(self):
        """Return destination truncated to fit within MAX_DESTINATION_WIDTH pixels."""
        text = self.destination
        while self.graphics.measure_text(text, 1) > MAX_DESTINATION_WIDTH and len(text) > 0:
            text = text[:-1]
        if text != self.destination:
            text = text[:-1] + "~"  # trailing ~ to indicate truncation
        return text
    
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
