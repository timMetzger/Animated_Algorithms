from pathfinding_algorithms import minimum_distance

def boruvkas(graph):
    pass

def prims(graph):
    size = len(graph)

    keys = graph.keys()
    dist = {key: float('inf') for key in keys}
    dist[0] = 0
    mstSet = {key: False for key in keys}
    parents = {}

    previous = 0
    for _ in range(size):
        current = minimum_distance(dist,mstSet)
        yield previous, current

        mstSet[current] = True

        for neighbor in graph[current].keys():
            if graph[current][neighbor] > 0 and mstSet[neighbor] == False and dist[neighbor] > graph[current][neighbor]:
                dist[neighbor] = graph[current][neighbor]
                parents[neighbor] = current
        previous = current

    return parents

def kruskals():
    pass

def reverse_delete():
    pass

