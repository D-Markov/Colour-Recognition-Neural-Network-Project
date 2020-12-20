class TrainDataGenerator:
    def __init__(self, image):
        self.image = image

    def create_data(self, x_pos, colours_map):
        if min(x_pos) < 0 or max(x_pos) > self.image.size[0] -1 :
            raise ValueError(f"x-coordinate outside of image size of {self.image.size[0]}")

        colour_x_coordinates = [m[0] for m in colours_map]
        
        if min(colour_x_coordinates) < 0 or max(colour_x_coordinates) > self.image.size[0] - 1:
            raise ValueError(f"colour map x-coordinate outside of image size of {self.image.size[0]}")
        
        rgb_Vals = []

        for x in x_pos:
            colour = self.get_colour_name(colours_map, x)
            rgb = self.get_RGB(x, 0)
            rgb_Vals.append((rgb, colour))

        return rgb_Vals

    def get_RGB(self, x, y):
        return self.image.getpixel((x, y))[0:3]

    def get_colour_name(self, colours, x):
        count = 0
        
        while x - colours[count][0] > 0:
            count += 1
        
        return colours[count][1]
