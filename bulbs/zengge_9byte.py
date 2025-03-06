from .zengge import Zengge

class Zengge9Byte(Zengge):

    def process_white(self, white):
        warm_hex, cold_hex = self._calculate_white_hex(white)
        return self.process_raw(f"31:00:00:00:{warm_hex}:{cold_hex}:0f:0f")

    def process_rgb(self, rgb):
        values = self._parse_rgb(rgb)
        values.extend([0, 0, 240, 15])
        return values