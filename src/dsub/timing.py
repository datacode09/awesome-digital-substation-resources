"""Lesson 7 - Time, redundancy and latency budgets on the process bus."""
from dataclasses import dataclass


def ptp_offset_delay(t1: float, t2: float, t3: float, t4: float) -> tuple[float, float]:
    """IEEE 1588 delay request-response. Returns (offset_of_slave, mean_path_delay) in seconds.

    t1 master Sync tx, t2 slave Sync rx, t3 slave Delay_Req tx, t4 master Delay_Req rx.
    """
    offset = ((t2 - t1) - (t4 - t3)) / 2
    delay = ((t2 - t1) + (t4 - t3)) / 2
    return offset, delay


def phase_error_deg(time_error_s: float, freq_hz: float = 50.0) -> float:
    """1 microsecond at 50 Hz = 0.018 degrees. IEC 61850-9-3 class: <=1 us for PTP profile."""
    return 360.0 * freq_hz * time_error_s


def frame_serialization_us(frame_bytes: int, link_mbps: float = 100.0) -> float:
    # + preamble/SFD (8) + IFG (12)
    return (frame_bytes + 20) * 8 / link_mbps


@dataclass
class LatencyBudget:
    """GOOSE trip class P1 (IEC 61850-5) requires transfer time <= 3 ms (TT6 for trips)."""
    publisher_processing_ms: float = 0.5
    serialization_ms: float = 0.0
    switch_hops: int = 2
    per_hop_ms: float = 0.05   # store-and-forward switch
    subscriber_processing_ms: float = 0.5

    def total_ms(self) -> float:
        return (self.publisher_processing_ms + self.serialization_ms
                + self.switch_hops * self.per_hop_ms + self.subscriber_processing_ms)

    def meets(self, limit_ms: float = 3.0) -> bool:
        return self.total_ms() <= limit_ms


def prp_accept(seen: set[tuple[bytes, int]], src_mac: bytes, seq: int) -> bool:
    """PRP (IEC 62439-3): send on LAN A and B; receiver keeps first copy, drops duplicate."""
    key = (src_mac, seq)
    if key in seen:
        return False
    seen.add(key)
    return True


def availability(mtbf_h: float, mttr_h: float, redundant: bool = False) -> float:
    a = mtbf_h / (mtbf_h + mttr_h)
    return 1 - (1 - a) ** 2 if redundant else a
