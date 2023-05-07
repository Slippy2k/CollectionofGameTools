"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

# Program tested on Python 3.11

# Ver    Date        Author               Comment
# v0.1   12.04.2023  Bartlomiej Duda      -
# v0.2   23.04.2023  Bartlomiej Duda      Add ReverseBox Translation Handler
# v0.3   25.04.2023  Bartlomiej Duda      Add more entries
# v0.4   01.05.2023  Bartlomiej Duda      Add more entries, update ReverseBox, add character mapping
# v0.5   01.05.2023  Bartlomiej Duda      Add more entries, List reverse

from typing import List

from reversebox.common.logger import get_logger
from reversebox.io_files.translation_text_handler import TranslationTextHandler, TranslationEntry

from character_mapping import tail_concerto_import_transform
from translation_memory import translation_memory

logger = get_logger(__name__)


# Adjust parameters below before using this tool!
# Read README file for more details
bin_file_path: str = "C:\\EMULACJA\\AA_GRY_PS1\\Tail Concerto\\OUT\\DATA.BIN"
po_file_path: str = "C:\\EMULACJA\\AA_GRY_PS1\\Tail Concerto\\OUT\\DATA.BIN.po"

option: int = 1     # 1 - export text   /   2 - import text


def get_datetime_string() -> str:
    return "29/04/2023 20:06:57"


def get_tail_concerto_encoding() -> str:
    return "windows-1250"


def generate_translation_entries(txt_file_path: str, text_key: str = "text_to_translate") -> bool:  # TODO - move it to reversebox
    """
    This function should be used along with "strings" program from SysInternals https://learn.microsoft.com/en-us/sysinternals/downloads/strings
    First, you should generate text dump using command "strings64.exe -o <binary_file_path> > <output_path>.
    Then you should search for text entries in the dump and copy them to some output file e.g. "entries.txt"
    Then you just need to run this function with your "entries.txt" as an input parameter for this function.
    """
    try:
        txt_file = open(txt_file_path, "rt")
    except Exception as error:
        logger.error(f"Error with opening file: {error}")
        return False

    for line in txt_file:
        line = line.strip()
        offset = line.split(":")[0]
        text = line.split(":")[-1]
        output_entry = f"\tTranslationEntry(text_offset={offset}, text_export_length={len(text)}, text_key=\"{text_key}\"),"
        print(output_entry)

    return True


def check_translation_entries(translation_memory_to_check: List[TranslationEntry]) -> bool:
    """
    Default function for checking if entries in Translation Memory are correct.
    """
    check_offsets_list: List[int] = []

    for translation_entry in translation_memory_to_check:
        if translation_entry.text_offset in check_offsets_list:
            logger.error(f"Duplicated text_offset: {translation_entry.text_offset}")
            return False

        if translation_entry.text_import_length and translation_entry.text_import_length < translation_entry.text_export_length:
            logger.error(f"Import length is lower than export length for entry with offset {translation_entry.text_offset}")
            return False

        check_offsets_list.append(translation_entry.text_offset)
    return True


def main():
    reversed_translation_memory: List[TranslationEntry] = list(reversed(translation_memory))
    if not check_translation_entries(reversed_translation_memory):
        logger.error("Error while checking translation memory")
        return
    translation_handler = TranslationTextHandler(
            translation_memory=reversed_translation_memory, file_path=bin_file_path,
            global_import_function=tail_concerto_import_transform,
        )

    if option == 1 and translation_handler.export_all_text(po_file_path, creation_date_string=get_datetime_string(),
                                                           revision_date_string=get_datetime_string(),
                                                           encoding=get_tail_concerto_encoding()):
        logger.info("Text exported successfully!")
    elif option == 2 and translation_handler.import_all_text(po_file_path, create_backup_file=False,
                                                             encoding=get_tail_concerto_encoding()):
        logger.info("Text imported successfully!")
    else:
        logger.error("Wrong option or some error occurred! See the logs for more details.")


if __name__ == "__main__":
    main()
