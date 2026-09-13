def days(rrule):
    return rrule.split("=")[-1].split(",")
