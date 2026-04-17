import heapq
from math import sqrt
from typing import Dict, List, Optional, Tuple


Grid = List[List[float]]
Point = Tuple[int, int]


class GraphUtils:
    @staticmethod
    def in_bounds(grid: Grid, node: Point) -> bool:
        r, c = node
        return 0 <= r < len(grid) and 0 <= c < len(grid[0])

    @staticmethod
    def is_blocked(grid: Grid, node: Point) -> bool:
        r, c = node
        return grid[r][c] == float("inf")

    @staticmethod
    def get_neighbors(grid: Grid, node: Point, diagonal: bool = False) -> List[Point]:
        r, c = node

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

        if diagonal:
            directions.extend([
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ])

        neighbors: List[Point] = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if GraphUtils.in_bounds(grid, (nr, nc)) and not GraphUtils.is_blocked(grid, (nr, nc)):
                neighbors.append((nr, nc))

        return neighbors

    @staticmethod
    def movement_cost(current: Point, neighbor: Point) -> float:
        dr = abs(current[0] - neighbor[0])
        dc = abs(current[1] - neighbor[1])
        if dr == 1 and dc == 1:
            return sqrt(2)
        return 1.0

    @staticmethod
    def heuristic(a: Point, b: Point) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def reconstruct_path(
        came_from: Dict[Point, Point],
        cost_so_far: Dict[Point, float],
        start: Point,
        goal: Point,
    ) -> List[dict]:
        if goal not in cost_so_far:
            return []

        path_nodes: List[Point] = []
        current = goal
        while current != start:
            path_nodes.append(current)
            current = came_from[current]
        path_nodes.append(start)
        path_nodes.reverse()

        return [
            {
                "row": r,
                "col": c,
                "cumulative_cost": round(cost_so_far[(r, c)], 3),
            }
            for r, c in path_nodes
        ]

    @staticmethod
    def astar(grid: Grid, start: Point, goal: Point, diagonal: bool = False) -> Tuple[List[dict], float]:
        frontier: List[Tuple[float, Point]] = []
        heapq.heappush(frontier, (0.0, start))

        came_from: Dict[Point, Point] = {}
        cost_so_far: Dict[Point, float] = {start: grid[start[0]][start[1]]}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for neighbor in GraphUtils.get_neighbors(grid, current, diagonal):
                step_cost = GraphUtils.movement_cost(current, neighbor)
                new_cost = cost_so_far[current] + step_cost + grid[neighbor[0]][neighbor[1]]

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + GraphUtils.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        path = GraphUtils.reconstruct_path(came_from, cost_so_far, start, goal)
        total_cost = round(cost_so_far[goal], 3) if goal in cost_so_far else float("inf")
        return path, total_cost

    @staticmethod
    def dijkstra(grid: Grid, start: Point, goal: Point, diagonal: bool = False) -> Tuple[List[dict], float]:
        frontier: List[Tuple[float, Point]] = []
        heapq.heappush(frontier, (0.0, start))

        came_from: Dict[Point, Point] = {}
        cost_so_far: Dict[Point, float] = {start: grid[start[0]][start[1]]}

        while frontier:
            current_cost, current = heapq.heappop(frontier)

            if current == goal:
                break

            if current_cost > cost_so_far.get(current, float("inf")):
                continue

            for neighbor in GraphUtils.get_neighbors(grid, current, diagonal):
                step_cost = GraphUtils.movement_cost(current, neighbor)
                new_cost = cost_so_far[current] + step_cost + grid[neighbor[0]][neighbor[1]]

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    came_from[neighbor] = current

        path = GraphUtils.reconstruct_path(came_from, cost_so_far, start, goal)
        total_cost = round(cost_so_far[goal], 3) if goal in cost_so_far else float("inf")
        return path, total_cost