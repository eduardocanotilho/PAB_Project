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
    cut_offset: str

def command_interpreter() -> list[str, list[str]]:
    user_input: str = ""
    command_properties: list[str, list[str]] = []
    while True:
        user_input = input(COMMAND_PROMPT)
        if not user_input:
            continue
        command_parts: str = user_input.split(" ")
        command, args = command_parts[0] , command_parts[1:]
        
        return [command, args]
    

def main() -> None:
    file_path = os.path.join(DATA_FOLDER, "enzymes.txt")
    with open(file_path) as handle:
        enzymes = handle.read()
    enzymes_repo: list[Enzyme] = []
    sequences_repo: list[Sequence] = []

    command_interpreter()


if __name__ == "__main__":
    main()