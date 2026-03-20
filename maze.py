class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }

def get_neighbors(cell, grid):
    neighbors = {}
    width = len(grid[0])
    height = len(grid)

    x, y = cell.x, cell.y

    if y > 0:
        neighbors["N"] = grid[y - 1][x]
    if x < width - 1:
        neighbors["E"] = grid[y][x + 1]
    if y < height - 1:
        neighbors["S"] = grid[y + 1][x]
    if x > 0:
        neighbors["W"] = grid[y][x - 1]
    return neighbors


def unvisited_neighbors(cell, grid):
    neighbors = get_neighbors(cell, grid)

    unvisited_neighbors = {}
    for direction in neighbors:
        neighbor = neighbors[direction]
        if not neighbor.visited:
            unvisited_neighbors[direction] = neighbor
    return unvisited_neighbors

def creat_grid(width, height):
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x, y))
        grid.append(row)

    return grid
OPPOSITE = {
        "W": "E",
        "E": "W",
        "S": "N",
        "N": "S"
}

def remove_wall(cell, neighbor, direction):
    cell.walls[direction] = False
    neighbor.walls[OPPOSITE[direction]] = False


grid = creat_grid(3, 3)
for row in grid:
    print([f"({c.x}, {c.y})" for c in row])

cell = grid[0][0]
neighbor = grid[0][1]

unvisited_neighbors = unvisited_neighbors(cell, grid)

for dir, nei in unvisited_neighbors.items():
    print(f"{dir}: ({nei.x}, {nei.y})")














