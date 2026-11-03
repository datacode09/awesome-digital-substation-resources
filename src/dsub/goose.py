"""Lesson 3 - GOOSE (IEC 61850-8-1): fast, multicast, event-driven messaging.

Includes a minimal ASN.1 BER codec for a GOOSE PDU and the retransmission
schedule that makes GOOSE reliable without acknowledgements.
"""
from dataclasses import dataclass, field

GOOSE_ETHERTYPE = 0x88B8
SV_ETHERTYPE = 0x88BA


# ---- minimal BER ----------------------------------------------------------
def _len(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def tlv(tag: int, value: bytes) -> bytes:
    return bytes([tag]) + _len(len(value)) + value


def read_tlv(buf: bytes, off: int = 0) -> tuple[int, bytes, int]:
    tag = buf[off]; off += 1
    ln = buf[off]; off += 1
    if ln & 0x80:
        k = ln & 0x7F
        ln = int.from_bytes(buf[off:off + k], "big"); off += k
    return tag, buf[off:off + ln], off + ln


def enc_uint(v: int) -> bytes:
    return v.to_bytes(max(1, (v.bit_length() + 7) // 8), "big")


def enc_bool(v: bool) -> bytes:
    return tlv(0x83, b"\xff" if v else b"\x00")


# ---- GOOSE PDU ------------------------------------------------------------
@dataclass
class GoosePdu:
    gocb_ref: str
    time_allowed_to_live_ms: int
    dat_set: str
    go_id: str
    st_num: int
    sq_num: int
    conf_rev: int
    all_data: list[bool] = field(default_factory=list)  # booleans only in this teaching codec

    def encode(self) -> bytes:
        body = (
            tlv(0x80, self.gocb_ref.encode())
            + tlv(0x81, enc_uint(self.time_allowed_to_live_ms))
            + tlv(0x82, self.dat_set.encode())
            + tlv(0x83, self.go_id.encode())
            + tlv(0x85, enc_uint(self.st_num))
            + tlv(0x86, enc_uint(self.sq_num))
            + tlv(0x87, b"\x00")                     # simulation = false
            + tlv(0x88, enc_uint(self.conf_rev))
            + tlv(0x89, b"\x00")                     # ndsCom = false
            + tlv(0x8A, enc_uint(len(self.all_data)))
            + tlv(0xAB, b"".join(enc_bool(b) for b in self.all_data))
        )
        return tlv(0x61, body)

    @classmethod
    def decode(cls, raw: bytes) -> "GoosePdu":
        tag, body, _ = read_tlv(raw)
        assert tag == 0x61, "not a goosePdu"
        f, off = {}, 0
        while off < len(body):
            t, v, off = read_tlv(body, off)
            f[t] = v
        data, off = [], 0
        while off < len(f[0xAB]):
            _, v, off = read_tlv(f[0xAB], off)
            data.append(v != b"\x00")
        n = lambda t: int.from_bytes(f[t], "big")
        return cls(f[0x80].decode(), n(0x81), f[0x82].decode(), f[0x83].decode(),
                   n(0x85), n(0x86), n(0x88), data)


def next_state(pdu: GoosePdu, new_data: list[bool]) -> GoosePdu:
    """Publisher rule: data change -> stNum+1, sqNum reset to 0."""
    return GoosePdu(pdu.gocb_ref, pdu.time_allowed_to_live_ms, pdu.dat_set, pdu.go_id,
                    pdu.st_num + 1, 0, pdu.conf_rev, new_data)


def retransmission_schedule(t_min_ms: float = 2, t_max_ms: float = 1000, count: int = 12,
                            factor: float = 2.0) -> list[float]:
    """Intervals after a state change: fast burst, then back off to the heartbeat T0."""
    out, t = [], t_min_ms
    for _ in range(count):
        out.append(min(t, t_max_ms))
        t *= factor
    return out


def subscriber_check(prev: GoosePdu | None, cur: GoosePdu) -> str:
    """Classify a received frame the way a subscribing IED does."""
    if prev is None:
        return "new publisher"
    if cur.conf_rev != prev.conf_rev:
        return "config revision mismatch - reject"
    if cur.st_num > prev.st_num:
        return "state change - act on data" + (" (stNum gap: missed events)" if cur.st_num > prev.st_num + 1 else "")
    if cur.st_num == prev.st_num and cur.sq_num == prev.sq_num + 1:
        return "retransmission - ok"
    if cur.st_num == prev.st_num and cur.sq_num > prev.sq_num + 1:
        return "sqNum gap - lost frame(s)"
    return "out-of-order/duplicate - discard"
