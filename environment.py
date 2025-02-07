import utils


class Environment:

    def __init__(self, map_path):
        self.file_path = map_path
        self.world = self.load_assets(self.load_map())

    def load_map(self):
        try:
            with open(self.file_path) as f:
                world_map = [[col.lower() for col in line.strip()] for line in f]

                first_row = len(world_map[0])
                for row in world_map:
                    if len(row) != first_row:
                        raise Exception("Map rows are not even")
                return world_map
        except FileNotFoundError:
            print(f"File not found")
        except PermissionError:
            print(f"File read permissions were denied")
        except IOError as er:
            print(f"IO error: {er}")

        return []

    @staticmethod
    def load_assets(world_map: list):
        for i in range(len(world_map)):
            for j in range(len(world_map[i])):
                if (world_map[i][j] == '^' or world_map[i][j] == 'v'
                        or world_map[i][j] == '<' or world_map[i][j] == '>'):
                    world_map[i][j] = utils.Robot((j, i), world_map[i][j])
                    print("robot location", world_map[i][j], (j, i))
                elif (world_map[i][j] == 'u' or world_map[i][j] == 'd'
                        or world_map[i][j] == 'l' or world_map[i][j] == 'r'):
                    world_map[i][j] = utils.BaseStation((j, i), world_map[i][j])
                    print("base location", world_map[i][j], (j, i))
                elif world_map[i][j] == ' ':
                    world_map[i][j] = utils.EmptySpot((j, i))
                    # print(utils.EmptySpot((j, i)))
        return world_map

    def get_cells(self, positions: list) -> dict[tuple[int, int], ...]:
        cells = {}
        for pos in positions:
            cells[pos] = self.world[pos[1]][pos[0]]
        return cells

    def __str__(self):
        out = ""
        for row in self.world:
            for col in row:
                out += f"{col}\t"
            out += "\n"
        return out

    @staticmethod
    def move_to(start, goal):
        valid = False
        if (goal[0], goal[1]) == (start[0] + 1, goal[1]):
            valid = True
        elif (goal[0], goal[1]) == (start[0] - 1, goal[1]):
            valid = True
        elif (goal[0], goal[1]) == (goal[0], start[1] + 1):
            valid = True
        elif (goal[0], goal[1]) == (goal[0], start[1] - 1):
            valid = True
        # print("goal", goal[0], goal[1])
        if valid is True:
            # print("success")
            return True
        else:
            return False


if __name__ == "__main__":
    floorplan = "floorplan1.txt"
    e = Environment(floorplan)
    robot1 = ""
    base1 = ""
    if floorplan == "floorplan1.txt":
        robot1 = e.world[10][3]
        base1 = e.world[11][3]
    elif floorplan == "floorplan2.txt":
        robot1 = e.world[1][4]
        base1 = e.world[1][8]
    print(e)
    count = 0
    while (robot1.battery_level <= 0 or count >= 500) is not True:
        base1.act(e)
        robot1.act(e)
        print(e)
        count += 1
        print("count =", count)
        # print(robot1.map)
        print("-----------------------------------------------------------------------")
    print("Program End. Cycles:", count)
    print(robot1.map)
