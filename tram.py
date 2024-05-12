import COLORS

class Tram:
    def __init__(self, destination, wait, status, index):
        self.destination = destination
        self.wait = wait
        self.status = status
        self.y = index * 8
        self.x = 0

    def get_text(self):
        return "{destination}: {wait}".format(destination=self.destination[0:3], wait=self.wait)
    
    def get_status_color(self):
        if self.status == "Arrived" or self.status == "Departing":
            return COLORS.INFO
        if self.status == "Due":
            return COLORS.OK
        if self.status == "Delay":
            return COLORS.WARNING
        return COLORS.ERROR
        