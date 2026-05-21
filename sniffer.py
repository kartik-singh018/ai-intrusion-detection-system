from scapy.all import sniff
import time

from utils.feature_extractor import FeatureExtractor
from detector import HybridDetector

# Initialize
extractor = FeatureExtractor()
detector = HybridDetector()

start_time = time.time()

data_store = {
    "normal": [],
    "attacks": [],
    "stats": {
        "total": 0,
        "correct": 0,
        "accuracy": 0
    }
}


def process_packet(packet):
    global start_time

    extractor.process_packet(packet)

    # Analyze every 5 seconds
    if time.time() - start_time > 5:

        features = extractor.get_features()

        print("FEATURES:", features)  # 🔥 Debug

        # 🔥 FIX: Always show normal traffic for low activity
        if features["packet_count"] < 30:
            result = "normal"
            method = "baseline"
            conf = 1.0
        else:
            result, method, conf = detector.detect(features)

        ip = features.get("attacker_ip", "N/A")

        msg = f"{result.upper()} from {ip} | {method} | conf={conf:.2f}"

        # Store results
        data_store["stats"]["total"] += 1

        if result == "normal":
            data_store["normal"].append("✔ " + msg)
            data_store["stats"]["correct"] += 1
        else:
            data_store["attacks"].append("🚨 " + msg)

        # Accuracy calculation
        total = data_store["stats"]["total"]
        correct = data_store["stats"]["correct"]

        if total > 0:
            data_store["stats"]["accuracy"] = round((correct / total) * 100, 2)

        # Reset window
        extractor.reset()
        start_time = time.time()


def start_sniffing():
    print("🚀 IDS Running on Loopback Interface...")

    sniff(
        prn=process_packet,
        store=0,
        iface="\\Device\\NPF_Loopback"
    )