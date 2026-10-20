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

RECOGNITION_SITES_NOT_FOUND = "The enzyme {enzyme_name} does not cut the sequence {sequence_id}."
RECOGNITION_SITES_FOUND = "Recognition sites of {enzyme_name} ({sequence}) in the sequence {sequence_id}:"
NUM_SITES_FOUND = "- Number of sites: {num_sites}."
POSITIONS_FOUND = "- Positions: {positions}."
# new constants
NO_FRAGS_PRODUCED = "The sequence {sequence_id} is not cut by the provided enzymes."
FRAGS_PRODUCED = "Digestion of the sequence {sequence_id} with {enzyme_names} produced the following fragments:"
LIST_FRAGS = "- {num_bases} bp (positions {start}-{end})"

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

command_args = ["pGFP_insert", "EcoRI", "HindIII"]
enzymes_repo = [Enzyme(enzyme_name="EcoRI", recognition_site="GAATTC", cut_offset=1), Enzyme(enzyme_name="BamHI", recognition_site="GGATCC", cut_offset=1), Enzyme("HindIII","AAGCTT",1)]
sequeces_repo = [Sequence(sequence_id="demo", sequence="ATGAATTCGGCCGAATTCTA"), Sequence("pGFP_insert","ACATCTGTCAATCCAATCAGTATAGGCTAGAATTCCCTCAAGTCAGCAACGTATACCATGGAACATCGAAGCGGCCGCTGGCAGCCACGGAAAAACACTTATACGAAATCCTCCAGGGTAGGATCCACTCTGCATTCCCCGAGTAATGGGAAGTCTGCCAGTGTAATCTCGTACTTAATATACAAGACGCAGAACCATGCGGATGTTGCAAGCTTGTACAAGACTATGTACCCTAGTCGC")]

def count_bases(sequence: str) -> int:
    return len(sequence)

def find_enzyme_in_repo(command_args: list[str], enzymes_repo: list[Enzyme]) -> bool:
    """Checks if an enzyme is in the enzymes repository"""
    enzymes_name_list: list[str] = []
    for enzyme in enzymes_repo:
        enzymes_name_list.append(enzyme.enzyme_name)

    for arg in command_args[1:]:
        if arg not in enzymes_name_list:
            print(UNKNOWN_ENZYME.format(enzyme_name=command_args[1]))
            return False
    return True
    
def find_sequence_in_repo(command_args: list[str], sequences_repo: list[Sequence]) -> bool:
    for seq in sequences_repo:
            if command_args[0] == seq.sequence_id:
                break
            print(SEQUENCE_NOT_LOADED.format(sequence_id=command_args[0]))
            return False
    return True

def find_cut_positions(sequence_to_look: str, enzyme_recognition: str) -> list[int]:
    positions: list[int] = []
    start = sequence_to_look.find(enzyme_recognition)
    while start != -1:
        positions.append(start + 1)
        start = sequence_to_look.find(enzyme_recognition, start + 1)
    return positions

def digest_sequence(command_args: list[str], enzymes_repo: list[Enzyme], sequences_repo: list[Sequence]) -> None:
    if not find_sequence_in_repo(command_args, sequences_repo):
        return
    if not find_enzyme_in_repo(command_args, enzymes_repo):
        return

    sequence_to_look: str = ""
    for seq in sequences_repo:
        if command_args[0] == seq.sequence_id:
            sequence_to_look = seq.sequence

    fragments: list[str] = [sequence_to_look]
    fragment_info: tuple[int] = ()

    for enzyme_name in command_args[1:]:
        enzyme_recognition: str = ""
        enzyme_cut: int = 0
        for enzyme in enzymes_repo:
            if enzyme_name == enzyme.enzyme_name:
                enzyme_recognition = enzyme.recognition_site
                enzyme_cut = int(enzyme.cut_offset)

        new_fragments: list[str] = []
        for fragment in fragments:
            positions = find_cut_positions(fragment, enzyme_recognition)
            start: int = 0
            for position in positions:
                cut_index = position + enzyme_cut - 1
                new_fragments.append(fragment[start:cut_index])
                start = cut_index
            new_fragments.append(fragment[start:])
        fragments = new_fragments
        print(new_fragments)
            
            


digest_sequence(command_args, enzymes_repo, sequeces_repo)



