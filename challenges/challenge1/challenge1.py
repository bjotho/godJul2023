
def rot(in_str: str, n: int) -> str:
    """Rotate each alphabet character in input string
    `in_str` by `n` positions, and output result.

    :param in_str: Input string
    :param n: Integer specifying how much to rotate the input string
    :returns: `in_str` rotated by `n` positions
    """

    # Get the ASCII values of 'a' and 'z', and calculate the range of the alphabet (26 in this case)
    start = ord('a')
    end = ord('z') + 1
    mod = end - start

    # Convert `in_str` to lower case
    in_str = in_str.lower()

    # Create new string to build the string of rotated characters
    out_str = ''
    # Loop over all characters in the input string
    for char in in_str:
        # Check if the character is a letter
        if start <= ord(char) < end:
            # Rotate the character `n` positions and add it to the end of `out_str`
            out_str += chr(((ord(char) - start + n) % mod) + start)
        else:
            # Add non-letter characters to the output string unchanged
            out_str += char

    # Return the rotated string
    return out_str


# This string contains the encrypted solution to this challenge
secret_string = "jrypbzr punyyratre"

# Examples:
print(rot("hello", 5))

n = 26
print(rot("I lost the game", n))

some_str = "abcdefghijklmnopqrstuvwxyz"
rotated = rot(some_str, -14)
print(rotated)
