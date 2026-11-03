"""Lesson 2 - IEC 61850-9-2 Sampled Values (process bus).

9-2LE (UCA implementation guideline) fixes 80 samples/cycle for protection
(4000 Hz at 50 Hz, 4800 Hz at 60 Hz) and 256 samples/cycle for power quality.
Each ASDU carries 4 currents + 4 voltages as INT32 plus a quality word.
Scaling: currents in 1 mA/LSB, voltages in 10 mV/LSB.
"""
import math
import struct
from dataclasses import dataclass

I_SCALE = 0.001   # A per LSB
V_SCALE = 0.01    # V per LSB


def samples_per_second(freq_hz: float = 50.0, spc: int = 80) -> float:
    return freq_hz * spc


def sample_period_us(freq_hz: float = 50.0, spc: int = 80) -> float:
    return 1e6 / samples_per_second(freq_hz, spc)


def three_phase(peak: float, freq_hz: float, n: int, spc: int, phase_deg: float = 0.0,
                sequence: str = "abc") -> list[tuple[float, float, float]]:
    """Generate n samples of a balanced 3-phase sinusoid (positive or negative sequence)."""
    shift = 120.0 if sequence == "abc" else -120.0
    out = []
    for k in range(n):
        wt = 2 * math.pi * k / spc
        p = math.radians(phase_deg)
        out.append((
            peak * math.sin(wt + p),
            peak * math.sin(wt + p - math.radians(shift)),
            peak * math.sin(wt + p + math.radians(shift)),
        ))
    return out


@dataclass
class SvAsdu:
    sv_id: str
    smp_cnt: int
    conf_rev: int
    smp_synch: int          # 0 none, 1 local clock, 2 global (GPS/PTP)
    values: list[int]       # 8 INT32: Ia Ib Ic In Va Vb Vc Vn
    quality: list[int]      # 8 uint32 quality words

    def encode(self) -> bytes:
        """Simplified fixed-layout encoding (real SV uses ASN.1 BER; see goose.py for BER)."""
        sid = self.sv_id.encode().ljust(16, b"\0")[:16]
        body = struct.pack(">16sHIB", sid, self.smp_cnt, self.conf_rev, self.smp_synch)
        for v, q in zip(self.values, self.quality):
            body += struct.pack(">iI", v, q)
        return body

    @classmethod
    def decode(cls, raw: bytes) -> "SvAsdu":
        sid, cnt, rev, sync = struct.unpack_from(">16sHIB", raw)
        off = struct.calcsize(">16sHIB")
        vals, qual = [], []
        for _ in range(8):
            v, q = struct.unpack_from(">iI", raw, off)
            vals.append(v); qual.append(q); off += 8
        return cls(sid.rstrip(b"\0").decode(), cnt, rev, sync, vals, qual)

    def engineering_values(self) -> list[float]:
        return [v * (I_SCALE if i < 4 else V_SCALE) for i, v in enumerate(self.values)]


def make_stream(i_peak_a: float, v_peak_v: float, freq_hz: float = 50.0, spc: int = 80,
                cycles: int = 1, sv_id: str = "MU01") -> list[SvAsdu]:
    n = spc * cycles
    cur = three_phase(i_peak_a, freq_hz, n, spc, phase_deg=-30)
    vol = three_phase(v_peak_v, freq_hz, n, spc)
    asdus = []
    for k in range(n):
        ia, ib, ic = (round(x / I_SCALE) for x in cur[k])
        va, vb, vc = (round(x / V_SCALE) for x in vol[k])
        asdus.append(SvAsdu(sv_id, k % int(samples_per_second(freq_hz, spc)), 1, 2,
                            [ia, ib, ic, ia + ib + ic, va, vb, vc, va + vb + vc], [0] * 8))
    return asdus


def lost_samples(counters: list[int], modulus: int) -> int:
    """Count missing smpCnt values in a received stream (a protection relay must detect these)."""
    lost = 0
    for prev, cur in zip(counters, counters[1:]):
        gap = (cur - prev) % modulus
        lost += max(gap - 1, 0)
    return lost
