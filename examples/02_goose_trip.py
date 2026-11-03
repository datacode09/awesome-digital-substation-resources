"""Simulate a protection trip as GOOSE: data change, burst, back-off to heartbeat."""
from dsub.goose import GoosePdu, next_state, retransmission_schedule, subscriber_check

pdu = GoosePdu("PROT1/LD0$gcb1", 2000, "PROT1/LD0$gooseDs", "gcb1", 1, 0, 1, [False, True])
print("idle      ", pdu.encode().hex())
pdu = next_state(pdu, [True, False])           # PTRC.Tr=TRUE, XCBR.Pos=open
print("trip      ", pdu.encode().hex())
t = 0.0
prev = None
for i, dt in enumerate(retransmission_schedule(2, 1000, 8)):
    t += dt
    pdu.sq_num = i
    print(f"t={t:7.0f} ms  stNum={pdu.st_num} sqNum={pdu.sq_num}  ->", subscriber_check(prev, pdu))
    prev = GoosePdu.decode(pdu.encode())
