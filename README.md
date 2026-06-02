# 🚊 tram-unicorn

A MicroPython app for the [Pimoroni Interstate75](https://shop.pimoroni.com/products/interstate-75) LED matrix controller that displays live Manchester Metrolink tram departure times.

## 📺 What it does

Shows upcoming trams from a configured Metrolink station on a 128×64 LED matrix display — destination, wait time, and status — updating every 60 seconds. Switch between incoming and outgoing trams with the onboard buttons.

## 🛠 Hardware

- [Pimoroni Interstate75](https://shop.pimoroni.com/products/interstate-75) (128×64 display)
- Any compatible 128×64 HUB75 LED matrix panel
- WiFi network

## 🚀 Setup

### 1. Flash MicroPython

Flash the [Pimoroni MicroPython build](https://github.com/pimoroni/pimoroni-pico/releases) for Interstate75 onto your board.

### 2. Configure WiFi

Copy `WIFI_CONFIG.example.py` to `WIFI_CONFIG.py` and fill in your network details:

```python
SSID = "your-network"
PSK = "your-password"
COUNTRY = "GB"
```

### 3. Configure your station

Copy `CONFIG.example.py` to `CONFIG.py` and set your station name and TfGM API key:

```python
TRAM_STATION = "Eccles"
API_KEY = "your-tfgm-api-key"
```

Get a free API key from the [TfGM Developer Portal](https://developer.tfgm.com/).

### 4. Upload files

Upload all `.py` files to the root of your Interstate75 using [Thonny](https://thonny.org/) or `mpremote`.

## 🎮 Controls

| Button | Action |
|--------|--------|
| **A** | Show incoming trams (towards city) |
| **B** | Show outgoing trams (from city) |

## 🎨 Display

Each row shows:
- **Destination** — truncated with `~` if too long to fit
- **Wait time** — in minutes, or status if due/arrived

Colour indicates tram status:
- 🟢 **Green** — Due
- 🔵 **Blue** — Arriving / Departing  
- 🟡 **Amber** — Delayed
- 🔴 **Red** — Cancelled

## 🔄 Updates

The app supports OTA updates via `update.py`. Drop updated files into the configured update source and they'll be pulled on next boot.

## 📦 Dependencies

All dependencies are provided by the Pimoroni MicroPython firmware — no additional packages needed.
