def bin_index(edges, value):
    for index in range(len(edges) - 1):
        if edges[index] <= value < edges[index + 1]:
            return index
    raise ValueError("out of range")
