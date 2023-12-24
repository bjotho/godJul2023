from typing import Dict
from string import ascii_lowercase
from utils.text_formatting import bright_blue


def letter_frequency(string: str, _print=True) -> Dict[str, int]:
    """Given an input string, generate a dictionary containing
    a mapping of the letter frequency in the string, and print
    the mapping to the console if `_print` is True.

    :param string: Input string.
    :param _print: Whether to print the mapping to the console.
    :returns: Dictionary of letter frequency in input string.
    """
    mapping = {}
    for char in string:
        char = char.lower()
        if char not in ascii_lowercase:
            continue
        elif char not in mapping:
            mapping[char] = 1
        else:
            mapping[char] += 1

    if _print:
        print("Ciphertext letter frequency:")
        for k, v in sorted(mapping.items(), key=lambda x: x[1], reverse=True):
            print(f"{k}: {v}")

    return mapping


def replace(string: str, mapping: dict, _print=True, color: callable = bright_blue) -> str:
    """Given a dictionary containing a mapping of characters,
    substitute all characters in the input string according
    to the `mapping` dict and output the result.

    Ex.
    string = "stay happy"
    mapping = {
        's': 'c',
        't': 'o',
        'a': 'l',
        'y': 'd',
        'h': 'b',
        'p': 'e',
    }
    returns "cold bleed"

    :param string: Input string to map.
    :param mapping: Dictionary mapping between characters.
    :param _print: Whether to print the mapped string to the console.
    :param color: Color of replaced characters if printing is enabled.
    :returns: Mapped string
    """

    # Default no-operation function to replace `color` if it's set to None
    def noop(text: str) -> str: return text

    if not color:
        color = noop

    output = ""
    for char in string:
        char = char.lower()
        if char in mapping.keys():
            output += color(text=mapping[char])
        else:
            output += char

    if _print:
        print("Decrypted:\n ", output)

    return output


ciphertext = """ajlnclfwq tftrqkek ek gtklu hf spl atws spts, ef tfq zevlf ksjlswp ha xjesslf rtfzctzl,
wljstef rlssljk tfu whygeftsehfk ha rlssljk hwwcj xesp vtjqefz ajlnclfwelk. yhjlhvlj, spljl ek t
wptjtwsljeksew ueksjegcsehf ha rlssljk spts ek jhczprq spl ktyl ahj tryhks trr ktyorlk ha spts
rtfzctzl. ahj efkstfwl, zevlf t klwsehf ha lfzrekp rtfzctzl, l, s, t tfu h tjl spl yhks whyyhf,
xperl d, n, b tfu i tjl jtjl. remlxekl, sp, lj, hf, tfu tf tjl spl yhks whyyhf otejk ha rlssljk
(sljylu gezjtyk hj uezjtopk), tfu kk, ll, ss, tfu aa tjl spl yhks whyyhf jloltsk. spl fhfklfkl
opjtkl "lsthef kpjurc" jlojlklfsk spl sxlrvl yhks ajlnclfs rlssljk ef sqoewtr lfzrekp rtfzctzl
slbs, tfu ek trkh spl tfkxlj sh spek wptrrlfzl. ef khyl weopljk, kcwp ojholjselk ha spl ftscjtr
rtfzctzl ortefslbs tjl ojlkljvlu ef spl weopljslbs, tfu splkl otssljfk ptvl spl ohslfsetr sh gl
lborheslu ef t weopljslbs-hfrq tsstwm."""


print("Ciphertext:\n ", ciphertext)
letter_frequency(string=ciphertext)

char_map = {

}

replace(string=ciphertext, mapping=char_map)
