import random
from collections import deque
from typing import List, Tuple, Dict, Optional, Set


class Cell:
    """Represents a single cell in the maze with its walls."""
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.visited: bool = False
        self.walls: Dict[str, bool] = {
                "N": True,
                "E": True,
                "S": True,
                "W": True
        }

class MazeGenerator:
    """Main class for maze generation, solving, and file output."""
    def __init__(self, width: int,
                 height: int,
                 entry: Tuple[int, int],
                 exit_: Tuple[int, int],
                 perfect: bool,
                 output_file: str,
                 seed = None) -> None:
        self.width = width
        self.height = height
        self.exit_ = exit_
        self.entry = entry
        self.perfect = perfect
        self.output_file = output_file
        self.seed = seed

        if seed is not None:
            random.seed(seed)
        self.opposite: Dict[str, str] = {
                "N": "S",
                "E": "W",
                "S": "N",
                "W": "E"
        }
        self.wall_bits: Dict[str, int] = {
                "N": 1,
                "E": 2,
                "S": 4,
                "W": 8
        }
        self.directions: Dict[str, Tuple[int, int]] = {
                "N": (0, -1),
                "E": (1, 0),
                "S": (0, 1),
                "W": (-1, 0)
        }

    def creat_grid(self) -> List[List[Cell]]:
        """Creates a grid of closed cells."""
        return [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]

    def get_neighbors(self, cell: Cell, grid: List[List[Cell]]) -> Dict[str, Cell]:
        neighbors = {}
        x, y = cell.x, cell.y
        for dir_name, (dx, dy) in self.directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors[dir_name] = grid[ny][nx]
        return neighbors


    def remove_wall(self, cell: Cell, neighbor: Cell, direction: str) -> None:
        cell.walls[direction] = False
        neighbor.walls[self.opposite[direction]] = False

    
    def generate_maze(self) -> List[List[Cell]]:
        """Generate the maze structure"""
        grid = self.creat_grid()
        self.place_42_pattern(grid)
        stack: List[Cell] = [grid[self.entry[1]][self.entry[0]]]
        grid[self.entry[1]][self.entry[0]].visited = True

        while stack:
            current = stack[-1]
            neighbors = self.get_neighbors(current, grid)
            unvisited = [d for d, n in neighbors.items() if not n.visited]

            if unvisited:
                direction = random.choice(unvisited)
                neighbor = neighbors[direction]
                self.remove_wall(current, neighbor, direction)
                neighbor.visited = True
                stack.append(neighbor)
            else:
                stack.pop()

        if not self.perfect:
            self.break_random_walls(grid)
        return grid


    def place_42_pattern(self, grid: List[List[Cell]]) -> None:
        """Marks cells for '42' as visited to keep them closed."""
        if self.width < 11 or self.height < 9:
            print("Error: Maze size too small for pattern 42.")
            return

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        points = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                  (4, 0), (5, 0), (6, 0), (6, 1), (4, 2), (5, 2), (6, 2), (4, 3), (4, 4), (5, 4), (6, 4)]
        for dx, dy in points:
            grid[start_y + dy][start_x + dx].visited = True

    def get_shortest_path(self, grid: List[List[Cell]]) -> List[str]:
        """BFS to find the shortest path."""
        queue = deque([(self.entry, [])])
        visited: Set[Tuple[int, int]] = {self.entry}

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == self.exit_:
                return path

            for direction, (dx, dy) in self.directions.items():
                if not grid[y][x].walls[direction]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [direction]))
        return []

    def save_maze(self, grid: List[List[Cell]]) -> None:
        """Saves according to the hexadecimal wall format."""
        path = self.get_shortest_path(grid)
        with open(self.output_file, "w") as f:
            for row in grid:
                line = "".join(format(sum(self.wall_bits[d] for d, w in c.walls.items() if w), "X") for c in row)
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit_[0]},{self.exit_[1]}\n")
            f.write("".join(path) + "\n")

    def break_random_walls(self, grid: List[List[Cell]], pro: float = 0.1) -> None:
        """Add cycles for non-perfect mazes."""
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if random.random() < pro:
                    d = random.choice(["E", "S"])
                    nx, ny = x + self.directions[d][0], y + self.directions[d][1]
                    self.remove_wall(grid[y][x], grid[ny][nx], d)

