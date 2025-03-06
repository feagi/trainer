import numpy as np
import sys
import argparse
from feagi_connector import feagi_interface as feagi


def expand_pixel(xyz_array, radius, width, height):
    """
    Expands each pixel in the input array by creating a square of pixels around it

    Args:
        xyz_array: numpy array of shape (N, 3) containing x,y coordinates
        radius: int, how many pixels to expand in each direction
        width: int, maximum width of the image
        height: int, maximum height of the image
    """
    # Create the offset ranges
    x_offsets = np.arange(-radius, radius)
    y_offsets = np.arange(-radius, radius)

    # Create meshgrid of offsets
    xx, yy = np.meshgrid(x_offsets, y_offsets)
    offsets = np.column_stack((xx.ravel(), yy.ravel()))

    # Expand the original array to match offsets shape
    expanded = xyz_array[:, np.newaxis, :]  # Shape becomes (1083, 1, 3)

    # Broadcasting magic happens here
    new_coords = expanded[:, :, :2] + offsets[np.newaxis, :, :]  # Add offsets to x,y coordinates

    # Clip to image boundaries
    new_coords[:, :, 0] = np.clip(new_coords[:, :, 0], 0, width)
    new_coords[:, :, 1] = np.clip(new_coords[:, :, 1], 0, height)

    # If there's a third column (e.g., intensity), repeat it for all expanded pixels
    if xyz_array.shape[1] > 2:
        new_values = np.repeat(xyz_array[:, 2:], offsets.shape[0]).reshape(xyz_array.shape[0], offsets.shape[0], -1)
        new_coords = np.concatenate([new_coords, new_values], axis=2)

    # Reshape to 2D array
    result = new_coords.reshape(-1, xyz_array.shape[1])

    return result


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

    sys.argv = [sys.argv[0]] + cleaned_args
    return csv_flag, range_value, args.csv_path
