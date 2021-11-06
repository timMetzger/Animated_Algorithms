from random import choice
BLACK = (0, 0, 0)

def a_star(graph, start, end, positions):
    # f = g + n
    # g is the actual cost of traversal from start node to current node
    # h is the actual cost from the current node to goal node i.e as the crow flies or other methods

    # This implementation of A* is not ideal since diagonal movement does not exist so it often does not give the
    # optimal path as the heuristic value is too influential

    start_pos = positions[start]
    end_pos = positions[end]

    gScore = [float('inf') for _ in graph.keys()]
    gScore[start] = 0
    parents = {}
    fScore = {node: float('inf') for node in graph.keys()}
    fScore[start] = manhattan_distance(start_pos, end_pos)
    next_node = start

    open_set = {start}

    while open_set:

        # Selecting the node with the lowest fScore
        current = min(fScore, key=fScore.get)

        if current == end:
            return path_as_list(start, end, parents)
        yield current

        open_set.remove(current)

        for neighbor in graph[current].keys():

            temp_gscore = gScore[current] + graph[current][neighbor]
            if temp_gscore < gScore[neighbor]:
                parents[neighbor] = current
                gScore[neighbor] = temp_gscore

                neighbor_pos = positions[neighbor]
                fScore[neighbor] = gScore[neighbor] + manhattan_distance(neighbor_pos, end_pos)

                if neighbor not in open_set:
                    open_set.add(neighbor)


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


def dijkstra(graph, start, end):
    # Without weights this is essentially a complicated BFS

    size = len(graph)

    # Traversal Distance
    dist = [float('inf') for _ in range(size)]
    dist[start] = 0

    # Shortest Path Tree
    sptSet = [False for _ in range(size)]

    # List to read back path
    parents = {}

    for _ in range(size):

        current = minimum_distance(size, dist, sptSet)

        if current == end:
            break
        yield current

        sptSet[current] = True

        for neighbor in graph[current].keys():
            if graph[current][neighbor] > 0 and sptSet[neighbor] is False and dist[neighbor] > dist[current] + \
                    graph[current][neighbor]:
                dist[neighbor] = dist[current] + graph[current][neighbor]
                parents[neighbor] = current

    return path_as_list(start, end, parents)

def depth_first_maze(boxs):

    rows = len(boxs)
    cols = len(boxs[0])
    stack = []
    stack.append(boxs[1][1])
    visited = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(False)
        visited.append(row)


    while stack:
        current = stack.pop()
        i,j = get_indices(boxs,current)
        print(i,j)

        neighbors = []

        # Left neighbor
        if i - 1 >= 0:
            neighbors.append(boxs[i-1][j])
            visited[i-1][j] = True

        # Right neighbor
        if i + 1 <= rows:
            neighbors.append(boxs[i+1][j])
            visited[i + 1][j] = True

        # Top neighbor
        if j + 1 <= cols:
            neighbors.append(boxs[i][j+1])
            visited[i][j + 1] = True

        if j - 1 >= 0:
            neighbors.append(boxs[i][j-1])
            visited[i][j - 1] = True



        chosen_one = choice(neighbors)
        chosen_one.color = BLACK
        i,j = get_indices(boxs, chosen_one)
        visited[i][j] = True
        stack.append(chosen_one)

        yield boxs
    return "Jobs Done!"





def get_indices(boxs, current):
    rows = len(boxs)
    cols = len(boxs[0])
    for i in range(rows):
        for j in range(cols):
            if boxs[i][j] is current:
                return i,j


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


def minimum_distance(size, dist, sptSet):
    min = float('inf')
    min_index = 0
    for u in range(size):
        if dist[u] < min and sptSet[u] is False:
            min = dist[u]
            min_index = u

    return min_index


def manhattan_distance(current, destination):
    return abs(current[0] - destination[0]) + abs(current[1] - destination[1])
