from io import BytesIO
from math import isqrt
from pathlib import Path
from typing import List, Optional, Tuple, Type, Union

import PIL
from PIL import Image

from utils.text_formatting import green, yellow
from utils.utils import handle_file, lsb_bits_to_string


def normalized_image(
    decoded_data: List[int],
    out_file: str = "normalized_image.png",
    dimensions: Tuple[int] = None
) -> bool:
    """Create a normalized image from the input `decoded_data` list,
    write the result to a file, and return a bool representing whether
    the operation was successful.

    :param decoded_data: List of ints to use in the normalized image.
        The length of the list must be a square number when
        `dimensions` is not provided.
    :param out_file: Filename of the image file to write to.
    :param dimensions: Tuple representing the dimensions of the
        `out_file` image in the format (width, height). If no
        dimensions are provided, it will be set to the square root of
        the length of the `decoded_data` list.
    :returns: Bool representing whether the operation was successful.
    """
    if not isinstance(decoded_data, list):
        print(yellow(f"`decoded_data` must be of type `list`, got type {type(decoded_data)}"))
        return False

    if not dimensions:
        # Get the largest integer, `size`, where `size` squared does not exceed `len(decoded_data)`
        size = isqrt(len(decoded_data))
        dimensions = (size, size)
        if size ** 2 != len(decoded_data):
            print(
                yellow(
                    f"The length of `decoded_data` must be a square number when `dimensions` "
                    f"is not provided. Got {len(decoded_data) = }"
                )
            )
            return False

        print(f"Using output dimensions {dimensions}")

    i = 0
    out_image = Image.new(mode="RGB", size=dimensions)
    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            pixel = (255, 255, 255) if decoded_data[i] else (0, 0, 0)
            out_image.putpixel((x, y), pixel)
            i += 1

    out_image.save(out_file, "png")

    return True


def read_image_lsb_data(
    filename: str,
    channel: int = 0,
    start: int = 0,
    stop: Optional[int] = None,
    return_type: Union[Type[str], Type[list]] = str
) -> Optional[Union[str, list]]:
    """Attempt to read LSB data from input file.

    :param filename: Name of the image file to read LSB data from.
    :param channel: Which color channel to attempt to read data from.
        0 = Red, 1 = Green, 2 = Blue.
    :param start: Position to start reading from. Starts at the
        beginning of the image file by default.
    :param stop: Position to stop reading at. Reads to the end
        of the image file by default.
    :param return_type: What type to return the image LSB data in.
        Either as a string of bits or a list of bits.
    :returns: Retrieved decoded bits, either as a string or list,
        or `None` on failure.
    """
    image_file = handle_file(file=filename, python_module=Path(__file__))
    if not image_file:
        # Could not find file `filename`
        return

    if return_type not in (str, list):
        print(yellow(f"The return_type must be set to either 'str' or 'list'. Got '{return_type}'"))
        return

    channel_map = {
        0: "red",
        1: "green",
        2: "blue",
    }
    if channel not in channel_map.keys():
        print(yellow(f"Invalid channel '{channel}'. Must be one of: '{list(channel_map.keys())}'."))
        return
    else:
        print(f"Extracting data from the {channel_map[channel]} color channel")

    i = 0
    lsb_bits = []
    done = False
    with Image.open(image_file) as img:
        width, height = img.size
        for x in range(width):
            if done:
                break

            for y in range(height):
                if done:
                    break

                if start <= i:
                    pixel = list(img.getpixel(xy=(x, y)))
                    lsb_bits.append(pixel[channel] & 1)

                i += 1
                if stop and i >= stop:
                    done = True

    if return_type is str:
        return lsb_bits_to_string(data=lsb_bits)
    elif return_type is list:
        return lsb_bits


def extract_jpg_data(jpg_filename: str, out_file: str = "embedded.png", byte_position: str = 'FFD8') -> None:
    """Extract data from a jpg file starting at the bytes matching `byte_position`.
    See https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format#File_format_structure for details.

    :param jpg_filename: Name of the jpg file to read data from.
    :param out_file: File to save extracted data to.
    :param byte_position: Start reading data after these bytes in the jpg file.
    :returns: None
    """
    jpg_file = handle_file(file=jpg_filename, python_module=Path(__file__))
    if not jpg_file:
        # Could not find file `jpg_filename`
        return

    try:
        with open(jpg_filename, "rb") as f:
            content = f.read()
            offset = content.index(bytes.fromhex(byte_position))
            f.seek(offset + 2)
            new_img = Image.open(BytesIO(f.read()))
            new_img.save(out_file)
    except PIL.UnidentifiedImageError:
        print(yellow(f"Unable to extract data from byte position '{byte_position}' in jpg file."))
        return

    print(green(f"Successfully extracted data from '{jpg_filename}', and saved result in '{out_file}'."))
