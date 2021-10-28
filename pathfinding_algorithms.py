def a_star(arr,start,end):
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
            for current in graph.get(vertex,[]):
                new_path = list(path)
                new_path.append(current)
                queue.append(new_path)

            visited.add(vertex)
            yield vertex

def depth_first(arr,start,end):
    pass

def dijkstra(arr,start,end):
    pass
