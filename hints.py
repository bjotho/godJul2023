"""
Use this file to get hints to the challenges. Call the `hint` function with the challenge
number and optionally the hint number to get a hint for that challenge, ex:

To get the first hint for challenge 5, add:
    hint(5, 1)
to the bottom of this file.
To get the third hint for challenge 2, add:
    hint(2, 3)
"""

from pathlib import Path
from typing import Optional
from utils.text_formatting import red, yellow
from utils.utils import encrypt, lfsr


def hint(challenge_num: int, hint_num: int = 1, _print: bool = True) -> Optional[str]:
    """Get a hint for the challenge `challenge_num`.

    :param challenge_num: The challenge to get a hint for.
    :param hint_num: Which specific challenge hint to output.
    :param _print: Whether to print the hint.
    :returns: The hint `hint_num` for challenge `challenge_num`
        on valid inputs, otherwise `None`.
    """
    if challenge_num < 1 or challenge_num > 5:
        print(red(f"Invalid challenge number: {challenge_num}"))
        return

    hint_filepath = Path(__file__).parent.joinpath("data/hint_data")
    encrypted_hint = None
    try:
        with open(hint_filepath, 'r') as f:
            line = f.readline()
            while line != '':
                line = line.strip()
                if line.startswith('#'):
                    line = f.readline()
                    continue

                if line == f"c{challenge_num}h{hint_num}":
                    encrypted_hint = f.readline().strip()
                    break

                line = f.readline()

    except FileNotFoundError:
        print(yellow(f"The file at {hint_filepath} could not be found."))

    if encrypted_hint is None:
        if _print:
            print(yellow(f"Could not find hint {hint_num} for challenge {challenge_num}."))
            return

    output = encrypt(
        text=encrypted_hint,
        keystream=lfsr,
        keystream_kwargs={
            "seed": challenge_num * 1337,
            "mask": hint_num * 9001
        }
    )

    if _print:
        print(f"Challenge {challenge_num} hint {hint_num}:")
        print(output)


# To get the first hint for challenge 2:
# hint(2, 1)
