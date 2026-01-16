"""
given n non negative int array, representing an elevation map;
width of each bar is 1,
compute the water trapped after raining

example:
    height = [0,1,0,2,1,0,1,3,2,1,2,1]

we can look at the input visually:
    height of rocks is black
    water is blue
    air is white
    required water = total - black - air
"""


def trapped_water(height: list[int]) -> int:
    # total box area
    peak_h = max(height)
    width = len(height)

    total_area = peak_h * width

    # area of rock (black)
    black_area = sum(height)

    # air area
    # left to peak
    white_area = 0
    index = 0
    peak_index = height.index(peak_h)
    while index < peak_index:
        white_area += peak_h - height[index]
        index += 1

    # right to peak
    index = width - 1
    while index > peak_index:
        white_area += peak_h - height[index]
        index -= 1

    # required answer blue
    blue_area = total_area - black_area - white_area
    return blue_area
