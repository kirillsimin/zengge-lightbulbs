import socket
import json
import sys

class Zengge:
    def __init__(self, ip):
        self.ip = ip

    def add_checksum(self, values):
        command = bytearray(values)
        checksum = sum(values) % 256
        command.append(checksum)
        return command

    def get_status(self):
        try:
            data = bytearray(self.process_raw('81:8a:8b:96'))
            s = socket.socket()
            s.settimeout(3)
            s.connect((self.ip, 5577))
            s.send(data)
            response = s.recvfrom(1024)
            response = [hex(s).replace('0x', '') for s in response[0]]
            response = ['0' + s if len(s) == 1 else s for s in response]

            # format and print out
            power = response[2]
            power = 'on' if power == '23' else power
            power = 'off' if power == '24' else power
            
            rgb = response[6:9]
            for i,c in enumerate(rgb):
                rgb[i] = int('0x'+c, 16)
            
            warm = int('0x'+response[9], 16)
            out = {"power" : power, "rgb" : rgb, "warm" : warm}
            print(json.dumps(out))

            return response
        except:
            self.print_error("Could not get the bulb's status")
            return None

    def get_version(self):
        try:
            data = b"HF-A11ASSISTHREAD"
            s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            s.settimeout(3)
            s.sendto(data, (self.ip, 48899))
            response = s.recvfrom(1024)
            msg = response[0].decode('utf-8')
            version = msg.split(',')
            return version[2]
        except:
            self.print_error("Could not get the bulb's version")
            return None

    def print_version(self):
        try:
            data = b"HF-A11ASSISTHREAD"
            s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            s.settimeout(3)
            s.sendto(data, (self.ip, 48899))
            response = s.recvfrom(1024)
            msg = response[0].decode('utf-8')
            version = msg.split(',')
            print(version)
        except:
            self.print_error("Could not get the bulb's version")
            return None

    def send(self, values):
        try:
            command = self.add_checksum(values)
            s = socket.socket()
            s.settimeout(3)
            s.connect((self.ip, 5577))
            s.sendall(command)
            print(json.dumps({"success": True}))
        except:
            self.print_error("Could not send the message to the bulb")
        
        sys.exit()

    def add_header(self):
        pass

    def _calculate_white_hex(self, white):
        """Helper to calculate warm and cold hex values from white input."""
        temp, brightness = map(int, white)

        warm = ((255 - temp) * brightness) // 255
        cold = (temp * brightness) // 255

        return f"{warm:02x}", f"{cold:02x}"

    def process_white(self, white):
        warm_hex, cold_hex = self._calculate_white_hex(white)
        return self.process_raw(f"31:00:00:00:{warm_hex}:{cold_hex}:0f")

    def process_raw(self, raw):
        raw = raw.split(':')
        values = ['0x' + s for s in raw]
        values = [int(v, 16) for v in values]
        return values

    def _parse_rgb(self, rgb):
        """Helper to parse and validate RGB input."""
        rgb_values = rgb.split(',')
        if len(rgb_values) < 3:
            self.print_error('Must have three color values (0-255) for R,G,B')
        values = [int(v) for v in rgb_values]
        values.insert(0, 49)
        return values

    def process_rgb(self, rgb):
        values = self._parse_rgb(rgb)
        values.extend([0, 240, 15])  # Common RGB suffix
        return values

    def process_power(self, power):
        if power == 'on':
            return self.process_raw('71:23:0f')
        if power == 'off':
            return self.process_raw('71:24:0f')

    def print_error(self, message):
        print(json.dumps({"success": False, "error": message}))
        sys.exit()
