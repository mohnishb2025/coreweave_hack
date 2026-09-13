from decimal import Decimal, ROUND_HALF_UP

def quantize(value):
    return format(Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")
