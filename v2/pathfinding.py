from collections import deque


class PathFinding:
    def __init__(self, game):
        self.game = game
        self._map = game.map.mini_map
        self._ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self._graph = {}
        self._get_graph()

    def get_path(self, start, goal):
        self._visited = self._bfs(start, goal, self._graph)
        path = [goal]
        step = self._visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self._visited[step]
        return path[-1]

    def _bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                if (
                    next_node not in visited
                    and next_node not in self.game.object_handler.npc_positions
                ):
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def _get_next_nodes(self, x, y):
        return [
            (x + dx, y + dy)
            for dx, dy in self._ways
            if (x + dx, y + dy) not in self.game.map.world_map
        ]

    def _get_graph(self):
        for y, row in enumerate(self._map):
            for x, col in enumerate(row):
                if not col:
                    self._graph[(x, y)] = self._graph.get(
                        (x, y), []
                    ) + self._get_next_nodes(x, y)
