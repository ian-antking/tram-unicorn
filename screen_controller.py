import COLORS
from scroll_text import ScrollText
from tram import Tram

BACKGROUND_COLOUR = (0, 0, 0)
MESSAGE_Y = 24

class Screen():
    def __init__(self, screen, graphics, time_ms, background_color= BACKGROUND_COLOUR, default_text_color= COLORS.WHITE):
        self.screen = screen
        self.graphics = graphics
        self.width = self.screen.width
        self.height = screen.height
        self.last_update = time_ms
        self.background_color = background_color
        self.default_color = default_text_color

        self.trams = []
        self.message = None

        self.graphics.set_font('bitmap8')

        self.destination_index = 0

    def clear_screen(self):
        self.graphics.set_pen(self.graphics.create_pen(*self.background_color))
        self.graphics.clear()

    def make_text(self, text, x, y, color= None):
        self.graphics.set_pen(self.graphics.create_pen(*color or self.default_color))
        self.graphics.text(text, x, y, -1, 1)

    def display_message(self, messages, color= None):
        self.clear_screen()
        for message in messages:
            self.make_text(message, 0, 8 * messages.index(message), color or self.default_color)
        self.screen.update(self.graphics)

    def set_trams(self, trams):
        self.trams = []
        for i, tram in enumerate(trams):
            new_tram = Tram(tram["destination"], tram["wait"], tram["status"], i, self.graphics)
            self.trams.append(new_tram)

    def set_message(self, message, color= None):
        self.message = ScrollText(message, self.width, self.height, 24, color or self.default_color, self.graphics.measure_text(message, 1))

    def update(self, time_ms):

        self.clear_screen()

        for tram in self.trams:
            self.graphics.set_pen(self.graphics.create_pen(*tram.get_status_color()))
            self.graphics.line(tram.destination_x, tram.y + 7 , self.width, tram.y + 7)
            self.make_text(tram.destination, tram.destination_x, tram.y)
            self.make_text(tram.get_wait_text(), tram.wait_x, tram.y)

        if self.message:
            self.message.update(time_ms)
            self.make_text(self.message.text, x=self.width - self.message.x, y=MESSAGE_Y)
        
        if self.message and self.message.state == "post-scroll":
            self.message = None
            
        self.screen.update(self.graphics)

