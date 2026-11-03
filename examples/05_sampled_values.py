"""Generate 80 spc SV, recover a phasor with a DFT, and detect a lost sample."""
from dsub import sampled_values as sv
from dsub.phasors import dft_phasor, to_polar

stream = sv.make_stream(i_peak_a=1414.2, v_peak_v=18000, cycles=1)
ia = [a.engineering_values()[0] for a in stream]
mag, ang = to_polar(dft_phasor(ia, 80))
print(f"{len(stream)} ASDUs/cycle, {sv.sample_period_us():.0f} us apart; Ia = {mag:.1f} A RMS @ {ang:.1f} deg")
counters = [a.smp_cnt for a in stream]
del counters[40]
print("lost samples detected:", sv.lost_samples(counters, 4000))
