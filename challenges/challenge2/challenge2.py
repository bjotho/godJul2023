from itertools import zip_longest
from pathlib import Path


def get_file_content(filepath: Path) -> str:
    """Read file at `filepath`, and output the content of the file as a string

    :param filepath: pathlib.Path object pointing to the file
    :raises FileNotFoundError: If no file exists at `filepath`
    :raises NotADirectoryError: If `filepath` points to non-existing directory
    :returns: String of file content
    """

    with open(filepath, 'r') as f:
        file_content = f.read()

    return file_content


# Read content of files `file1`, `file2`, `file3` and `file4` into variables
file1_content = get_file_content(Path(f"{__file__}").parent.joinpath("file1"))
file2_content = get_file_content(Path(f"{__file__}").parent.joinpath("file2"))
file3_content = get_file_content(Path(f"{__file__}").parent.joinpath("file3"))
file4_content = get_file_content(Path(f"{__file__}").parent.joinpath("file4"))

for n, content in enumerate((file1_content, file2_content, file3_content, file4_content)):
    print(f"file{n}_{content = }")

print("")

# Build a string by sequentially adding one character from each file at a time
output = ""
for a, b, c, d in zip_longest(file1_content, file2_content, file3_content, file4_content, fillvalue=''):
    output += f"{a}{b}{c}{d}"

print(f"{output = }")
