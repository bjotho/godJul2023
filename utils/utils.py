from pathlib import Path
from typing import Any, Callable, Collection, Dict, Iterator, List, Optional

try:
    from utils.text_formatting import yellow
except ModuleNotFoundError:
    from text_formatting import yellow

from string import digits, ascii_lowercase, ascii_uppercase


ALPHABET = f"{ascii_uppercase}{ascii_lowercase}{digits}+/"

# b64_xor dicts mapping characters to base64 character codes, and reverse
ord_map = {ALPHABET[i]: i for i in range(len(ALPHABET))}
chr_map = {i: ALPHABET[i] for i in range(len(ALPHABET))}


def _ord(x: str) -> Optional[int]:
    """Map an input character `x` to corresponding base64 code.

    :param x: String containing character to map.
    :returns: Base64 character code, or `None` if the character does not exist in the
        mapping dict `ord_map`.
    """
    return ord_map.get(x)


def _chr(x: int) -> Optional[str]:
    """Map an input int `x` to corresponding base64 character.

    :param x: Int representing base64 character code.
    :returns: String containing the character corresponding to the base64 character code
        given in `x`, or `None` if `x` does not exist in the mapping dict `chr_map`.
    """
    return chr_map.get(x)


def handle_file(file: str, python_module: Path, _print: bool = True) -> Optional[Path]:
    """Handle an input filename or path and return Path object to given file.

    :param file: Filename or absolute path to file.
    :param python_module: Path to the python module calling this function.
    :param _print: Whether to print to console if file is not found.
    :returns: Path object to file.
    """

    file = Path(file)
    if not file.is_file():
        file = python_module.parent.joinpath(file)
        if not file.is_file():
            print(
                yellow(
                    f"Could not find file '{file}'. Either provide an absolute path "
                    f"to the file, or place the file in the same directory as this script."
                )
            )
            return

    return file


def chunker(sequence: Collection[Any], size: int) -> Iterator[List[Any]]:
    """Splits input sequence into chunks of equal size, and returns
    an iterable of the sequence items.

    :param sequence: Sequence to break into chunks.
    :param size: Size of each chunk.
    :returns: Iterable of lists (i.e. chunks).
    """
    for pos in range(0, len(sequence), size):
        yield sequence[pos:pos + size]


def lsb_bits_to_string(data: List[int], char_size: int = 8) -> str:
    """Decode binary LSB data retrieved from image, and return
    string containing decoded data.

    :param data: Binary encoded LSB data.
    :param char_size: number of bits used for representing a char.
        Default size is 8 bits per char.
    :returns: String of decoded LSB data.
    """
    output = ''
    for byte in chunker(sequence=data, size=char_size):
        char = 0
        for bit in byte:
            char = (char << 1) | bit

        output += chr(char)

    return output


def b64_xor(str1: str, str2: str) -> Optional[str]:
    """Using a custom implementation of the `ord()` and `chr()` builtin functions, calculate the XOR
    of `str1` and `str2`, such that the result always produces a string containing characters in the
    alphabet containing all base64 characters: `[A-Z][a-z][0-9][+/]`.

    :param str1: First input string to XOR.
    :param str2: Second input string to XOR.
    :returns: Result of `str1 XOR str2`, within the alphabet `ALPHABET`.
    """

    if len(str1) != len(str2):
        print(yellow(f"Input string lengths must be equal. Got {len(str1) = } and {len(str2) = }"))
        return

    for arg in (str1, str2):
        for c in arg:
            if _ord(c) is None:
                print(yellow(f"Got invalid character '{c}'. Valid characters are: '{ALPHABET}'."))
                return

    return "".join(_chr(_ord(u) ^ _ord(h)) for u, h in zip(str1, str2))


def clean_string(string: str) -> str:
    """Remove non-alphabet characters from the input string.

    :param string: String to clean.
    :returns: String only containing characters from `ALPHABET`.
    """
    clean_str = ""
    for char in string:
        if char in ALPHABET:
            clean_str += char

    return clean_str


def encrypt(
    text: str,
    key: Optional[str] = None,
    keystream: Callable = None,
    keystream_kwargs: Optional[Dict] = None
) -> str:
    """Encrypt input text with the given key using b64_xor encryption.

    :param text: The text string to encrypt.
    :param key: Key to use for encrypting the text.
        Only used with the default keystream generator.
    :param keystream: Generator to use for generating the keystream bits.
        Defaults to a rotating key keystream.
    :param keystream_kwargs: Keyword arguments to the keystream generator.
        Only necessary if `keystream` is provided.
    :raises ValueError: If both `key` and `keystream` are `None`,
        if `keystream` is provided, but not `keystream_kwargs`,
        or if `keystream_kwargs` is provided, but not `keystream`.
    :returns: Encrypted string.
    """

    if key is None and keystream is None:
        raise ValueError("`key` and `keystream` cannot both be `None`")
    elif keystream is not None and keystream_kwargs is None:
        raise ValueError(
            f"`keystream_kwargs` must be provided if `keystream` is provided. Got {keystream = }, {keystream_kwargs = }"
        )
    elif keystream is None and keystream_kwargs is not None:
        raise ValueError(f"`keystream_kwargs` cannot be provided when `keystream` is not provided")

    def default_keystream_generator():
        """Get the next key char"""
        i = 0
        while True:
            yield key[i % len(key)]
            i += 1

    if keystream is None:
        keystream = default_keystream_generator
        keystream_kwargs = {}

    encrypted = ""
    _keystream = keystream(**keystream_kwargs)
    for n, char in enumerate(text):
        if char in ALPHABET:
            k = _keystream.__next__()
            if isinstance(k, int):
                k = _chr(k % len(ALPHABET))

            encrypted += b64_xor(char, k)
        else:
            encrypted += char

    return encrypted


def lfsr(seed: int, mask: int, skip: int = 10) -> Iterator[int]:
    """Linear feedback shift register for generating pseudorandom bits

    :param seed: Initial integer to start the bit generation process (key).
    :param mask: Mask to calculate XOR for each iteration.
    :param skip: Skip yielding the first `skip` iterations.
    :yields: Pseudorandom integer.
    """
    result = seed
    nbits = mask.bit_length() - 1
    i = 0
    while True:
        result = (result << 1)
        xor = result >> nbits
        if xor != 0:
            result ^= mask

        if i >= skip:
            yield result

        i += 1
