def a_star(arr, start, end)

    # Heuristic function
    def manhattan_distance():
        return abs(current_x - end_x) + abs(current_y - end_y)


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

    dist = [float('inf') for _ in range(len(graph)-1)]
    path = {}
    dist[start] = 0

    current = start

    while current != end:
        if weighted is None:
            weight = 1
            # graph[current] -> a list of adjacent node
            for neighbor in graph[current]:
                if weight + dist[current] < dist[current]:
                    dist[current] = weight + dist[current]
                    path[neighbor] = current
                    hold = neighbor
                index = graph[neighbor].index(current)
                del graph[neighbor][index]
            del dist[current]
            print(neighbor)
            current = neighbor
        else:
            return "Not yet implemented"

    print(path)






def min_distance():
    pass
