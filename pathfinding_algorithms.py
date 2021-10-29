def a_star(arr, start, end):
    pass


def breadth_first(graph, start, end):
    queue = [[start]]
    visited = set()

    while queue:
        path = queue.pop(0)
        vertex = path[-1]

        if vertex == end:
            return path
        elif vertex not in visited:
            for current in graph.get(vertex, []):
                new_path = list(path)
                new_path.append(current)
                queue.append(new_path)

            visited.add(vertex)
            yield vertex


def depth_first(graph, start, end):
    stack = [(start, [start])]
    visited = set()

    while stack:
        (vertex, path) = stack.pop()
        if vertex not in visited:
            if vertex == end:
                return path
            visited.add(vertex)
            yield vertex
            for neighbor in graph[vertex]:
                stack.append((neighbor, path + [neighbor]))


def dijkstra(graph, start, end, weighted=None):
    size = len(graph)


def min_distance(dist, sptSet):
    pass
