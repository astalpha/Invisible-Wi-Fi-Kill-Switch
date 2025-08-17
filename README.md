# Wi-Fi Deauthentication Attack Detection (Windows Simulation)

## 📌 Project Overview
This project simulates the detection of Wi-Fi **deauthentication attacks** using Python.
Deauthentication attacks are a form of Wi-Fi Denial-of-Service (DoS) where an attacker sends forged `802.11` deauth frames to disconnect devices from a network.

On **Windows**, real-time 802.11 frame sniffing is not possible without special drivers and hardware. Therefore, this script **simulates** packet detection while producing realistic output for demonstration purposes.

---

## 🚀 Features
- Simulates normal and deauthentication Wi-Fi packets.
- Generates **realistic MAC addresses** for a natural look.
- Detects spikes in deauth frames within a time window.
- Logs attack alerts to `deauth_alerts.log`.
- Color-coded console output for clarity.

---

## 🛠 Installation
1. Install Python 3.x from [python.org](https://www.python.org/downloads/).
2. Download the script `deauth_detector_win.py`.
3. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

---

## 📥 How to Run
1. Open **PowerShell** or **Command Prompt** in the script's directory.
2. Run:
   ```bash
   python deauth_detector_win.py
   ```
3. Stop the script anytime with **CTRL + C**.

---

## ⚙ Parameters (Optional)
You can adjust detection parameters:
```bash
python deauth_detector_win.py --chance 0.25 --threshold 6 --window 8 --rate 0.3
```
- `--chance` → Probability (0..1) each packet is a deauth (default: 0.2)
- `--threshold` → Number of deauth frames in the time window to trigger alert (default: 5)
- `--window` → Time window in seconds (default: 10)
- `--rate` → Seconds between simulated packets (default: 0.5)

---

## 📄 Example Output
```
[*] Starting Deauth Detection Simulator (Windows 11)
    Threshold: 5 frames in 10s, Packet Rate: 0.5s

[ ] Normal packet from 00:1A:3F:89:7B:52
[!] Deauth frame detected from 2C:4B:5A:12:9F:7E
[!] Deauth frame detected from 40:6E:8F:AA:3B:44

[ALERT] 2025-08-10 15:05:13 - 5 deauth frames detected in last 10s | Suspects: 2C:4B:5A:12:9F:7E(3), 40:6E:8F:AA:3B:44(2)
```

---

## 📂 Files
- `deauth_detector_win.py` → Main script
- `deauth_alerts.log` → Log file for detected attack alerts

---

## 📌 Notes
- This script is **simulation only** on Windows.
- For real-time sniffing, use **Linux** (Kali) with a monitor mode-capable Wi-Fi adapter.

---

## 👨‍💻 Author
Anang Shashwat Tarun
