# --- Imports ---
import os
from dataclasses import dataclass

# --- Constants ---
DATA_FOLDER: str = "data"
ENZYMES_FOLDER: str = "enzymes.txt"
COMMAND_PROMPT: str = "Command to execute: "
UNKNOWN_COMMAND: str = "Unknown command."
COMMAND_EXIT: str = "Goodbye!"
COMMANDS: list[str] = [
    "LOAD_SEQUENCES", "LIST_SEQUENCES", "SEQUENCE_INFO", "FIND_SITES",
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

def load_enzymes(enzymes_data: str, enzymes_repo: list[Enzyme]) -> None:
    """Loads enzymes from a string into the enzymes repository"""
    temp_list: list[str] = enzymes_data.split("\n")
    temp_elements: list[str, str, int] = []
    for enzymes in temp_list:
        temp_elements = enzymes.split(" ")
        if len(temp_elements) == 3:
            enzyme = Enzyme(enzyme_name=temp_elements[0], recognition_site=temp_elements[1], cut_offset=temp_elements[2])
            enzymes_repo.append(enzyme)
    return

def count_bases(sequence: str) -> int:
    """Counts the number of base pairs in a sequence"""
    return len(sequence)

def find_enzyme_in_repo(command_args: list[str], enzymes_repo: list[Enzyme]) -> bool:
    """Checks if an enzyme is in the enzymes repository"""
    for enzyme in enzymes_repo:
            if command_args[1] == enzyme.enzyme_name:
                return True
    print(FIND_ENZYME_NOT_LOADED.format(enzyme_name=command_args[1]))
    return False

def find_sequence_in_repo(command_args: list[str], sequences_repo: list[Sequence]) -> bool:
    """Checks if a sequence is in the sequences repository"""
    for seq in sequences_repo:
            if command_args[0] == seq.sequence_id:
                return True
    print(FIND_SEQUENCE_NOT_LOADED.format(sequence_id=command_args[0]))
    return False
    
def find_sites(command_args: list[str], enzymes_repo: list[Enzyme], sequences_repo: list[Sequence]) -> None:
    """Finds the recognition sites of an enzyme in a sequence and prints the results"""
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

def list_sequences(sequences_repo: list[Sequence]) -> None:
    """Lists all loaded sequences and their lengths (bps)"""
    if sequences_repo == []:
        print(NOTHING_LOADED)
        return
    
    print(SEQUENCES_LOADED.format(num_sequences_loaded= len(sequences_repo)))
    for sequence in sequences_repo:
        print(LIST_SEQUENCES.format(sequence_id=sequence.sequence_id, num_bases=count_bases(sequence.sequence)))
    return

def valid_sequence(sequence: str) -> bool:
    """"Checks if a sequence contains only valid nucleotides (A, C, G, T)"""
    for nucleotide in sequence:
        if nucleotide in VALID_BASES:
            continue
        else:
            return False
    return True

def load_fasta(fasta_file: str) -> str:
    """Loads fasta file and returns its content as a list of strings"""
    file_path = os.path.join(DATA_FOLDER, fasta_file)
    with open(file_path) as handle:
        fasta_data = handle.readlines()
    return fasta_data

def load_sequences(command_args: list[str], sequences_repo: list[Sequence], fasta_repo: list[str]) -> None:
    """Loads sequences from fasta files into the sequences repository"""
    # Check if the fasta file is already loaded
    for fasta_file in command_args:
        if fasta_file in fasta_repo:
            print(FILE_ALREADY_LOADED.format(fasta_file=fasta_file))
            return

        new_sequences: list[Sequence] = []
        current_id: str = ""
        current_parts: str = ""

        # Loads sequences IDs and sequences from the fasta file, validating its bases
        for line in load_fasta(fasta_file):
            line = line.strip()
            if line.startswith(SEQUENCE_HEADER_MARK):
                if current_id != "":
                    new_sequences.append(Sequence(sequence_id=current_id, sequence=current_parts))
                current_id = line.split(" ")[0][1:]
                current_parts = ""
            else:
                if valid_sequence(line) == False:
                    print(INVALID_BASES.format(fasta_file=fasta_file, sequence_id=current_id))
                    return
                current_parts += line

        # Add the last instance of a sequence
        if current_id != "":
            new_sequences.append(Sequence(sequence_id=current_id, sequence=current_parts))

        seen_ids: set[str] = set()
        for seq in sequences_repo:
            seen_ids.add(seq.sequence_id)

        # Check for duplicate sequence IDs in the new sequences found
        for seq in new_sequences:
            if seq.sequence_id in seen_ids:
                print(FILE_DUPLICATED.format(fasta_file=fasta_file, sequence_id=seq.sequence_id))
                return
            seen_ids.add(seq.sequence_id)

        # If all checks pass, add the loaded fasta file and its sequences to the repositories
        sequences_repo.extend(new_sequences)
        fasta_repo.append(fasta_file)
        print(FILE_LOADED.format(fasta_file=fasta_file))

def command_runner(command_name: str, command_args: list[str], enzymes_repo: list[Enzyme], fasta_repo: list[str], sequences_repo: list[Sequence]) -> None:
    """Runs the command based on the command name and arguments"""
    if command_name == "LOAD_SEQUENCES":
        load_sequences(command_args, sequences_repo, fasta_repo)
        return
    if command_name == "LIST_SEQUENCES":
        list_sequences(sequences_repo)
        return
    #if command_name == "SEQUENCE_INFO":

    if command_name == "FIND_SITES":
        find_sites(command_args, enzymes_repo, sequences_repo)
        return
    #if command_name == "DIGEST":

def command_interpreter(user_input: str) -> list[str, list[str]]:
    """Interprets user input and returns command name and arguments"""
    command_parts: str = user_input.split(" ")
    command, args = command_parts[0] , command_parts[1:]
    return [command, args]

def command_input(enzymes_repo: list[Enzyme]) -> None:
    """Handles user input and command execution"""
    user_input: str = ""
    command_proprieties: list[str, list[str]] = []
    command_name: str = ""
    command_args: list[str] = []
    fasta_repo: list[str] = []
    sequences_repo: list[Sequence] = []

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
        command_runner(command_name, command_args, enzymes_repo, fasta_repo, sequences_repo)
    

def main() -> None:
    """Main function to load enzymes and start command input"""
    enzymes_repo: list[Enzyme] = []
    file_path = os.path.join(DATA_FOLDER, ENZYMES_FOLDER)
    with open(file_path) as handle:
        enzymes_data = handle.read()
    load_enzymes(enzymes_data, enzymes_repo)
    command_input(enzymes_repo)

if __name__ == "__main__":
    main()
