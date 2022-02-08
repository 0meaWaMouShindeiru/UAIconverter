

def calculate_center_position_from_dimensions(x, y, z, height, length, width):
    # Specification says order is "front, left, up"
    # UAI coordinate system, from picture:
    # y axis points up -> height
    # x axis points right (left) -> length
    # z axis points towards (front) -> width
    front = width/2 + z
    left = length/2 + x
    up = height/2 + y
    return front, left, up
