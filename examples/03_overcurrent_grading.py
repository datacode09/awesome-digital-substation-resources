"""Grade two IEC standard-inverse relays and print the trip-time table."""
from dsub.protection import iec_trip_time, grading_margin

print(f"{'I/Is':>6} {'downstream':>11} {'upstream':>9} {'margin':>7}")
for m in (3, 5, 8, 12, 20):
    d = iec_trip_time(m, 0.10)
    u = iec_trip_time(m / 2, 0.30)  # upstream sees the same current but has a higher pickup
    print(f"{m:>6} {d:>10.3f}s {u:>8.3f}s {grading_margin(u, d):>6.3f}s")
