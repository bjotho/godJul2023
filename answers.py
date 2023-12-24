"""
Use this file to check if the answers you find for the challenges are correct, and to redeem a prize.

To check if an answer is correct, simply call the `check` function with the challenge number and the
answer you want to check, ex:

To check if the answer to challenge 3 is "kalleankasladrehanka", add
    check(3, "kalleankasladrehanka")
to the bottom of this file.

To redeem a prize, call the 'redeem_prize' function with your username and a list of all the
challenge answers on the bottom of this file, ex:

redeem_prize("your_username", ["answer1", "answer2", "answer3", ...])
"""

from hashlib import sha256
from pathlib import Path
from typing import List, Optional

from utils.text_formatting import green, red, yellow
from utils.utils import encrypt


def check(challenge: int, answer: str, _print: bool = True) -> bool:
    """Takes a challenge number and a string containing the answer to check for that challenge,
    and outputs whether the answer is correct or not.

    :param challenge: Integer corresponding to the challenge to check answer for.
    :param answer: The answer string to check.
    :param _print: Whether to print the result of the check.
    :returns: Boolean representing if the answer is correct or not.
    """
    sha256_filepath = Path(__file__).parent.joinpath("data/sha256_truncated")
    answer_hash = sha256(answer.encode("utf-8")).hexdigest()[:56]
    solution_hash = None
    try:
        with open(sha256_filepath, 'r') as f:
            for i, line in enumerate(f, start=1):
                if i == challenge:
                    solution_hash = line.strip()
                    break

        if not solution_hash:
            raise ValueError("Invalid challenge number")

        if answer_hash == solution_hash:
            if _print:
                print(green("The answer is correct!"))
            return True
        else:
            if _print:
                print(red("The answer is wrong."))
            return False

    except FileNotFoundError:
        print(yellow(f"The file at {sha256_filepath} could not be found."))
    except ValueError:
        print(yellow(f"The challenge number you provided ({challenge}) does not exist"))

    return False


def redeem_prize(username: str, answers: List[str]) -> Optional[str]:
    """Redeem a prize for the given username if all the answers in the `answers` list are correct

    :param username: Username to redeem a prize for.
    :param answers: List of challenge answers, where the 1st list entry corresponds to the answer
        to challenge 1, the second entry corresponds to the answer to challenge 2, and so on.
    :returns: A prize if all the challenge answers are correct...
    """
    sha256_filepath = Path(__file__).parent.joinpath("data/sha256_truncated")
    try:
        with open(sha256_filepath, 'r') as f:
            num_challenges = sum(1 for _ in f)
            if len(answers) != num_challenges:
                print(
                    yellow(
                        f"There are {num_challenges} challenges, but you provided {len(answers)} answers. "
                        f"Please provide one answer for each challenge."
                    )
                )
                return

            remainder_hashes = ""
            f.seek(0)
            for n, line in enumerate(f):
                answer_full_hash = sha256(answers[n].encode("utf-8")).hexdigest()
                answer_hash = answer_full_hash[:56]
                remainder_hash = answer_full_hash[56:]
                if answer_hash != line.strip():
                    print(
                        red(
                            f"The answer to challenge {n + 1}, '{answers[n]}' is incorrect. "
                            f"Skipping remaining challenges."
                        )
                    )
                    return

                remainder_hashes += remainder_hash

            prize = encrypt(username, remainder_hashes)
            print(f"{prize = }")

    except FileNotFoundError:
        print(yellow(f"The file at {sha256_filepath} could not be found."))


# To check if the answer to challenge 3 is "answer3":
# check(3, "answer3")

# To redeem a prize when you have found all the challenge answers:
# redeem_prize("your_username", ["answer1", "answer2", "answer3", ...])
