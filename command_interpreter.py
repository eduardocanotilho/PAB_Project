# --- Imports ---
import os
from dataclasses import dataclass

# --- Constants ---
DATA_FOLDER: str = "data"
COMMAND_PROMPT: str = "Command to execute: "
UNKNOWN_COMMAND: str = "Unknown command"
COMMAND_EXIT: str = "Goodbye!"
COMMANDS: list[str] = [
    "LOAD_SEQUENCES", "LIST_SEQUENCES", "SEQUENCE_INFO", "FIND_SITES"
    "DIGEST", "EXIT"
    ]

# --- Data Classes ---
@dataclass
class Sequence:
    """Single DNA Sequence"""
    sequence_id: str
    sequence: str

@dataclass
class Enzyme:
    """Single Restriction Enzyme"""
    enzyme_name: str
    recognition_site: str
    cut_offset: int

def load_enzymes(enzymes_data: str, enzymes_repo: list[Enzyme]) -> None:
    temp_list: list[str] = enzymes_data.split("\n")
    temp_elements: list[str, str, int] = []
    for enzyme in temp_list:
        temp_elements = enzyme.split(" ")
        if len(temp_elements) == 3:
            enzyme = Enzyme(enzyme_name=temp_elements[0], recognition_site=temp_elements[1], cut_offset=temp_elements[2])
            enzymes_repo.append(enzyme)
    return

def command_runner(command_name: str, command_args: list[str]) -> None:
    #if command_name == "LOAD_SEQUENCES":

    #if command_name == "LIST_SEQUENCES":

    #if command_name == "SEQUENCE_INFO":

    #if command_name == "FIND_SITES":

    #if command_name == "DIGEST":
    # idk

def command_interpreter(user_input: str) -> list[str, list[str]]:
    command_parts: str = user_input.split(" ")
    command, args = command_parts[0] , command_parts[1:]
    return [command, args]

def command_input() -> None:
    user_input: str = ""
    command_proprieties: list[str, list[str]] = []
    command_name: str = ""
    command_args: list[str] = []

    while True:
        user_input = input(COMMAND_PROMPT)
        command_proprieties = command_interpreter(user_input)
        command_name = command_proprieties[0]
        command_args = command_proprieties[1]
        if command_name not in COMMANDS:
            print(UNKNOWN_COMMAND)
            continue
        if command_name == COMMANDS[-1]:
            print(COMMAND_EXIT)
            return
    

def main() -> None:
    enzymes_repo: list[Enzyme] = []
    sequences_repo: list[Sequence] = []

    file_path = os.path.join(DATA_FOLDER, "enzymes.txt")
    with open(file_path) as handle:
        enzymes_data = handle.read()
    load_enzymes(enzymes_data, enzymes_repo)

    command_input()


if __name__ == "__main__":
    main()
