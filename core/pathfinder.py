from PIL import Image, ImageDraw
from pathlib import Path



class Point:
    """
    Represents a point of elevation data.
    """
    def __init__(self, pt, val):
        self.pt = pt
        self.val = val



class Draw:
    """
    Represents a path. Includes methods to take in elevation data, draw a map, and find paths.
    """

    def __init__(self, data_file, pk):
        """
        @params = {
            @param data_file: txt file that contains points of elevation,
            @param data: array of elevation points from data_file,
            @param img: the map generated from the elevation data,
            @param rows: # of rows of data
            @param columns: # of columns of data
        }
        """
        self.data_file = data_file
        self.pk = pk
        self.data = []
        self.nest = []
        self.paths = []
        self.rows = 0
        self.columns = 0
        self.min_elevation = 0
        self.max_elevation = 0
        self.file_path = Path("core/static/images/elevation_map_paths" + str(self.pk) + ".png")
        self.name = "Map " + str(self.pk)

    def init_data(self, file):
        self.data_file = file
        
        # open file and store data in lines
        lines = file.readlines()
        q = 0
        for l in lines:
            q += 1
            if not l[0].isalpha() and q >= 8 and len(l)>200:
                clean_line = l[0:(len(l)-1)]
                aline = clean_line.split(" ")
                anotherline = []
                if aline != []:
                    for i in aline:
                        if i != "":
                            anotherline.append(int(i))
                if anotherline != []:
                    self.nest.append(anotherline)

        y = 0
        for row in self.nest:
            x = 0
            for val in row:
                pt = Point((x, y), int(val))
                self.data.append(pt)
                x +=1
            y += 1
        
        self.rows = len(self.nest)
        self.columns = len(self.nest[0])

        return self.data


    def get_max_min(self):
        self.min_elevation = self.data[0].val
        self.max_elevation = self.data[0].val
        for o in self.data:
            if o.val < self.min_elevation:
                self.min_elevation = o.val
            elif o.val > self.max_elevation:
                self.max_elevation = o.val
        self.max_elevation = int(self.max_elevation)
        self.min_elevation = int(self.min_elevation)


    def from_index_get_val(self, index):
        for o in self.data:
            if o.pt == index:
                return o.val

        return -1


    # returns the path with the least elevation change
    def path_least_change(self):
        best_path = self.paths[0]
        for path in self.paths:
            if path[1] < best_path[1]:
                best_path = path
        return best_path[0]


    def pathfinder(self, start_pt):
        """takes a starting y value.
        from there, finds the lowest elevation out of (x+1, y-1), (x+1, y), and (x+1, y+1).
        steps to that point and repeats the process"""
        x = 1
        y = start_pt
        points_in_path = [(0, start_pt)]
        path_and_change = []
        total_change = 0
        current_elevation = self.nest[start_pt][0]
        while x < (self.columns - 2):
            # automatically goes straight forward if neither up-forward or down-forward has less change
            best_choice = (x, y)
            best_y = y 
            
            # checks if up-forward has less change than forward
            if abs((self.nest[y - 1][x] - current_elevation)) < abs(self.nest[y][x] - current_elevation):
                # even if up-forward is less than forward, down-forward may still have less change
                if y < (self.rows - 1) and abs(self.nest[y - 1][x] - current_elevation) > abs(self.nest[y + 1][x] - current_elevation):
                    best_choice = (x, y + 1)
                    best_y = y + 1
                else:
                    best_choice = (x, y - 1)
                    best_y = y - 1
            # if forward-up has greater or equal elevation change than forward, forward-down may have less change than forward
            elif y < (self.rows - 1) and abs(self.nest[y + 1][x] - current_elevation) < abs(self.nest[y][x] - current_elevation):
                best_choice = (x, y + 1)
                best_y = y + 1
            #sets the current elevation to the elevation at the point pathfinder chooses to move to
            total_change += abs(self.nest[best_y][x] - current_elevation)
            current_elevation = self.nest[best_y][x]
            y = best_y
            points_in_path.append(best_choice)
            x += 1

        path_and_change.append(points_in_path)
        path_and_change.append(total_change)
        # stores each path with its total elevation change in paths
        self.paths.append(path_and_change)
        
        return points_in_path


    def draw_map(self):
        self.init_data(self.data_file)
        self.get_max_min()

        img = Image.new('RGBA', (self.columns, self.rows), (0, 77, 64))
        img.save(self.file_path)

        for x in range(self.columns - 1):
            print(f"Drawing map... {int((x / self.columns) * 100)}% complete")
            for y in range(self.rows - 1):
                img.putpixel((x, y), (
                    (int((self.nest[y][x] - self.min_elevation) / (self.max_elevation - self.min_elevation) * 255)), 
                    (int((self.nest[y][x] - self.min_elevation) / (self.max_elevation - self.min_elevation) * 255)), 
                    (int((self.nest[y][x] - self.min_elevation) / (self.max_elevation - self.min_elevation) * 255))))
        img.save(self.file_path)


        draw = ImageDraw.Draw(img)
        for x in range(self.rows - 1):
            draw.line(self.pathfinder(x), fill=(243, 156, 18))
            print(f"Drawing path {x}/{self.rows - 2}")
        draw.line(self.path_least_change(), fill=(244, 67, 54), width=2)
        print("Done.")
        print(" ")
        print("Map saved at " + str(self.file_path))

        img.save(self.file_path, format="png")

        return self.file_path
