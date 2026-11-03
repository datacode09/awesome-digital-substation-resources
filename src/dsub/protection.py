"""Lesson 5 - Protection functions: 50/51 overcurrent, 87 differential, 21 distance."""
import math

# IEC 60255-151 inverse-time constants: t = TMS * k / ((I/Is)^alpha - 1)
IEC_CURVES = {
    "NI": (0.14, 0.02),     # standard inverse
    "VI": (13.5, 1.0),      # very inverse
    "EI": (80.0, 2.0),      # extremely inverse
    "LTI": (120.0, 1.0),    # long-time inverse
}


def iec_trip_time(i_pickup_multiple: float, tms: float, curve: str = "NI") -> float:
    """Operating time (s) for fault current = multiple x pickup. inf below pickup."""
    if i_pickup_multiple <= 1.0:
        return math.inf
    k, a = IEC_CURVES[curve]
    return tms * k / (i_pickup_multiple ** a - 1)


def definite_time_50(i: float, pickup: float, delay_s: float = 0.0) -> float:
    return delay_s if i >= pickup else math.inf


def grading_margin(upstream_t: float, downstream_t: float) -> float:
    """Coordination margin; typical target is 0.3-0.4 s (breaker + relay overtravel + CT error)."""
    return upstream_t - downstream_t


def differential_87(i1: complex, i2: complex, slope1: float = 0.25, slope2: float = 0.6,
                    i_min_op: float = 0.2, breakpoint: float = 2.0) -> tuple[bool, float, float]:
    """Dual-slope percentage differential. Currents in pu, both entering the zone.

    Returns (trip, i_diff, i_restraint).
    """
    i_diff = abs(i1 + i2)
    i_rest = (abs(i1) + abs(i2)) / 2
    threshold = i_min_op + (slope1 * i_rest if i_rest <= breakpoint
                            else slope1 * breakpoint + slope2 * (i_rest - breakpoint))
    return i_diff > threshold, i_diff, i_rest


def second_harmonic_block(i_fund: float, i_2nd: float, ratio: float = 0.15) -> bool:
    """Block differential during transformer inrush (2nd harmonic rich)."""
    return i_fund > 0 and (i_2nd / i_fund) > ratio


def mho_21(v: complex, i: complex, z_reach: complex) -> bool:
    """Self-polarised mho circle through the origin with diameter z_reach."""
    if abs(i) == 0:
        return False
    z = v / i
    centre = z_reach / 2
    return abs(z - centre) < abs(centre)


def zone_reach(line_z: complex, pct: float) -> complex:
    return line_z * pct
