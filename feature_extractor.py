from scapy.all import TCP, Raw, IP

class FeatureExtractor:

    def __init__(self):
        self.reset()

    def reset(self):
        self.packet_count = 0
        self.syn_count = 0
        self.unique_ports = set()
        self.payload_size = 0
        self.connection_attempts = 0
        self.source_ips = {}

    def process_packet(self, packet):
        self.packet_count += 1

        # Track source IP
        if packet.haslayer(IP):
            src = packet[IP].src
            self.source_ips[src] = self.source_ips.get(src, 0) + 1

        if packet.haslayer(TCP):
            tcp = packet[TCP]

            # 🔥 FIXED SYN DETECTION
            if tcp.flags & 0x02:
                self.syn_count += 1
                self.connection_attempts += 1

            self.unique_ports.add(tcp.dport)

        if packet.haslayer(Raw):
            self.payload_size += len(packet[Raw].load)

    def get_features(self):
        attacker_ip = max(self.source_ips, key=self.source_ips.get) if self.source_ips else "N/A"

        return {
            "packet_count": self.packet_count,
            "syn_count": self.syn_count,
            "unique_ports": len(self.unique_ports),
            "payload_size": self.payload_size,
            "connection_attempts": self.connection_attempts,
            "attacker_ip": attacker_ip
        }