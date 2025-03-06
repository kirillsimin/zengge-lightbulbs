# Zengge Lightbulb CLI Utility

*Formerly known as Magic Hue utility*

This repository includes two scripts:

The `setup.py` script allows the user to connect the "Zengge" lightbulb to their Wi-Fi.
The `control.py` script provides an easy API for the "Zengge" lightbulbs.

## Installation

1. Plug in your Zengge lightbulb and turn it on. It will start flashing different colors.
2. Connect to its Wi-Fi (something like LEDnetE1234B).
3. Run the `setup.py` script, providing your SSID and your Wi-Fi password:

   ```
   python3 setup.py -ssid MyWifiEndpoint -pswd MyAwesomePassword
   ```

If the script worked, your lightbulb will turn green within a few seconds.

*Note: Currently, the script is automated for WPA2PSK / AES only. Modify it if your Wi-Fi uses a different mode and encryption.*

## Usage

Once your lightbulb is on your network, you can use the `zengge.py` script with the following arguments:

```
  -h, --help  show help message and exit
  -ip         provide the IP for the lightbulb; i.e. -ip 192.168.2.2
  -raw        accept colon-separated raw hex string; i.e. -raw 71:23:0f
  -rgb        accept comma-separated RGB values; i.e. -rgb 100,155,75
  -white      accept value of white temperature and brightness (0-255); i.e. -white 150,255
  -warm       accept value of warm white (0-255); i.e. -warm 150
  -cool       accept value of cool white (0-255); i.e. -cool 150
  -power      accept 'on' or 'off'; i.e. -power on
  -status     get the bulb's status
  -version    get the bulb's version
```

The user must provide the lightbulb's IP address and either RGB values, HEX values, or a white setting. An updated list of known combinations and rules for HEX values can be found below.

#### RGB Example:

This will set the lightbulb to red:

```
python3 control.py -ip 192.168.2.2 -rgb 200,0,0
```

#### White Example:

This will set the lightbulb to a specific white temperature and brightness:

```
python3 control.py -ip 192.168.2.2 -white 150,255
```

#### Warm White Example:

This will set the lightbulb to half power of warm white:

```
python3 control.py -ip 192.168.2.2 -warm 123
```

#### Raw Hex Example:

This will turn the lightbulb on with its last setting:

```
python3 control.py -ip 192.168.2.2 -raw 71:23:0f
```

## Understanding the Bulb's HEX Codes:

### Versions AK001-ZJ2101 & AK001-ZJ2145

I've been able to sniff a few codes that the app sends to the lightbulb. The structure of the hex list follows a pattern. The first bit defines the type of action. Then follow informational bits that define colors, brightness, etc. The entire list is followed by a checksum bit, masked by 255. For example, this is the broken-down list for turning the bulb on:

| Action Bit | Body Bit List | Finish Bit | Checksum Bit |
| ---------- | ------------- | ---------- | ------------ |
| `71`       | `24`          | `0f`       | `a4`         |

And here is how the data looks for magenta/purple color:

| Action Bit | Body Bit List    | Finish Bit | Checksum Bit |
| ---------- | ---------------- | ---------- | ------------ |
| `31`       | `ff:2f:ff:00:f0` | `0f`       | `5d`         |

**It's important to note that this script will calculate the checksum bit. You MUST NOT include it in the -raw argument.**

There are several different types of commands (Action Bits) that the bulb accepts:

- `31` - Color options
- `61` - Pulse/gradual options
- `71` - Power options
- `81` - Status options

The `31` and `61` action bit commands follow this structure in the body bit list:

```
31:RR:GG:BB:?BRIGHTNESS?:?COLORTYPE?:0f
61:COLOR(S):BRIGHTNESS:0f
```

The following examples can help you further understand the structure of the body bit list:

### HEX Examples

*Note that the final checksum bit is not included here. The script will add it automatically.*

| Action Type               | Values                 |
| ------------------------- | ---------------------- |
| On                        | `71:23:0f`             |
| Off                       | `71:24:0f`             |
|                           |                        |
| RGB (255,47,255)          | `31:ff:2f:ff:00:f0:0f` |
| RGB (255,126,0)           | `31:ff:7e:00:00:f0:0f` |
| RGB (0,79,255)            | `31:00:4f:ff:00:f0:0f` |
|                           |                        |
| Warm White 100%           | `31:00:00:00:ff:0f:0f` |
| Warm White 50%            | `31:00:00:00:80:0f:0f` |
| Warm White 1%             | `31:00:00:00:02:0f:0f` |
|                           |                        |
| 7 Color range, 100% speed | `61:25:1f:0f`          |
| 7 Color range, 50% speed  | `61:25:10:0f`          |
| 7 Color range, 1% speed   | `61:25:01:0f`          |
| Red gradual, 100% speed   | `61:26:1f:0f`          |
| Red gradual, 50% speed    | `61:26:10:0f`          |
| Green gradual, 100% speed | `61:27:1f:0f`          |
| Blue gradual, 100% speed  | `61:28:01:0f`          |

### Special Signature for AK001-ZJ21411

Firmware 11 has a very different signature and uses 23 bytes instead of 8 (or 9). Here are some parts I've been able to decipher:

b0b1b2b3000102 -- header, always the same
34 -- counter, keeps ticking up
000ee00100 -- filler ??
b1 - white / a1 - color
000000 - white, HEX values for Hue / 2, Saturation , Value if color (ie 006464)
00 -- warm / 64 cool
64 -- brightness for white
0000140000 -- filler?
24 -- checksum

| Header          | Counter | Filler       | Type  | White/Color HEX  | Warm/Cool | Brightness | Filler     | Checksum |
| -------------- | -------- | ----------- | ----- | ---------------- | --------- | ---------- | ---------- | -------- |
| `b0b1b2b3000102` | `34`   | `000ee00100` | `b1/a1` | `000000` / `006464` | `00/64`   | `64`       | `0000140000` | `24`      |

