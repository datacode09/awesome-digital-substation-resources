import math
from pathlib import Path

import pytest

from dsub import faults, goose, phasors, protection, sampled_values as sv, scl, timing

ROOT = Path(__file__).parent.parent


def test_dft_recovers_phasor():
    spc = 80
    x = [100 * math.sin(2 * math.pi * k / spc + math.radians(30)) for k in range(spc)]
    mag, ang = phasors.to_polar(phasors.dft_phasor(x, spc))
    assert mag == pytest.approx(100 / math.sqrt(2), rel=1e-6)
    assert ang == pytest.approx(30, abs=1e-6)


def test_sequence_components_balanced_and_roundtrip():
    va, vb, vc = phasors.polar(1, 0), phasors.polar(1, -120), phasors.polar(1, 120)
    v0, v1, v2 = phasors.sequence_components(va, vb, vc)
    assert abs(v0) < 1e-12 and abs(v2) < 1e-12 and abs(v1) == pytest.approx(1)
    back = phasors.abc_from_sequence(v0, v1, v2)
    assert all(abs(a - b) < 1e-12 for a, b in zip(back, (va, vb, vc)))


def test_sv_rates_and_codec():
    assert sv.samples_per_second(50, 80) == 4000
    assert sv.sample_period_us(50, 80) == pytest.approx(250)
    stream = sv.make_stream(1000, 325, cycles=1)
    assert len(stream) == 80
    a = stream[10]
    assert sv.SvAsdu.decode(a.encode()) == a
    assert abs(sum(a.engineering_values()[:3])) < 0.01  # balanced currents sum ~0


def test_lost_samples():
    assert sv.lost_samples([0, 1, 2, 5, 6], 4000) == 2
    assert sv.lost_samples([3998, 3999, 0, 1], 4000) == 0


def test_goose_roundtrip_and_subscriber():
    p = goose.GoosePdu("PROT1/LD0$gcb1", 2000, "PROT1/LD0$gooseDs", "gcb1", 1, 0, 1, [False, True])
    assert goose.GoosePdu.decode(p.encode()) == p
    changed = goose.next_state(p, [True, True])
    assert (changed.st_num, changed.sq_num) == (2, 0)
    assert "state change" in goose.subscriber_check(p, changed)
    retx = goose.GoosePdu(**{**changed.__dict__, "sq_num": 1})
    assert goose.subscriber_check(changed, retx) == "retransmission - ok"


def test_goose_schedule_caps_at_heartbeat():
    s = goose.retransmission_schedule(2, 1000, 12)
    assert s[0] == 2 and s[-1] == 1000 and s == sorted(s)


def test_scl_parse():
    ieds = scl.parse_scl(str(ROOT / "data" / "sample.scd"))
    assert set(ieds) == {"PROT1", "MU1"}
    cb = ieds["PROT1"].control_blocks[0]
    assert cb.kind == "GSE" and cb.mac == "01-0C-CD-01-00-01" and cb.vlan_priority == "4"
    assert any(ln.name == "PTOC1" for ln in ieds["PROT1"].lns["LD0"])
    assert ieds["MU1"].control_blocks[0].appid == "4000"


def test_iec_curves():
    # NI, TMS 1, 10x pickup -> 2.97 s (textbook value)
    assert protection.iec_trip_time(10, 1.0, "NI") == pytest.approx(2.97, abs=0.01)
    assert protection.iec_trip_time(0.9, 1.0) == math.inf


def test_differential_through_fault_restrains_internal_trips():
    assert not protection.differential_87(5 + 0j, -5 + 0.1j)[0]   # through current
    assert protection.differential_87(5 + 0j, 0.5 + 0j)[0]        # internal
    assert protection.second_harmonic_block(1.0, 0.2)


def test_mho():
    reach = complex(10, 0)
    assert protection.mho_21(4 + 0j, 1 + 0j, reach)
    assert not protection.mho_21(12 + 0j, 1 + 0j, reach)


def test_faults():
    z = 0.1j
    i3 = faults.three_phase_fault(1, z)
    assert abs(i3) == pytest.approx(10)
    # with z1=z2=z0, SLG equals 3-phase
    ia, _ = faults.slg_fault(1, z, z, z)
    assert abs(ia) == pytest.approx(10)
    ib, ic = faults.ll_fault(1, z, z)
    assert abs(ib) == pytest.approx(abs(i3) * math.sqrt(3) / 2)
    ib, ic, ig = faults.dlg_fault(1, z, z, z)
    assert abs(ig) == pytest.approx(10, rel=1e-6)
    assert faults.base_current(100, 33) == pytest.approx(1.7495, abs=1e-3)


def test_timing():
    off, dly = timing.ptp_offset_delay(0.0, 1.0e-6 + 5e-7, 2.0, 2.0 + 5e-7 - 1e-6)
    assert off == pytest.approx(1e-6) and dly == pytest.approx(5e-7)
    assert timing.phase_error_deg(1e-6) == pytest.approx(0.018)
    b = timing.LatencyBudget(serialization_ms=timing.frame_serialization_us(200) / 1000)
    assert b.meets(3.0)
    seen = set()
    assert timing.prp_accept(seen, b"a", 1) and not timing.prp_accept(seen, b"a", 1)
    assert timing.availability(1e5, 24, True) > timing.availability(1e5, 24)
