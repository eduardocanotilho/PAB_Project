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

def count_bases(sequence: str) -> int:
    return len(sequence)

def list_sequences(sequences_repo: list[Sequence]) -> None:
    if sequences_repo == []:
        print(NOTHING_LOADED)
        return
    
    print(SEQUENCES_LOADED.format(num_sequences_loaded= len(sequences_repo)))

    for sequence in sequences_repo:
        print(LIST_SEQUENCES.format(sequence_id=sequence.sequence_id, num_bases=count_bases(sequence.sequence)))