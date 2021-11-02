def a_star(graph, start, end, positions, weights=False):
    # f = g + n
    # g is the actual cost of traversal from start node to current node
    # h is the actual cost from the current node to goal node i.e as the crow flies or other methods
    if not weights:
        graph = add_weights(graph)



    start_pos = positions[start]
    end_pos = positions[end]

    gScore = [float('inf') for _ in graph.keys()]
    gScore[start] = 0
    parents = {}
    fScore = {node: float('inf') for node in graph.keys()}
    fScore[start] = manhattan_distance(start_pos,end_pos)
    next_node = start

    open_set = {start}
    
    while open_set:
        # Next node is minimum f-score node in open_set
        min_node = 0
        min = fScore[0]
        for node in open_set:
            if fScore[node] < min:
                min_node = node
                min = fScore[node]

        next_node = min_node


        if next_node == end:
            return path_as_list(start, end, parents)

        open_set.remove(next_node)

        for neighbor in graph[next_node]:
            # Marking visited nodes by removing them and then choosing the shortest distance node
            temp_g_score = graph[next_node][neighbor] + gScore[next_node]
            if temp_g_score < gScore[neighbor]:

                parents[neighbor] = next_node
                gScore[neighbor] = temp_g_score
                
                neighbor_pos = positions[neighbor]
                fScore[neighbor] = gScore[neighbor] + manhattan_distance(neighbor_pos, end_pos)
                if neighbor not in open_set:
                    open_set.add(neighbor)

        yield next_node



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


def dijkstra(graph, start, end, weights=False):
    # Without weights this is essentially a complicated BFS
    if not weights:
        graph = add_weights(graph)

    costs = {node: float('inf') for node in graph.keys()}
    costs[start] = 0
    parents = {}
    next_node = start

    while next_node != end:
        for neighbor in graph[next_node]:
            # Marking visited nodes by removing them and then choosing the shortest distance node
            if graph[next_node][neighbor] + costs[next_node] < costs[neighbor]:
                costs[neighbor] = graph[next_node][neighbor] + costs[next_node]
                parents[neighbor] = next_node
            del graph[neighbor][next_node]
        del costs[next_node]
        yield next_node
        next_node = min(costs, key=costs.get)

    return path_as_list(start, end, parents)


def path_as_list(start, end, data):
    """Returns a path from start to end as a list of nodes"""
    node = end
    backpath = [end]
    path = []
    while node != start:
        backpath.append(data[node])
        node = data[node]

    for i in range(len(backpath)):
        path.append(backpath[-i - 1])
    return path


def add_weights(graph):
    # If weights not given then each has traversal costs 1 point
    # Changing graph to form {node:{adj_node:value,adj_node:value,adj_node:value}}
    for node, adj_nodes in graph.items():
        graph[node] = {adj_node_key: 1 for adj_node_key in adj_nodes}

    return graph


def manhattan_distance(current, destination):
    return abs(current[0] - destination[0]) + abs(current[1] - destination[1])


def min_distance():
    pass
