from tabulate import tabulate

class NetworkStats(object):
    def __init__(self) -> None:
        self.udp_packet_rx = 0
        self.udp_packet_tx = 0
        self.udp_packet_drop_rx = 0
        self.udp_packet_drop_tx = 0
        self.udp_bytes_rx = 0
        self.udp_bytes_tx = 0
        self.tcp_packet_rx = 0
        self.tcp_packet_tx = 0
        self.tcp_packet_drop_rx = 0
        self.tcp_packet_drop_tx = 0
        self.tcp_bytes_rx = 0
        self.tcp_bytes_tx = 0
        self.icmp_packet_rx = 0
        self.icmp_packet_tx = 0
        self.icmp_packet_drop_rx = 0
        self.icmp_packet_drop_tx = 0
        self.icmp_bytes_rx = 0
        self.icmp_bytes_tx = 0
        self.rx_latency = 0
        self.tx_latency = 0

    def __str__(self) -> str:
        table_header = ['Metric', 'Value']
        table_rows = [
            [ "UDP: Packets Received",      self.udp_packet_rx ],
            [ "UDP: Packets Sent",          self.udp_packet_tx ],
            [ "UDP: Rx Packets Dropped",    self.udp_packet_drop_rx ],
            [ "UDP: Tx Packets Dropped",    self.udp_packet_drop_tx ],
            [ "UDP: Bytes Received",        self.udp_bytes_rx ],
            [ "UDP: Bytes Sent",            self.udp_bytes_tx ],
            [ "TCP: Packets Received",      self.tcp_packet_rx ],
            [ "TCP: Packets Sent",          self.tcp_packet_tx ],
            [ "TCP: Rx Packets Dropped",    self.tcp_packet_drop_rx ],
            [ "TCP: Tx Packets Dropped",    self.tcp_packet_drop_tx ],
            [ "TCP: Bytes Received",        self.tcp_bytes_rx ],
            [ "TCP: Bytes Sent",            self.tcp_bytes_tx ],
            [ "ICMP: Packets Received",     self.icmp_packet_rx ],
            [ "ICMP: Packets Sent",         self.icmp_packet_tx ],
            [ "ICMP: Rx Packets Dropped",   self.icmp_packet_drop_rx ],
            [ "ICMP: Tx Packets Dropped",   self.icmp_packet_drop_tx ],
            [ "ICMP: Bytes Received",       self.icmp_bytes_rx ],
            [ "ICMP: Bytes Sent",           self.icmp_bytes_tx ],
            [ "Rx Latency",                 self.rx_latency ],
            [ "Tx Latency",                 self.tx_latency ],
        ]
        return tabulate(table_rows, headers=table_header, tablefmt="grid")

def deserialize_network_stats(network_stats_str):
    deserialized_stats = NetworkStats()
    all_stats = network_stats_str.split(',')

    if len(all_stats) == 20:
        deserialized_stats.udp_packet_rx = all_stats[0]
        deserialized_stats.udp_packet_tx = all_stats[1]
        deserialized_stats.udp_packet_drop_rx = all_stats[2]
        deserialized_stats.udp_packet_drop_tx = all_stats[3]
        deserialized_stats.udp_bytes_rx = all_stats[4]
        deserialized_stats.udp_bytes_tx = all_stats[5]
        deserialized_stats.tcp_packet_rx = all_stats[6]
        deserialized_stats.tcp_packet_tx = all_stats[7]
        deserialized_stats.tcp_packet_drop_rx = all_stats[8]
        deserialized_stats.tcp_packet_drop_tx = all_stats[9]
        deserialized_stats.tcp_bytes_rx = all_stats[10]
        deserialized_stats.tcp_bytes_tx = all_stats[11]
        deserialized_stats.icmp_packet_rx = all_stats[12]
        deserialized_stats.icmp_packet_tx = all_stats[13]
        deserialized_stats.icmp_packet_drop_rx = all_stats[14]
        deserialized_stats.icmp_packet_drop_tx = all_stats[15]
        deserialized_stats.icmp_bytes_rx = all_stats[16]
        deserialized_stats.icmp_bytes_tx = all_stats[17]
        deserialized_stats.rx_latency = all_stats[18]
        deserialized_stats.tx_latency = all_stats[19]

    return deserialized_stats
