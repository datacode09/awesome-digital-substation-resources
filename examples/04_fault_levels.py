"""Fault currents at a 33 kV bus: 3-phase, SLG, LL, DLG with a 1 ohm earth-return fault."""
from dsub import faults
from dsub.phasors import to_polar

kv, mva = 33.0, 100.0
v = 1.0
z1 = z2 = 0.08j
z0 = 0.2j
ib = faults.base_current(mva, kv)
print(f"Base current {ib * 1000:.0f} A")
i3 = faults.three_phase_fault(v, z1)
ia, _ = faults.slg_fault(v, z1, z2, z0)
b, c = faults.ll_fault(v, z1, z2)
b2, c2, ig = faults.dlg_fault(v, z1, z2, z0)
for name, i in (("3-phase", i3), ("SLG", ia), ("LL", b), ("DLG phase", b2), ("DLG ground", ig)):
    mag, ang = to_polar(i)
    print(f"{name:<11} {mag * ib:7.2f} kA  @ {ang:7.1f} deg")
