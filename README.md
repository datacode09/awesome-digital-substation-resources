# awesome-digital-substation-resources

Curated resources **plus runnable Python** for learning digital substation engineering: IEC 61850, process bus, protection, fault analysis and time/redundancy.

## Quick start
```bash
pip install -e '.[dev]'      # stdlib-only runtime, pytest for tests
pytest                       # 12 tests double as worked answers
python examples/01_parse_scd.py
python examples/02_goose_trip.py
python examples/03_overcurrent_grading.py
python examples/04_fault_levels.py
python examples/05_sampled_values.py
```
Follow [docs/curriculum.md](docs/curriculum.md) for the order and exercises, and keep [docs/glossary.md](docs/glossary.md) open for terminology (IEDs, LNs, GOOSE, SV, PRP, PTP, protection and fault terms).

## What's in the box
| Module | Teaches |
|---|---|
| `dsub.phasors` | DFT phasor extraction, Fortescue sequence components |
| `dsub.sampled_values` | IEC 61850-9-2LE: 80/256 spc, scaling, ASDU codec, loss detection |
| `dsub.goose` | GOOSE PDU BER codec, stNum/sqNum rules, retransmission schedule |
| `dsub.scl` | Parse SCD/ICD: IEDs, logical nodes, GOOSE/SV control blocks |
| `dsub.protection` | IEC inverse curves, grading, 87 dual-slope, inrush block, 21 mho |
| `dsub.faults` | 3ph, SLG, LL, DLG faults, base current, CT knee-point sizing |
| `dsub.timing` | PTP offset/delay, PRP, latency budget, availability |

The codecs are deliberately simplified for teaching (e.g. SV uses a fixed layout; GOOSE carries booleans only). Use the libraries below for real traffic.

## Curated external resources
**Standards (buy/read from the source):** [IEC 61850 series](https://webstore.iec.ch/) (IEC webstore) - [IEEE C37.118](https://standards.ieee.org/) - IEC 62439-3 (PRP/HSR) - IEC 60255-151.

**Open-source tools**
- [libiec61850](https://github.com/mz-automation/libiec61850) - C library: MMS, GOOSE, SV client/server
- [lib60870](https://github.com/mz-automation/lib60870) - IEC 60870-5-101/104
- [OpenSCD](https://github.com/openscd/open-scd) - browser SCL editor
- [Wireshark](https://www.wireshark.org/) - dissectors for GOOSE, SV, MMS, PTP, PRP
- [Scapy](https://github.com/secdev/scapy) - craft/parse Ethernet frames (GOOSE/SV experiments)
- [pandapower](https://github.com/e2nIEE/pandapower) - power-flow and short-circuit analysis in Python
- [PowSyBl / pypowsybl](https://github.com/powsybl/pypowsybl) - grid modelling and analysis

**How to use them with this repo:** capture GOOSE with Wireshark, decode it with `dsub.goose` and compare; build a network in pandapower and check your hand fault calculations against `dsub.faults`.

## Contributing
Add resources only if you've used them; keep links to official/primary sources. New lessons should include a module, an example and tests.
