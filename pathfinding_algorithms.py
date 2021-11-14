from random import choice, choices

BLACK = (0, 0, 0)
AQUATIC_GREEN = (0, 255, 145)


def a_star(graph, start, end, positions):
    # f = g + n
    # g is the actual cost of traversal from start node to current node
    # h is the actual cost from the current node to goal node i.e as the crow flies or other methods

    # This implementation of A* is not ideal since diagonal movement does not exist so it often does not give the
    # optimal path as the heuristic value is too influential
    start_pos = positions[start]
    end_pos = positions[end]

    gScore = {key: float('inf') for key in graph.keys()}

    gScore[start] = 0
    parents = {}
    fScore = {node: float('inf') for node in graph.keys()}
    fScore[start] = manhattan_distance(start_pos, end_pos)
    next_node = start

    open_set = {start}

    while open_set:

        # Selecting the node in open_set with lowest fScore
        min_fScores = {key: value for key, value in sorted(fScore.items(), key=lambda item: item[1])}
        for key, value in min_fScores.items():
            if key in open_set:
                current = key
                break

        open_set.remove(current)

        if current == end:
            return path_as_list(start, end, parents)
        yield current

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

    keys = graph.keys()
    # Traversal Distance
    dist = {key: float('inf') for key in keys}
    dist[start] = 0

    # Shortest Path Tree
    sptSet = {key: False for key in keys}

    # List to read back path
    parents = {}

    for _ in range(size):

        current = minimum_distance(dist, sptSet)

        if current == end:
            return path_as_list(start, end, parents)
        yield current

        sptSet[current] = True

        for neighbor in graph[current].keys():
            if graph[current][neighbor] > 0 and sptSet[neighbor] is False and dist[neighbor] > dist[current] + \
                    graph[current][neighbor]:
                dist[neighbor] = dist[current] + graph[current][neighbor]
                parents[neighbor] = current


def depth_first_maze(boxs):
    rows = len(boxs)
    cols = len(boxs[0])
    stack = []
    stack.append(boxs[1][1])
    visited = []

    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(False)
        visited.append(row)

    visited[1][1] = True

    while stack:
        current = stack.pop()
        i, j = get_indices(boxs, current)

        neighbors = []
        flag = False

        # Top
        if i - 1 >= 0:
            if not visited[i - 1][j]:
                neighbors.append(boxs[i - 1][j])
                flag = True

        # Bottom
        if i + 1 <= rows - 1:
            if not visited[i + 1][j]:
                neighbors.append(boxs[i + 1][j])
                flag = True

        # Right
        if j + 1 <= cols - 1:
            if not visited[i][j + 1]:
                neighbors.append(boxs[i][j + 1])
                flag = True

        # Left
        if j - 1 >= 0:
            if not visited[i][j - 1]:
                neighbors.append(boxs[i][j - 1])
                flag = True

        # Top left
        if i - 1 >= 0 and j - 1 >= 0:
            if not visited[i - 1][j - 1]:
                neighbors.append(boxs[i - 1][j - 1])
                flag = True

        # Top right
        if i - 1 >= 0 and j + 1 <= cols - 1:
            if not visited[i - 1][j + 1]:
                neighbors.append(boxs[i - 1][j + 1])
                flag = True

        # Bottom left
        if i + 1 <= rows - 1 and j - 1 >= 0:
            if not visited[i + 1][j - 1]:
                neighbors.append(boxs[i + 1][j - 1])
                flag = True

        # Bottom right
        if i + 1 <= rows - 1 and j + 1 <= cols - 1:
            if not visited[i + 1][j + 1]:
                neighbors.append(boxs[i + 1][j + 1])
                flag = True

        if flag:
            stack.append(current)
            chosen_one = choice(neighbors)
            chosen_one.color = BLACK
            stack.append(chosen_one)

            for neighbor in neighbors:
                if neighbor is not chosen_one:
                    stack.append(neighbor)
                i, j = get_indices(boxs, neighbor)
                visited[i][j] = True

            yield chosen_one

    return "Jobs Done!"


def depth_first_maze_weighted(boxs):
    rows = len(boxs)
    cols = len(boxs[0])
    stack = []
    stack.append(boxs[1][1])
    visited = []

    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(False)
        visited.append(row)

    visited[1][1] = True

    while stack:
        current = stack.pop()
        i, j = get_indices(boxs, current)

        neighbors = []
        flag = False

        # Top
        if i - 1 >= 0:
            if not visited[i - 1][j]:
                neighbors.append(boxs[i - 1][j])
                flag = True

        # Bottom
        if i + 1 <= rows - 1:
            if not visited[i + 1][j]:
                neighbors.append(boxs[i + 1][j])
                flag = True

        # Right
        if j + 1 <= cols - 1:
            if not visited[i][j + 1]:
                neighbors.append(boxs[i][j + 1])
                flag = True

        # Left
        if j - 1 >= 0:
            if not visited[i][j - 1]:
                neighbors.append(boxs[i][j - 1])
                flag = True

        # Top left
        if i - 1 >= 0 and j - 1 >= 0:
            if not visited[i - 1][j - 1]:
                neighbors.append(boxs[i - 1][j - 1])
                flag = True

        # Top right
        if i - 1 >= 0 and j + 1 <= cols - 1:
            if not visited[i - 1][j + 1]:
                neighbors.append(boxs[i - 1][j + 1])
                flag = True

        # Bottom left
        if i + 1 <= rows - 1 and j - 1 >= 0:
            if not visited[i + 1][j - 1]:
                neighbors.append(boxs[i + 1][j - 1])
                flag = True

        # Bottom right
        if i + 1 <= rows - 1 and j + 1 <= cols - 1:
            if not visited[i + 1][j + 1]:
                neighbors.append(boxs[i + 1][j + 1])
                flag = True

        if flag:
            stack.append(current)
            chosen_wall, chosen_weight = choices(neighbors, k=2)
            chosen_wall.color = BLACK
            if chosen_weight.color != BLACK:
                chosen_weight.color = AQUATIC_GREEN
            stack.append(chosen_wall)

            for neighbor in neighbors:
                if neighbor is not chosen_wall:
                    stack.append(neighbor)
                i, j = get_indices(boxs, neighbor)
                visited[i][j] = True

            yield [chosen_wall, chosen_weight]

    return "Jobs Done!"


def get_indices(boxs, current):
    rows = len(boxs)
    cols = len(boxs[0])
    for i in range(rows):
        for j in range(cols):
            if boxs[i][j] is current:
                return i, j


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


def minimum_distance(dist, sptSet):
    min_val = float('inf')
    min_node = 0
    for node, value in dist.items():
        if value < min_val and sptSet[node] is False:
            min_node = node
            min_val = value

    return min_node


def manhattan_distance(current, destination):
    return abs(current[0] - destination[0]) + abs(current[1] - destination[1])
