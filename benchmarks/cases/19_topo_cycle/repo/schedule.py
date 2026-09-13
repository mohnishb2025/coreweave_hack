def order(graph):
    remaining = {node: set(deps) for node, deps in graph.items()}
    done = []
    while remaining:
        ready = [node for node, deps in remaining.items() if not deps]
        if not ready:
            break
        node = sorted(ready)[0]
        done.append(node)
        del remaining[node]
        for deps in remaining.values():
            deps.discard(node)
    return done
