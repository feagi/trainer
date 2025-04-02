import numpy as np
import sys
import argparse
from feagi_connector import feagi_interface as feagi


def expand_pixel(x: int, y: int, magnification: int, width: int, height: int) -> list:
    """
    Expands a single pixel (x, y) into a larger dot based on the magnification factor.
    Ensures the expanded range does not exceed the frame boundaries (width, height).
    Returns a list of tuples representing the new pixel coordinates.
    """
    expanded_pixels = []
    radius = magnification // 2  # Defines the range to expand around the pixel

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < width and 0 <= new_y < height:  # Ensure within bounds
                expanded_pixels.append((new_x, new_y))
    return expanded_pixels


# def expand_pixel(xyz_array, magnification: int, width: int, height: int) -> list:
#     """
#     Expands a single pixel (x, y) into a larger dot based on the magnification factor.
#     Ensures the expanded range does not exceed the frame boundaries (width, height).
#     Returns a list of tuples representing the new pixel coordinates.
#     """
#     radius = magnification // 2  # Defines the range to expand around the pixel
#     xyz_array[:, 0] = range(max(xyz_array[:, 0] - radius, 0), min(xyz_array[:, 0] + radius, width - 1) + 1)
#     xyz_array[:, 1] = range(max(xyz_array[:, 1] - radius, 0), min(xyz_array[:, 1] + radius, height - 1) + 1)
#     return xyz_array

def check_the_flag():
    parser = argparse.ArgumentParser(description="read csv")
    parser.add_argument(
        "--csv_data_range",
        type=int,
        nargs=2,
        default=[0, 10],
        help="define the min and max range"
    )
    parser.add_argument(
        "--csv_path",
        type=str,
        help="path to csv file"
    )
    parser.add_argument(
        "--stimulation_period",
        type=float,
        default=1,
        help="for how long it stays display the voxel"
    )
    parser.add_argument(
        "--stimulation_gap",
        type=float,
        default=0,
        help="for how long gap between 2 rows of data"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Enable testing mode and it will disable trainer ID"
    )

    args, remaining_args = parser.parse_known_args()
    if args.csv_path:
        csv_flag = True
    else:
        csv_flag = False
    range_value = list(args.csv_data_range)
    available_list_from_feagi_connector = feagi.get_flag_list()
    cleaned_args = []
    skip_next = False
    for i, arg in enumerate(sys.argv[1:]):
        if skip_next:
            skip_next = False
            continue
        if arg in available_list_from_feagi_connector:
            cleaned_args.append(arg)
            if i + 1 < len(sys.argv[1:]) and not sys.argv[1:][i + 1].startswith("-"):
                cleaned_args.append(sys.argv[1:][i + 1])
                skip_next = True

    sys.argv = [sys.argv[0]] + remaining_args
    return csv_flag, range_value, args.csv_path, args.stimulation_period, args.stimulation_gap, args.test
