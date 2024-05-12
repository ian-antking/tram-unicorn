STATE_PRE_SCROLL = "pre-scroll"
STATE_SCROLLING = "scrolling"
STATE_POST_SCROLL = "post-scroll"
PADDING = 5
HOLD_TIME = 2.0
STEP_TIME = 0.075

class ScrollText:
    def __init__(self, text, screen_width, screen_height, y, color, message_width):
        self.text = text
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 0
        self.y = y
        self.state = STATE_PRE_SCROLL
        self.last_update = 0
        self.text_color = color
        self.msg_width = message_width

    def update(self, time_ms):
        if self.state == STATE_PRE_SCROLL and time_ms - self.last_update > HOLD_TIME * 1000:
            if self.msg_width + PADDING * 2 >= self.screen_width:
                self.state = STATE_SCROLLING
            self.last_update = time_ms

        if self.state == STATE_SCROLLING and time_ms - self.last_update > STEP_TIME * 1000:
            self.x += 1
            if self.x >= (self.msg_width + self.screen_width) - 1:
                self.state = STATE_POST_SCROLL
            self.last_update = time_ms

        if self.state == STATE_POST_SCROLL and time_ms - self.last_update > HOLD_TIME * 500:
            self.state = STATE_PRE_SCROLL
            self.x = 0
            self.last_update = time_ms