import math

class Coordinate:
    def __init__(self, frac: (float, float), absolute: (int, int), absolute_size: (int, int)):

        if frac == None:
            abs_x, abs_y = absolute
            abs_size_x, abs_size_y = absolute_size

            self.frac_x = abs_x / abs_size_x
            self.frac_y = abs_y / abs_size_y
        else:
            frac_x, frac_y = frac
            self.frac_x = frac_x
            self.frac_y = frac_y

            
    def frac(self) -> (float, float):
        return (self.frac_x, self.frac_y)

    
    def absolute(self, absolute_size: (int, int)) -> (int, int):
        abs_size_x, abs_size_y = absolute_size
        return (int(self.frac_x * abs_size_x), int(self.frac_y * abs_size_y))


    def frac_distance_from(self, c: 'coord') -> float:
        return math.sqrt(
            (self.frac_x - c.frac_x) * (self.frac_x - c.frac_x) + (self.frac_y - c.frac_y) * (self.frac_y - c.frac_y))

    
def from_frac(frac: (float, float)) -> Coordinate:
    return Coordinate(frac, None, None)


def from_absolute(absolute: (int, int), absolute_size: (int, int)) -> Coordinate:
    return Coordinate(None, absolute, absolute_size)
