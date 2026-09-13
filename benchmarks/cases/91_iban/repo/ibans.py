def valid(iban):
    compact = iban.replace(" ", "")
    return compact.startswith("GB") and len(compact) == 22
