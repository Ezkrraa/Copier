import os, codecs
import charwidth

PAGE_LINES = 14
PAGE_WIDTH_PX = 115
LINE_WIDTH_PX = 100  # should be 122?? but 100 is not working


def split_into_pages_and_lines(text: str) -> list[list[str]]:
    words = text.split()
    pages = []
    current_page = []
    current_line = ""
    current_line_width_px = 0

    for word in words:
        word_width_px = charwidth.wordwidth(word)
        space_width_px = charwidth.charwidth(" ")

        # handle words longer than one line wide
        if word_width_px > LINE_WIDTH_PX:
            # flush if there's a new line
            if current_line:
                current_page.append(current_line)
                current_line = ""
                current_line_width_px = 0

            # break the long word into parts that fit
            for character in word:
                char_width_px = charwidth.charwidth(character)
                # if adding this word exceeds line width, flush
                if current_line_width_px + char_width_px > LINE_WIDTH_PX:
                    if current_line:
                        current_page.append(current_line)
                        current_line = ""
                        current_line_width_px = 0
                    # add the character to the new line
                    current_line += character
                    current_line_width_px = char_width_px
                else:
                    # if it fits, just add it to the current line
                    current_line += character
                    current_line_width_px += char_width_px

            # not yet sure if this is desired behavior
            # after processing the long word, make a new line
            if current_line:
                current_page.append(current_line)
                current_line = ""
                current_line_width_px = 0

            # check if page is full
            if len(current_page) >= PAGE_LINES:
                pages.append(current_page)
                current_page = []

            continue

        # handle words that fit within the line width
        if current_line_width_px + word_width_px + (space_width_px if current_line else 0) <= LINE_WIDTH_PX:
            if current_line:
                current_line += " "
                current_line_width_px += space_width_px
            current_line += word
            current_line_width_px += word_width_px
        else:
            # if current line is full, flush
            if current_line:
                current_page.append(current_line)
                current_line = ""
                current_line_width_px = 0

            # check if page is full
            if len(current_page) >= PAGE_LINES:
                pages.append(current_page)
                current_page = []

            # start a new line with the current word
            current_line = word
            current_line_width_px = word_width_px

    # add what's left
    if current_line:
        current_page.append(current_line)
    if current_page:
        pages.append(current_page)

    return pages
