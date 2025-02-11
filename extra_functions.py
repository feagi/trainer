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