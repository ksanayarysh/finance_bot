from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP

TWO_PLACES = Decimal("0.01")

def q2(x: Decimal) -> Decimal:
    return x.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
