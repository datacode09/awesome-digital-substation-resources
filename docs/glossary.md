# Glossary

Terms are grouped by theme. "Where" points to the module or file in this repo that demonstrates the idea.

## Architecture and equipment
| Term | Meaning | Where |
|---|---|---|
| Digital substation | Substation where signals (measurements, status, trips) travel as Ethernet messages (IEC 61850) instead of copper wires | README |
| IED | Intelligent Electronic Device: relay, bay controller, meter or merging unit with a processor and network port | `scl.py` |
| Station bus | Ethernet network between IEDs, SCADA and gateways (MMS, station-level GOOSE) | |
| Process bus | Ethernet network carrying SV and GOOSE between primary equipment interfaces and protection IEDs | `sampled_values.py` |
| MU (Merging Unit) | Digitizes CT/VT analog signals and publishes them as Sampled Values | `sampled_values.py` |
| NCIT | Non-Conventional Instrument Transformer: optical or Rogowski sensors with digital output | |
| CT / VT (PT) | Current / voltage (potential) transformer: scales primary quantities for measurement and protection | `faults.py` |
| Bay | Group of equipment serving one feeder, line or transformer | `data/sample.scd` |
| Breaker IED / Smart switchgear | Interface that executes trips and reports breaker position over GOOSE | |
| SCADA | Supervisory Control and Data Acquisition: operator-level monitoring and control | |
| RTU / Gateway | Converts IEC 61850 to the control-center protocol (IEC 60870-5-104, DNP3) | |
| HMI | Human-Machine Interface used by operators | |
| Hardwired signal | Traditional copper connection that GOOSE/SV replace | |

## IEC 61850 information model
| Term | Meaning | Where |
|---|---|---|
| IEC 61850 | International standard series for substation communication and data modelling | |
| Server / Client | Server holds data model (IED); client reads/controls it (SCADA, engineering tool) | |
| LD (Logical Device) | Container of logical nodes inside an IED | `scl.py` |
| LN (Logical Node) | Smallest functional unit, e.g. PTOC (overcurrent), XCBR (breaker) | `scl.py` |
| LLN0 / LPHD | Mandatory LNs: device-level data and physical device info | `scl.py` |
| DO (Data Object) | Named data within an LN, e.g. `Pos` (position), `Op` (operate) | |
| DA (Data Attribute) | Leaf value of a DO, e.g. `stVal`, `q`, `t` | |
| CDC (Common Data Class) | Template defining a DO's attributes, e.g. SPS, DPC, MV, ACT | |
| FC (Functional Constraint) | Tag giving the role of a DA: ST status, MX measured, CF config, CO control | |
| FCDA | Functional Constrained Data Attribute: an entry in a data set | `data/sample.scd` |
| Data set | Ordered list of FCDAs published together | `data/sample.scd` |
| Object reference | `IED LD/LN.DO.DA` path, e.g. `PROT1LD0/XCBR1.Pos.stVal` | `scl.py` |
| Quality (q) | Bits describing validity of a value (good, invalid, test, substituted) | `sampled_values.py` |
| Mode / Behaviour | `Mod` and `Beh` DOs: on, blocked, test, off. Test mode lets you inject signals safely | |
| ACSI | Abstract Communication Service Interface: the services (read, report, control) defined in part 7-2 | |
| Report Control Block (BRCB/URCB) | Buffered/unbuffered reporting of changes from an IED to a client | |
| Control model | Direct or SBO (select-before-operate), with normal or enhanced security | |

## Engineering (SCL) files
| Term | Meaning | Where |
|---|---|---|
| SCL | Substation Configuration description Language: XML for IEC 61850 | `scl.py` |
| SSD | System Specification Description: single-line diagram and required LNs | |
| ICD / IID | IED Capability Description / Instantiated IED Description: what a device offers / one configured device | |
| SCD | Substation Configuration Description: whole-system file with all IEDs and communication | `data/sample.scd` |
| CID | Configured IED Description: the part of the SCD downloaded to one IED | |
| SED | System Exchange Description: exchange between projects or utilities | |
| System configurator | Tool that merges ICDs and wires GOOSE/SV subscriptions into an SCD | |
| IED configurator | Vendor tool that creates the IED's CID/settings | |
| confRev | Configuration revision; subscriber rejects messages when it does not match | `goose.py` |
| Inputs / ExtRef | SCL elements that declare which published data an IED subscribes to | |

## Communication services
| Term | Meaning | Where |
|---|---|---|
| MMS | Manufacturing Message Specification: client-server protocol over TCP/IP for reports and control | |
| GOOSE | Generic Object Oriented Substation Event: multicast Layer-2 message for trips, interlocks and status (ethertype 0x88B8) | `goose.py` |
| SV / SMV | Sampled Values: multicast Layer-2 stream of current/voltage samples (ethertype 0x88BA) | `sampled_values.py` |
| 9-2LE | Implementation guideline for SV: 80 spc (protection) or 256 spc (power quality) | `sampled_values.py` |
| 9-2 (full) | The standard's SV mapping; flexible, 9-2LE is a profile | |
| stNum | GOOSE state number; increments on every data change | `goose.py` |
| sqNum | GOOSE sequence number; increments on each retransmission | `goose.py` |
| smpCnt | SV sample counter, used to detect lost or out-of-order samples | `sampled_values.py` |
| smpSynch | SV flag telling whether the sample clock is time-synchronized | `sampled_values.py` |
| APPID | Application identifier in GOOSE/SV frames, identifies the stream | `data/sample.scd` |
| Multicast MAC | Layer-2 group address; GOOSE uses 01-0C-CD-01-xx-xx, SV 01-0C-CD-04-xx-xx | `data/sample.scd` |
| BER / ASN.1 | Encoding rules used for GOOSE/MMS payloads | `goose.py` |
| TAL (timeAllowedToLive) | How long a subscriber should wait for the next GOOSE before declaring the publisher lost | `goose.py` |
| Heartbeat | Periodic GOOSE retransmission at the slowest interval when nothing changes | `goose.py` |
| Virtual wire | A GOOSE/SV subscription that replaces a copper connection | |
| Transfer time | Time from publisher application to subscriber application; trip class limit 3 ms | `timing.py` |

