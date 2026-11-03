"""Lesson 6 - Fault calculation with symmetrical components (per-unit or ohms)."""
from .phasors import A, abc_from_sequence


def three_phase_fault(v_prefault: complex, z1: complex, zf: complex = 0) -> complex:
    return v_prefault / (z1 + zf)


def slg_fault(v: complex, z1: complex, z2: complex, z0: complex, zf: complex = 0):
    """Single line-to-ground (phase A). Returns (Ia_fault, (I0, I1, I2))."""
    i1 = v / (z1 + z2 + z0 + 3 * zf)
    return 3 * i1, (i1, i1, i1)


def ll_fault(v: complex, z1: complex, z2: complex, zf: complex = 0):
    """Line-to-line (phases B-C). Returns (Ib, Ic)."""
    i1 = v / (z1 + z2 + zf)
    i2 = -i1
    _, ib, ic = abc_from_sequence(0, i1, i2)
    return ib, ic


def dlg_fault(v: complex, z1: complex, z2: complex, z0: complex, zf: complex = 0):
    """Double line-to-ground (B-C-G). Returns (Ib, Ic, I_ground)."""
    z2g = (z2 * (z0 + 3 * zf)) / (z2 + z0 + 3 * zf)
    i1 = v / (z1 + z2g)
    i2 = -i1 * (z0 + 3 * zf) / (z2 + z0 + 3 * zf)
    i0 = -i1 * z2 / (z2 + z0 + 3 * zf)
    _, ib, ic = abc_from_sequence(i0, i1, i2)
    return ib, ic, 3 * i0


def base_current(mva: float, kv: float) -> float:
    """Base current (kA) for three-phase MVA and line kV."""
    return mva / (3 ** 0.5 * kv)


def pu_to_ohm(z_pu: complex, mva: float, kv: float) -> complex:
    return z_pu * kv ** 2 / mva


def ct_saturation_voltage(i_fault_a: float, ct_ratio: float, r_ct: float, r_burden: float,
                          xr: float = 0.0) -> float:
    """Required knee-point voltage (V) ~ If_sec * (1 + X/R) * (Rct + Rb)."""
    return (i_fault_a / ct_ratio) * (1 + xr) * (r_ct + r_burden)
