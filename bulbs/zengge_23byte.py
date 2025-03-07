import colorsys
from .zengge import Zengge

class Zengge23Byte(Zengge):
    def process_white(self, white):
        temp, brightness = map(int, white)

        temp_hex = f"{temp:02x}"
        brightness_hex = f"{brightness:02x}"

        values = self.process_raw(
            f"b0:b1:b2:b3:00:01:02:00:00:0e:e0:01:00:b1:00:00:00:{temp_hex}:{brightness_hex}:00:00:14:00:00"
        )
        
        return values

    def process_rgb(self, rgb):
        rgb_values = rgb.split(',')
        if len(rgb_values) < 3:
            self.print_error("Must have three color values (0-255) for R,G,B")

        r, g, b = map(int, rgb_values)
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

        half_hue = int((h * 360) / 2)  # Hue is divided by 2 (would love to know why!)
        saturation = int(s * 100)
        value = int(v * 100)

        half_hue_hex = f"{half_hue:02x}"
        saturation_hex = f"{saturation:02x}"
        value_hex = f"{value:02x}"

        values = self.process_raw(
            f"b0:b1:b2:b3:00:01:02:75:00:0e:e0:01:00:a1:{half_hue_hex}:{saturation_hex}:{value_hex}:00:00:00:00:14:00:00"
        )

        return values
