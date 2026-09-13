def parse_row(line):
    name, city = line.strip().split(",")
    return {"name": name.strip('"'), "city": city.strip('"')}
