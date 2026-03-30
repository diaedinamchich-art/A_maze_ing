from maze import MazeGenerator

def test_run():
    width, height = 20, 15
    entry = (0, 0)
    exit_ = (19, 14)
    output = "maze_test.txt"

    gen = MazeGenerator(width, height, entry, exit_, True, output, seed=42)
    print("Generating maze...")
    grid = gen.generate_maze()

    print(f"Saving to {output}...")
    gen.save_maze(grid)

    try:
        with open(output, 'r') as f:
            content = f.read().splitlines()
        print("\n successful")
        print("-" * 30)
        print(f"Maze size: {width}*{height}")
        for line in content[:3]:
            print(f"   {line}")
        print("   ...")
        for line in content[-3:]:
            print(f"   {line}")
        print("-" * 30)
    except FileNotFoundError:
        print("\n Error: the output file")

if __name__ == "__main__":
    test_run()
