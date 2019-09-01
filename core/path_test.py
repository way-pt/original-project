from pathfinder import Map
from pathlib import Path

file = open(Path("elevation_small.txt"))

test_map = Map(file)
test_map.draw_map()
file.close()
