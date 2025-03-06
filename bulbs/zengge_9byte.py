import socket
import json
from .zengge import Zengge

class Zengge9Byte(Zengge):

    def process_rgb(self, rgb):
        rgb = rgb.split(',')
        if len(rgb) < 3:
            self.print_error('Must have three color values (0-255) for R,G,B')
        values = [int(v) for v in rgb]
        values.insert(0, 49)
        
        values.extend([0, 0, 240, 15])
        return values
    
    def process_white(self, white):
        temp, brightness = map(int, white) 

        warm = ((255 - temp) * brightness) // 255
        cold = (temp * brightness) // 255

        warm_hex = f"{warm:02x}"
        cold_hex = f"{cold:02x}"

        values = self.process_raw(f"31:00:00:00:{warm_hex}:{cold_hex}:0f:0f")

        return values