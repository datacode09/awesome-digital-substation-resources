"""Lesson 1 - Phasors, DFT and symmetrical components.

Protection relays reduce sampled waveforms to phasors, then apply logic on them.
"""
import cmath
import math

A = cmath.rect(1.0, 2 * math.pi / 3)  # the 120-degree operator "a"


def polar(mag: float, angle_deg: float) -> complex:
    return cmath.rect(mag, math.radians(angle_deg))


def to_polar(z: complex) -> tuple[float, float]:
    """Return (magnitude, angle in degrees)."""
    return abs(z), math.degrees(cmath.phase(z))


def dft_phasor(samples: list[float], samples_per_cycle: int) -> complex:
    """Fundamental-frequency RMS phasor from exactly one cycle of samples (full-cycle DFT)."""
    n = samples_per_cycle
    if len(samples) < n:
        raise ValueError("need at least one full cycle of samples")
    acc = sum(samples[k] * cmath.exp(-2j * math.pi * k / n) for k in range(n))
    return acc * math.sqrt(2) / n * 1j  # cos reference -> RMS phasor (sin => 0 deg at k=0 after j)


def sequence_components(va: complex, vb: complex, vc: complex) -> tuple[complex, complex, complex]:
    """Fortescue transform: return (zero, positive, negative)."""
    v0 = (va + vb + vc) / 3
    v1 = (va + A * vb + A * A * vc) / 3
    v2 = (va + A * A * vb + A * vc) / 3
    return v0, v1, v2


def abc_from_sequence(v0: complex, v1: complex, v2: complex) -> tuple[complex, complex, complex]:
    return (
        v0 + v1 + v2,
        v0 + A * A * v1 + A * v2,
        v0 + A * v1 + A * A * v2,
    )
