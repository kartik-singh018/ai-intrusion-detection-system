import joblib
import numpy as np

model = joblib.load("model.pkl")


class HybridDetector:

    def rule_based_detection(self, f):

        # 🔵 PROBE FIRST (many ports)
        if f["unique_ports"] > 20:
            return "probe"

        # 🟣 U2R (many attempts, low SYN)
        if (
            f["connection_attempts"] > 50 and
            f["syn_count"] < 30
        ):
            return "u2r"

        # 🔴 DoS LAST (high SYN flood)
        if f["syn_count"] > 80:
            return "dos"

        return None

    def ml_detection(self, f):

        X = [[
            f["packet_count"],
            f["syn_count"],
            f["unique_ports"],
            f["payload_size"],
            f["connection_attempts"]
        ]]

        pred = model.predict(X)[0]
        prob = np.max(model.predict_proba(X))

        if prob < 0.5:
            return "normal", prob

        return pred, prob

    def detect(self, f):

        rule = self.rule_based_detection(f)
        if rule:
            return rule, "rule-based", 1.0

        pred, prob = self.ml_detection(f)
        return pred, "ml", prob