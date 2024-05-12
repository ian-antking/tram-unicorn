class ButtonController:
    def __init__(self, cosmic_unicorn):
        self.cu = cosmic_unicorn

    def update(self):
        if self.cu.is_pressed(self.cu.SWITCH_VOLUME_UP):
            return "display_incoming"

        if self.cu.is_pressed(self.cu.SWITCH_VOLUME_DOWN):
            return "display_outgoing"

        if self.cu.is_pressed(self.cu.SWITCH_SLEEP):
            return "handle_sleep"

        if self.cu.is_pressed(self.cu.SWITCH_BRIGHTNESS_UP):
            return "increase_brightness"
        
        if self.cu.is_pressed(self.cu.SWITCH_BRIGHTNESS_DOWN):
            return "decrease_brightness"

        if self.cu.is_pressed(self.cu.SWITCH_A):
            return "handle_button_a"

        if self.cu.is_pressed(self.cu.SWITCH_B):
            return "handle_button_b"

        if self.cu.is_pressed(self.cu.SWITCH_C):
            return "handle_button_c"

        if self.cu.is_pressed(self.cu.SWITCH_D):
            return "handle_button_d"

        return None
