# --- Imports ---
import os
from dataclasses import dataclass

# --- Constants ---
DATA_FOLDER: str = "data"
COMMAND_PROMPT: str = "Command to execute: "
UNKNOWN_COMMAND: str = "Unknown command."
COMMAND_EXIT: str = "Goodbye!"
COMMANDS: list[str] = [
    "LOAD_SEQUENCES", "LIST_SEQUENCES", "SEQUENCE_INFO", "FIND_SITES"
    "DIGEST", "EXIT"
    ]
SEQUENCE_NOT_LOADED = "The sequence {sequence_id} is not loaded."
UNKNOWN_ENZYME = "The enzyme {enzyme_name} is not available."
SEQUENCE_HEADER_MARK = ">"
VALID_BASES = "ACGT"
FILE_LOADED = "File {fasta_file} validated and loaded!"
FILE_ALREADY_LOADED = "File {fasta_file} already loaded!"
INVALID_BASES = "File {fasta_file} could not be loaded. Sequence {sequence_id} contains invalid nucleotides."
FILE_DUPLICATED = "File {fasta_file} could not be loaded. Sequence {sequence_id} is already in use."
SEQUENCES_LOADED = "Number of sequences loaded: {num_sequences_loaded}"
LIST_SEQUENCES = "- {sequence_id} ({num_bases} bp)"
NOTHING_LOADED = "No sequences loaded."
# new constants
FIND_ENZYME_NOT_LOADED = "The enzyme {enzyme_name} is not available."
FIND_SEQUENCE_NOT_LOADED = "The sequence {sequence_id} is not loaded."
RECOGNITION_SITES_NOT_FOUND = "The enzyme {enzyme_name} does not cut the sequence {sequence_id}."
RECOGNITION_SITES_FOUND = "Recognition sites of {enzyme_name} ({sequence}) in the sequence {sequence_id}:"
NUM_SITES_FOUND = "- Number of sites: {num_sites}."
POSITIONS_FOUND = "- Positions: {positions}."

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

command_args = ["demo", "EcoRI"]
enzymes_repo = [Enzyme(enzyme_name="EcoRI", recognition_site="GAATTC", cut_offset=1)]
sequeces_repo = [Sequence(sequence_id="demo", sequence="ATGAATTCGGCCGAATTCTA")]

def count_bases(sequence: str) -> int:
    return len(sequence)

def find_enzyme_in_repo(command_args: list[str], enzymes_repo: list[Enzyme]) -> bool:
    for enzyme in enzymes_repo:
            if command_args[1] == enzyme.enzyme_name:
                break
            print(FIND_ENZYME_NOT_LOADED.format(enzyme_name=command_args[1]))
            return False
    return True
    
def find_sequence_in_repo(command_args: list[str], sequences_repo: list[Sequence]) -> bool:
    for seq in sequences_repo:
            if command_args[0] == seq.sequence_id:
                break
            print(FIND_SEQUENCE_NOT_LOADED.format(sequence_id=command_args[0]))
            return False
    return True
    
def find_sites(command_args: list[str], enzymes_repo: list[Enzyme], sequences_repo: list[Sequence]) -> None:
    if not find_sequence_in_repo(command_args, sequences_repo):
         return
    if not find_enzyme_in_repo(command_args, enzymes_repo):
         return
    
    sequence_to_look: str = ""
    for seq in sequences_repo:
         if command_args[0] == seq.sequence_id:
              sequence_to_look = seq.sequence
    
    enzyme_recognition: str = ""
    for enzyme in enzymes_repo:
         if command_args[1] == enzyme.enzyme_name:
              enzyme_recognition = enzyme.recognition_site

    positions: list[int] = []
    start = sequence_to_look.find(enzyme_recognition)
    while start != -1:
         positions.append(start + 1)
         start = sequence_to_look.find(enzyme_recognition, start + 1)

    if positions == []:
         print(RECOGNITION_SITES_NOT_FOUND.format(enzyme_name=command_args[1], sequence_id=command_args[0]))
         return
    else:
        print(RECOGNITION_SITES_FOUND.format(enzyme_name=command_args[1], sequence= enzyme_recognition, sequence_id=command_args[0]))
        print(NUM_SITES_FOUND.format(num_sites=len(positions)))
        print(POSITIONS_FOUND.format(positions=str(positions).strip("[").strip("]")))
        return

    
find_sites(command_args, enzymes_repo, sequeces_repo)