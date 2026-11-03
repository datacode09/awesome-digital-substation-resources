"""Print the IED/LN/GOOSE/SV structure of data/sample.scd."""
from pathlib import Path
from dsub.scl import parse_scl, summarize

print(summarize(parse_scl(str(Path(__file__).parent.parent / "data" / "sample.scd"))))
