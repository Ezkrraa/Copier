def charwidth(char: str) -> int:
    if len(char) != 1:
        raise Exception("Tried to get the character width of a non-character")
    different_chars = {
        "I": 4,
        "f": 5,
        "i": 2,
        "l": 3,
        "t": 4,
        " ": 4,
        ":": 2,
        "!": 2,
        "|": 2,
        "`": 3,
        "*": 4,
        ",": 2,
        ".": 2,
    }
    if char in different_chars.keys():
        return different_chars[char]
    return 6


def wordwidth(word: str) -> int:
    return sum([charwidth(char) for char in word])