## Ethernet, redundancy and timing
| Term | Meaning | Where |
|---|---|---|
| VLAN / VLAN priority (802.1Q) | Traffic segmentation and priority tagging; GOOSE/SV commonly use priority 4 | `data/sample.scd` |
| Multicast filtering / IGMP / MMRP | Prevents multicast flooding by limiting delivery to subscribers | |
| Store-and-forward | Switch receives the whole frame before forwarding, adding serialization delay | `timing.py` |
| RSTP | Rapid Spanning Tree Protocol: ring redundancy with reconvergence time (too slow for the process bus) | |
| PRP | Parallel Redundancy Protocol (IEC 62439-3): duplicate frames on two LANs, zero recovery time | `timing.py` |
| HSR | High-availability Seamless Redundancy (IEC 62439-3): ring where frames travel both ways | |
| RedBox | Device connecting a non-redundant node to PRP/HSR | |
| PTP (IEEE 1588) | Precision Time Protocol: sub-microsecond network time distribution | `timing.py` |
| Power profile (C37.238 / IEC 61850-9-3) | PTP profile tailored to substations | `timing.py` |
| Grandmaster | Master clock source, usually GPS-disciplined | |
| GNSS / GPS | Satellite time source | |
| 1PPS | One-pulse-per-second hardwired time signal | |
| IRIG-B | Legacy time code distributed by cable | |
| Boundary / transparent clock | PTP switch types that correct for their own delay | |
| Holdover | How long a clock stays accurate after losing its reference | |

## Protection and control
| Term | Meaning | Where |
|---|---|---|
| ANSI/IEEE device numbers | 50 instantaneous overcurrent, 51 time overcurrent, 87 differential, 21 distance, 79 reclosing, 52 breaker, 86 lockout, 25 sync-check | `protection.py` |
| Pickup | Setting current/value above which a function starts timing | `protection.py` |
| TMS / TD | Time multiplier setting / time dial: scales an inverse-time curve | `protection.py` |
| Inverse-time curve | Operating time falls as current rises (IEC NI, VI, EI, LTI) | `protection.py` |
| Grading / coordination | Setting relays so only the device nearest the fault trips first | `protection.py` |
| Differential protection | Compares currents entering and leaving a zone; trips on imbalance | `protection.py` |
| Restraint | Percentage-slope bias that prevents false trips from CT error | `protection.py` |
| Inrush | Transformer energisation current, rich in 2nd harmonic | `protection.py` |
| Distance (mho) | Impedance-based line protection with zones 1/2/3 | `protection.py` |
| POTT / PUTT | Permissive overreach / underreach transfer trip: teleprotection schemes | |
| Breaker failure (BF, 50BF) | Backup that trips neighbours if a breaker does not clear a fault | |
| Busbar protection | Differential protection covering a bus; benefits greatly from process bus | |
| Interlocking | Logic blocking unsafe switching, often implemented with GOOSE | |
| Reclosing (79) | Automatic re-energisation after a transient fault | |
| Synchrocheck (25) | Verifies voltage/angle/frequency match before closing | |
| Lockout (86) | Trip latch that needs manual reset | |
| Setting group | Alternative set of protection settings selectable at run time | |
| Trip class P1/P2/P3, TT | IEC 61850-5 performance classes; TT6 trip: ≤ 3 ms | `timing.py` |

## Power-system analysis
| Term | Meaning | Where |
|---|---|---|
| Phasor | Magnitude and angle representing a sinusoid | `phasors.py` |
| DFT | Discrete Fourier Transform used to extract the 50/60 Hz phasor | `phasors.py` |
| RMS | Root-mean-square value; peak/√2 for a sine | `phasors.py` |
| Symmetrical components | Positive, negative and zero sequence decomposition (Fortescue) | `phasors.py` |
| Per-unit (pu) | Quantities normalized by base MVA and kV | `faults.py` |
| Fault types | 3-phase, SLG, LL, DLG | `faults.py` |
| X/R ratio | Reactance-to-resistance ratio; sets DC offset decay | `faults.py` |
| DC offset | Decaying component in fault current that can saturate CTs | `faults.py` |
| CT saturation | Core flux limit distorts secondary current; threatens differential security | `faults.py` |
| Knee-point voltage | Voltage above which the CT core starts to saturate | `faults.py` |
| Burden | Load (Ω or VA) on a CT secondary | `faults.py` |
| Synchrophasor / PMU | Time-stamped phasor measurement (IEEE C37.118) | |
| Aliasing / anti-alias filter | Distortion from sampling too slowly; prevented by low-pass filtering | `sampled_values.py` |

## Operations and cybersecurity
| Term | Meaning |
|---|---|
| FAT / SAT | Factory / Site Acceptance Test |
| Interoperability | Ability of different vendors' IEDs to work together via 61850 |
| Conformance test | Testing that a device implements the standard correctly (UCA International) |
| Test set / SV injector | Equipment that publishes simulated SV/GOOSE to test relays |
| IEC 62351 | Security for power-system communication: authentication, encryption, roles |
| IEC 62443 | Industrial automation cybersecurity framework |
| NERC CIP | North American cyber security standards for bulk electric system |
| Zone and conduit | Security segmentation model from IEC 62443 |
| Electronic security perimeter | Defined boundary protecting critical assets |
