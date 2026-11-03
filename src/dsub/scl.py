"""Lesson 4 - SCL (IEC 61850-6): the XML engineering language (ICD/IID/CID/SCD).

Parses the IED -> LDevice -> LN hierarchy plus GOOSE/SV communication settings.
IEC 61850 object reference:  <IED><LD>/<prefix><LNclass><inst>.<DO>.<DA>
"""
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

NS = {"s": "http://www.iec.ch/61850/2003/SCL"}

LN_CLASS_HELP = {
    "LLN0": "Logical node zero: device-level info, datasets, control blocks",
    "LPHD": "Physical device information",
    "PTOC": "Time overcurrent protection (ANSI 50/51)",
    "PDIF": "Differential protection (ANSI 87)",
    "PDIS": "Distance protection (ANSI 21)",
    "PTRC": "Protection trip conditioning",
    "RREC": "Autoreclosing (ANSI 79)",
    "XCBR": "Circuit breaker",
    "XSWI": "Switch / disconnector",
    "CSWI": "Switch controller",
    "CILO": "Interlocking",
    "MMXU": "Measurements (RMS, power, ...)",
    "TCTR": "Current transformer (process bus)",
    "TVTR": "Voltage transformer (process bus)",
}


@dataclass
class LogicalNode:
    ln_class: str
    inst: str
    prefix: str = ""

    @property
    def name(self) -> str:
        return f"{self.prefix}{self.ln_class}{self.inst}"

    @property
    def description(self) -> str:
        return LN_CLASS_HELP.get(self.ln_class, "see IEC 61850-7-4")


@dataclass
class ControlBlock:
    kind: str            # GSE or SMV
    name: str
    ld: str
    mac: str = ""
    appid: str = ""
    vlan_priority: str = ""
    dataset: str = ""


@dataclass
class Ied:
    name: str
    lns: dict[str, list[LogicalNode]] = field(default_factory=dict)  # per LDevice
    control_blocks: list[ControlBlock] = field(default_factory=list)


def _p(addr, kind: str) -> str:
    if addr is None:
        return ""
    for p in addr.findall("s:P", NS):
        if p.get("type") == kind:
            return p.text or ""
    return ""


def parse_scl(path: str) -> dict[str, Ied]:
    root = ET.parse(path).getroot()
    ieds: dict[str, Ied] = {}
    for ied_el in root.findall("s:IED", NS):
        ied = Ied(ied_el.get("name"))
        for ld in ied_el.iterfind(".//s:LDevice", NS):
            nodes = []
            for ln in list(ld.findall("s:LN0", NS)) + list(ld.findall("s:LN", NS)):
                nodes.append(LogicalNode(ln.get("lnClass"), ln.get("inst", ""), ln.get("prefix", "")))
                for gc in ln.findall("s:GSEControl", NS):
                    ied.control_blocks.append(ControlBlock("GSE", gc.get("name"), ld.get("inst"), dataset=gc.get("datSet")))
                for sc in ln.findall("s:SampledValueControl", NS):
                    ied.control_blocks.append(ControlBlock("SMV", sc.get("name"), ld.get("inst"), dataset=sc.get("datSet")))
            ied.lns[ld.get("inst")] = nodes
        ieds[ied.name] = ied
    # merge Communication addressing into control blocks
    for cap in root.iterfind(".//s:ConnectedAP", NS):
        ied = ieds.get(cap.get("iedName"))
        if not ied:
            continue
        for el, kind in (("GSE", "GSE"), ("SMV", "SMV")):
            for node in cap.findall(f"s:{el}", NS):
                for cb in ied.control_blocks:
                    if cb.kind == kind and cb.name == node.get("cbName") and cb.ld == node.get("ldInst"):
                        addr = node.find("s:Address", NS)
                        cb.mac, cb.appid = _p(addr, "MAC-Address"), _p(addr, "APPID")
                        cb.vlan_priority = _p(addr, "VLAN-PRIORITY")
    return ieds


def summarize(ieds: dict[str, Ied]) -> str:
    lines = []
    for ied in ieds.values():
        lines.append(f"IED {ied.name}")
        for ld, lns in ied.lns.items():
            lines.append(f"  LD {ld}")
            for ln in lns:
                lines.append(f"    {ln.name:<8} {ln.description}")
        for cb in ied.control_blocks:
            lines.append(f"  {cb.kind} {cb.name} dataset={cb.dataset} mac={cb.mac} appid={cb.appid}")
    return "\n".join(lines)
