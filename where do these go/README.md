# Digital Cluster for Full-Size Bronco / GMC Sierra

A fully custom digital instrument cluster built using a Raspberry Pi 3B, CAN Bus integration, ADC for analog sensors, UPS battery backup, active cooling, touchscreen interface, and a complete Kivy-powered UI.

---

## 📦 Features

- ✅ CAN Bus support with the Waveshare 2-Channel Isolated HAT (MCP2515 + SN65HVD230)
- ✅ Real-time analog fuel gauge input using ADC (15–160Ω sender + 100Ω pull-up)
- ✅ Animated speedometer & tachometer with redline flash
- ✅ Transmission, coolant, oil, AFR, voltage & UPS battery monitoring
- ✅ Sensor smoothing, hysteresis, fault detection
- ✅ Alert icons with detailed touch overlays
- ✅ Night mode & brightness auto-adjust via TSL25911FN light sensor
- ✅ Touchscreen UI with drag-and-drop customizable gauges
- ✅ Layout profiles with save/load/export/import
- ✅ Diagnostic Trouble Code (DTC) viewer with log decoding & clearing
- ✅ CAN traffic logger for reverse engineering
- ✅ UPS-triggered safe shutdown handling
- ✅ Auto-update checker (Wi-Fi only)

---

## 🖥️ Hardware Requirements

- Raspberry Pi 3B (or later)
- Waveshare 7" IPS Touchscreen (1024x600 HDMI)
- Waveshare 2-Channel Isolated CAN Bus Expansion HAT
- Waveshare High-Precision AD HAT (ADC)
- Waveshare UPS HAT (2x Samsung 30Q 18650 batteries)
- 2x Noctua NF-A4x10 5V PWM Fans (GPIO 13, 18)
- Waveshare AM2302 (Temp/Humidity Sensor, GPIO 4)
- TSL25911FN Ambient Light Sensor (I2C)
- 128GB SanDisk Extreme microSDXC UHS-I card

---

## 🧰 Installation

### 1. Clone this Repository

```bash
git clone https://github.com/Broncorniclops/Digital-cluster.git
cd Digital-cluster
```

### 2. Run the Installer

```bash
sudo bash install/install_with_reboot.sh
```

This script will:
- Install Python packages
- Set up systemd services
- Apply file permissions
- Reboot the system

---

## 🧠 Usage

- System will start automatically on boot
- Touchscreen launches the `main.py` UI
- Settings menu allows layout editing, toggles, log cleanup, and more
- Alerts will appear with red icons — tap for details
- CAN errors or faults automatically display DTC viewer

---

## 📁 File Structure Overview

```plaintext
Digital-cluster/
├── main.py
├── install/
├── services/
├── config/
├── modules/
├── ui/
├── gauges/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🤝 Contributing

Pull requests are welcome! Please submit changes to a separate branch or fork the repo.

---

## 📜 License

MIT License — feel free to adapt this project for your own vehicle builds!

---

## 📷 Screenshots

Coming soon — preview images of the cluster UI and setup.
