"""
This module contains functions for image processing.
"""

from PIL import Image


def rgbToBytes(rgb: tuple) -> bytearray:
    """
    Converts a tuple of RGB values to a bytes object.
    """
    if len(rgb) == 4:
        # eliminate the alpha value
        rgb = rgb[:3]

    elif len(rgb) != 3:
        raise ValueError("The tuple must contain 3 values.")
    result = bytearray()
    for i in rgb:
        result.append(i)
    return result


def hexToRgb(input_hex: str) -> tuple:
    if isinstance(input_hex, str) and len(input_hex) != 6:
        raise ValueError("The hex value must be a string of length 6.")

    return int(input_hex[1:3], 16), int(input_hex[3:5], 16), int(input_hex[5:7], 16)


def getColors(img: Image, x: int = None, y: int = None, width: int = None, height: int = None) -> dict:
    """
    Returns a dictionary where the keys are the coordinates of the pixels and the values are the colors of each pixel
    in hexadecimal format of a specified region of an image. If no region is specified, the colors of the whole image
    will be returned.
    """
    colors = {}
    for i in range(width):
        for j in range(height):
            colors[(x + i, y + j)] = rgbToBytes(img.getpixel((x + i, y + j)))
    return colors


def updatePixels(img: Image, x: int, y: int, width: int, height: int, color: tuple | list) -> Image:
    """
    Updates the pixels of an image given the coordinates of the top left corner, the width and height of the rectangle.
    The color argument can be either a tuple or a dictionary. If it is a tuple, then all the pixels in the specified
    region will be painted with the same color. If it is a list, it's length must be equal to the number of pixels in
    the specified region. The pixels will be painted with the colors in the list in the order they appear in it.
    """
    # Check if the color is a tuple or a list
    if color is list and len(color) != width * height:
        raise ValueError("The number of colors must be equal to the number of pixels in the specified region.")

    # If the color argument is a tuple
    if color is tuple:
        for i in range(y, height + y):
            for j in range(x, width + x):
                img.putpixel((j, i), color)

    # If the color argument is a list
    elif color is list:
        for i in range(y, height + y):
            for j in range(x, width + x):
                img.putpixel((j, i), color[i * j])
    else:
        raise ValueError("The color argument must be a tuple or a list.")

    return img


def binaryToRgb(binary: bytearray) -> tuple:
    """
    Converts a bytearray of length 3 to a tuple of RGB values.
    """
    if len(binary) != 3:
        raise ValueError("The bytearray must have a length of 3.")
    return int(binary[0]), int(binary[1]), int(binary[2])


def updatePixelsFromDict(img: Image, x: int, y: int, width: int, height: int, colors: dict) -> Image:
    """
    Updates the pixels of an image given the coordinates of the top left corner, the width and height of the rectangle.
    The color argument can be either a tuple or a dictionary. If it is a tuple, then all the pixels in the specified
    region will be painted with the same color. If it is a list, it's length must be equal to the number of pixels in
    the specified region. The pixels will be painted with the colors in the list in the order they appear in it.
    """
    # Check if the color is a tuple or a dictionary
    if not isinstance(colors, dict):
        raise ValueError("The color argument must be a dictionary.")

    # If the color argument is a tuple
    for i in range(width):
        for j in range(height):
            img.putpixel((x + i, y + j), binaryToRgb(colors[(x + i, y + j)]))

    return img
