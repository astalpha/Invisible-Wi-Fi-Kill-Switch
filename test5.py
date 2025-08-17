#!/usr/bin/env python3


import random
import time
import argparse
from collections import deque
from datetime import datetime

# Simple ANSI color helpers (works on Win11 terminal)
CSI = "\033["
RESET = CSI + "0m"
RED = CSI + "31m"
GREEN = CSI + "32m"
YELLOW = CSI + "33m"
CYAN = CSI + "36m"

def pretty_print(msg, color=RESET):
    print(f"{color}{msg}{RESET}")

def rand_mac(prefix=None):
    # Generate a random MAC-like string. prefix optionally used for attacker MACs.
    if prefix:
        return prefix + ":" + ":".join(f"{random.randint(0,255):02X}" for _ in range(3))
    return ":".join(f"{random.randint(0,255):02X}" for _ in range(6))

def write_log(line, logfile="deauth_alerts.log"):
    with open(logfile, "a") as f:
        f.write(line + "\n")

def simulate_detector(deauth_chance=0.2, threshold=5, window=10, rate=0.5):
    """
    deauth_chance: probability (0..1) each packet is a deauth frame
    threshold: number of deauths in `window` seconds to trigger alert
    window: time window in seconds
    rate: seconds between generated packets
    """
    pretty_print("[*] Starting Deauth Detection Simulator (Windows)", CYAN)
    pretty_print(f"    deauth_chance={deauth_chance}, threshold={threshold}, window={window}s, packet_rate={rate}s\n", CYAN)

    # We keep a deque of timestamps (float seconds) for recent deauth frames
    deauth_times = deque()
    attacker_counts = {}  # count per attacker MAC for reporting

    try:
        while True:
            # Simulate incoming packet
            is_deauth = random.random() < deauth_chance
            if is_deauth:
                mac = rand_mac(prefix="FA:KE:MA")  # attacker-like MAC
                ts = time.time()
                deauth_times.append(ts)
                attacker_counts[mac] = attacker_counts.get(mac, 0) + 1
                pretty_print(f"[!] Deauth frame detected from {mac}", YELLOW)
            else:
                mac = rand_mac(prefix="NO:RM:AL")
                pretty_print(f"[ ] Normal packet from {mac}", GREEN)

            # Remove timestamps older than window
            now = time.time()
            while deauth_times and (now - deauth_times[0]) > window:
                deauth_times.popleft()

            # Check threshold
            current_count = len(deauth_times)
            if current_count >= threshold:
                # Compose alert message
                alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                top_attackers = sorted(attacker_counts.items(), key=lambda x: -x[1])[:3]
                attackers_str = ", ".join(f"{mac}({cnt})" for mac, cnt in top_attackers)
                alert_msg = (
                    f"[ALERT] {alert_time} - Possible Deauth Attack Detected! "
                    f"{current_count} deauth frames in last {window} seconds. Top: {attackers_str}"
                )
                pretty_print("\n" + alert_msg + "\n", RED)
                write_log(alert_msg)

                # Reset counts (start new detection cycle)
                deauth_times.clear()
                attacker_counts.clear()

            time.sleep(rate)

    except KeyboardInterrupt:
        pretty_print("\n[!] Exiting simulator (KeyboardInterrupt).", CYAN)
        pretty_print("  Check 'deauth_alerts.log' for any recorded alerts.", CYAN)


def main():
    parser = argparse.ArgumentParser(description="Deauth Detection Simulator (Windows-friendly)")
    parser.add_argument("--chance", type=float, default=0.2,
                        help="Probability each packet is a deauth (0..1). Default: 0.2")
    parser.add_argument("--threshold", type=int, default=5,
                        help="Number of deauth frames in the time window to trigger alert. Default: 5")
    parser.add_argument("--window", type=int, default=10,
                        help="Time window in seconds. Default: 10")
    parser.add_argument("--rate", type=float, default=0.5,
                        help="Seconds between simulated packets. Default: 0.5")
    parser.add_argument("--log", type=str, default="deauth_alerts.log",
                        help="Log file name. Default: deauth_alerts.log")

    args = parser.parse_args()

    # Ensure log file exists / append a header
    write_log(f"=== Deauth Simulator Log started at {datetime.now().isoformat()} ===", args.log)

    simulate_detector(deauth_chance=args.chance,
                      threshold=args.threshold,
                      window=args.window,
                      rate=args.rate)

if __name__ == "__main__":
    main()
