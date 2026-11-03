# Learning path

Work in order; each step has a module in `src/dsub/`, an example in `examples/`, and tests in `tests/test_dsub.py` that you can read as worked answers.

| # | Topic | Read | Run | Key idea |
|---|-------|------|-----|----------|
| 0 | Big picture | README resources | - | Station bus, process bus, merging units, IEDs, time sync |
| 1 | Phasors, DFT, sequence components | `phasors.py` | - | Relays turn samples into phasors, then into sequence quantities |
| 2 | Sampled Values (9-2LE) | `sampled_values.py` | `05_sampled_values.py` | 80 samples/cycle, smpCnt, scaling, loss detection |
| 3 | GOOSE | `goose.py` | `02_goose_trip.py` | stNum/sqNum, retransmission back-off, BER |
| 4 | SCL / data model | `scl.py`, `data/sample.scd` | `01_parse_scd.py` | IED > LD > LN > DO > DA; ICD/CID/SCD workflow |
| 5 | Protection | `protection.py` | `03_overcurrent_grading.py` | 50/51 grading, 87 slopes, 21 mho |
| 6 | Faults and CT sizing | `faults.py` | `04_fault_levels.py` | 3ph/SLG/LL/DLG, why z0 matters |
| 7 | Time, redundancy, latency | `timing.py` | - | PTP offset, PRP, 3 ms trip budget |

## Exercises
1. Extend `GoosePdu` to carry a structured dataset (INT32, bit-string quality, UTC time) and decode a real capture from Wireshark.
2. Add a `PTOC` setting group to `sample.scd` and write a validator that checks every GSE subscriber's `confRev` matches the publisher.
3. Replace the full-cycle DFT with a half-cycle or cosine filter; measure response to a decaying DC offset.
4. Implement CT saturation by driving a magnetising-curve model with an offset fault and see how 87 behaves.
5. Simulate PRP with two lossy LANs and measure the effective frame-loss rate.
6. Build a 21 zone-1/2/3 scheme with carrier-aided tripping (POTT) over GOOSE.

## Core standards map
- IEC 61850-5 requirements (message performance classes) / -6 SCL / -7-x data model / -8-1 MMS+GOOSE / -9-2 SV / -9-3 PTP power profile
- IEC 62439-3 PRP & HSR, IEC 60255-151 protection curves, IEEE C37.118 synchrophasors, IEEE C37.238 PTP profile
