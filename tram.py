import COLORS
import time

STEP_TIME = 1

class Tram:
    def __init__(self, destination, wait, status, index):
        dest_len = len(destination)
        self.destination = destination if dest_len == 16 else destination + " " * (16 - dest_len)
        self.wait = wait
        self.status = status
        self.destination_x = 0
        self.wait_x = 23
        self.y = index * 8
        self.last_update = time.ticks_ms()
        self.slice_start = 0
        self.slice_end = 4

    def get_destination_text(self):
        return self.destination[self.slice_start: self.slice_end]
    
    def get_wait_text(self):
        return self.wait if len(self.wait) == 2 else " {wait}".format(wait=self.wait)
    
    def get_status_color(self):
        if self.status == "Arrived" or self.status == "Departing":
            return COLORS.INFO
        
        if self.status == "Due":
            return COLORS.OK
        
        if self.status == "Delay":
            return COLORS.WARNING
        
        return COLORS.ERROR
    
    def should_update(self, time_ms):
        return time_ms - self.last_update > STEP_TIME * 1000

    def update(self, time_ms):      
        if  self.should_update(time_ms):
            self.slice_start += 1
            self.slice_end += 1

            if self.slice_end > len(self.destination):
                self.slice_start = 0
                self.slice_end = 4

            self.last_update = time_ms
