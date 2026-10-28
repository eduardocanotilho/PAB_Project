# ------------------------------------
# 1. IMPORTS
# ------------------------------------
import os
from dataclasses import dataclass

# ------------------------------------
# 2. CONSTANTS
# ------------------------------------

# --- Settings ---
DATA_FOLDER: str = "data"
ENZYMES_FOLDER: str = "enzymes.txt"
SEQUENCE_HEADER_MARK = ">"
VALID_BASES = "ACGT"

# --- Command names ---
COMMAND_PROMPT: str = "Command to execute: "
UNKNOWN_COMMAND: str = "Unknown command."
COMMAND_EXIT: str = "Goodbye!"
COMMANDS: list[str] = [
    "LOAD_SEQUENCES", "LIST_SEQUENCES", "SEQUENCE_INFO", "FIND_SITES",
    "DIGEST", "EXIT"
    ]

# --- Messages: general errors ---
SEQUENCE_NOT_LOADED: str = "The sequence {sequence_id} is not loaded."
UNKNOWN_ENZYME: str = "The enzyme {enzyme_name} is not available."

# --- Messages: LOAD_SEQUENCES ---
FILE_LOADED: str = "File {fasta_file} validated and loaded!"
FILE_ALREADY_LOADED: str = "File {fasta_file} already loaded!"
INVALID_BASES: str = "File {fasta_file} could not be loaded. Sequence {sequence_id} contains invalid nucleotides."
FILE_DUPLICATED = "File {fasta_file} could not be loaded. Sequence ID {sequence_id} is already in use."

# --- Messages: LIST_SEQUENCES ---
SEQUENCES_LOADED: str = "Number of sequences loaded: {num_sequences_loaded}"
LIST_SEQUENCES: str = "- {sequence_id} ({num_bases} bp)"
NOTHING_LOADED: str = "No sequences loaded."

# --- Messages: SEQUENCE_INFO ---
SEQUENCE_INFO: str = "Information about the sequence {sequence_id}:"
SEQUENCE_LENGTH: str = "- Length: {num_bases} bp."
SEQUENCE_BASES_COUNT: str = "- Base counts: A={A_count}, C={C_count}, G={G_count}, T={T_count}."
SEQUENCE_GC_CONTENT: str = "- GC content: {gc_percentage}%."

# --- Messages: FIND_SITES ---
RECOGNITION_SITES_NOT_FOUND: str = "The enzyme {enzyme_name} does not cut the sequence {sequence_id}."
RECOGNITION_SITES_FOUND: str = "Recognition sites of {enzyme_name} ({sequence}) in the sequence {sequence_id}:"
NUM_SITES_FOUND: str = "- Number of sites: {num_sites}."
POSITIONS_FOUND: str = "- Positions: {positions}."

# --- Messages: DIGEST ---
NO_FRAGS_PRODUCED: str = "The sequence {sequence_id} is not cut by the provided enzymes."
FRAGS_PRODUCED: str = "Digestion of the sequence {sequence_id} with {enzyme_names} produced the following fragments:"
LIST_FRAGS: str = "- {num_bases} bp (positions {start}-{end})"


# ------------------------------------
# 3. DATA CLASSES
# ------------------------------------
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


# ------------------------------------
# 4. LOADING DATA
# ------------------------------------

# --- Enzymes ---
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

# --- FASTA files ---
def load_fasta(fasta_file: str) -> str:
    """Loads fasta file and returns its content as a list of strings"""
    file_path = os.path.join(DATA_FOLDER, fasta_file)
    with open(file_path) as handle:
        fasta_data = handle.readlines()
    return fasta_data

# ------------------------------------
# 5. LOOKUP HELPERS
# ------------------------------------
def find_enzyme_in_repo(command_args: list[str], enzymes_repo: list[Enzyme]) -> bool:
    """Checks if an enzyme is in the enzymes repository"""
    enzymes_name_list: list[str] = []
    for enzyme in enzymes_repo:
        enzymes_name_list.append(enzyme.enzyme_name)

    # Checks if all enzymes in the command arguments are in the enzymes repository
    for arg in command_args[1:]:
        if arg not in enzymes_name_list:
            print(UNKNOWN_ENZYME.format(enzyme_name=arg))
            return False
    return True

def find_sequence_in_repo(command_args: list[str], sequences_repo: list[Sequence]) -> bool:
    """Checks if a sequence is in the sequences repository"""
    for seq in sequences_repo:
            if command_args[0] == seq.sequence_id:
                return True
    print(SEQUENCE_NOT_LOADED.format(sequence_id=command_args[0]))
    return False

def get_sequence(sequence_id: str, sequences_repo: list[Sequence]) -> str:
    """Returns the bases of the sequence with the given ID ("" if not found)"""
    sequence_to_look: str = ""
    for seq in sequences_repo:
        if sequence_id == seq.sequence_id:
            sequence_to_look = seq.sequence
    return sequence_to_look

def get_enzyme(enzyme_name: str, enzymes_repo: list[Enzyme]) -> Enzyme | None:
    """Returns the enzyme with the given name (None if not found)"""
    for enzyme in enzymes_repo:
        if enzyme_name == enzyme.enzyme_name:
            return enzyme
    return None


# ------------------------------------
# 6. ANALYSIS HELPERS
# ------------------------------------
def count_bases(sequence: str) -> int:
    """Counts the number of base pairs in a sequence"""
    return len(sequence)

def count_nucleotides_type(sequence: str) -> dict[str, int]:
    """Counts how many A, C, G and T a sequence has"""
    nucleotide_counts: dict[str, int] = {"A": 0, "C": 0, "G": 0, "T": 0}

    for nucleotide in sequence:
        nucleotide_counts[nucleotide] += 1
    return nucleotide_counts

def find_cut_positions(sequence_to_look: str, enzyme_recognition: str) -> list[int]:
    """Returns the 1-based positions where a recognition site starts in a sequence"""
    positions: list[int] = []
    start = sequence_to_look.find(enzyme_recognition)
    while start != -1:
        positions.append(start + 1)
        start = sequence_to_look.find(enzyme_recognition, start + 1)
    return positions

def alphabetic_sort(sequences_repo: list[Sequence]) -> list[Sequence]:
    """Returns the sequences sorted alphabetically by their ID"""
    sorted_sequences_repo: list[Sequence] = []
    sorted_names: list[str] = []
    temp_list: list[str] = []

    # Collects all sequence IDs and sorts them alphabetically
    for seq in sequences_repo:
        temp_list.append(seq.sequence_id)
    sorted_names = sorted(temp_list)

    # Appends the sequences to the sorted list in the order of the sorted IDs
    index: int = 0
    while len(sequences_repo) != len(sorted_sequences_repo):
        for seq in sequences_repo:
            if len(sequences_repo) != len(sorted_sequences_repo) and seq.sequence_id == sorted_names[index]:
                sorted_sequences_repo.append(seq)
                index += 1
    return sorted_sequences_repo

def valid_sequence(sequence: str) -> bool:
    """Checks if a sequence contains only valid nucleotides (A, C, G, T)"""
    for nucleotide in sequence:
        if nucleotide in VALID_BASES:
            continue
        else:
            return False
    return True

# ------------------------------------
# 7. COMMANDS
# ------------------------------------

# --- LOAD_SEQUENCES ---
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

        # Creates a set of already seen sequence IDs to check for duplicates
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

# --- LIST_SEQUENCES ---
def list_sequences(sequences_repo: list[Sequence]) -> None:
    """Lists all loaded sequences and their lengths (bps)"""
    # Validation
    if sequences_repo == []:
        print(NOTHING_LOADED)
        return

    # Output header and list of sequences
    print(SEQUENCES_LOADED.format(num_sequences_loaded= len(sequences_repo)))
    sorted_sequences_repo = alphabetic_sort(sequences_repo)
    for sequence in sorted_sequences_repo:
        print(LIST_SEQUENCES.format(sequence_id=sequence.sequence_id, num_bases=count_bases(sequence.sequence)))
    return

# --- SEQUENCE_INFO ---
def sequence_info(command_args: list[str], sequences_repo: list[Sequence]) -> None:
    """Prints the length, base counts and GC content of a sequence"""
    # Validation
    if not find_sequence_in_repo(command_args, sequences_repo):
        return

    sequence_to_look: str = get_sequence(command_args[0], sequences_repo)

    # Length
    print(SEQUENCE_INFO.format(sequence_id=command_args[0]))
    sequence_length = count_bases(sequence_to_look)
    print(SEQUENCE_LENGTH.format(num_bases = sequence_length))

    # Base counts
    nucleotide_counts = count_nucleotides_type(sequence_to_look)
    print(SEQUENCE_BASES_COUNT.format(A_count=nucleotide_counts["A"], C_count=nucleotide_counts["C"], G_count=nucleotide_counts["G"], T_count=nucleotide_counts["T"]))

    # GC content
    gc_content = ((nucleotide_counts["C"] + nucleotide_counts["G"]) * 100) / sequence_length
    print(SEQUENCE_GC_CONTENT.format(gc_percentage=round(gc_content, 2)))

# --- FIND_SITES ---
def find_sites(command_args: list[str], enzymes_repo: list[Enzyme], sequences_repo: list[Sequence]) -> None:
    """Finds the recognition sites of an enzyme in a sequence and prints the results"""
    # Validation
    if not find_sequence_in_repo(command_args, sequences_repo):
         return
    if not find_enzyme_in_repo(command_args, enzymes_repo):
         return

    sequence_to_look: str = get_sequence(command_args[0], sequences_repo)
    enzyme_recognition: str = get_enzyme(command_args[1], enzymes_repo).recognition_site

    # Search and report
    positions = find_cut_positions(sequence_to_look, enzyme_recognition)

    if positions == []:
         print(RECOGNITION_SITES_NOT_FOUND.format(enzyme_name=command_args[1], sequence_id=command_args[0]))
         return
    else:
        print(RECOGNITION_SITES_FOUND.format(enzyme_name=command_args[1], sequence= enzyme_recognition, sequence_id=command_args[0]))
        print(NUM_SITES_FOUND.format(num_sites=len(positions)))
        print(POSITIONS_FOUND.format(positions=str(positions).strip("[").strip("]")))
        return

# --- DIGEST ---
def digest_sequence(command_args: list[str], enzymes_repo: list[Enzyme], sequences_repo: list[Sequence]) -> None:
    """Cuts a sequence with one or more enzymes and prints the resulting fragments"""
    # Validation
    if not find_sequence_in_repo(command_args, sequences_repo):
        return
    if not find_enzyme_in_repo(command_args, enzymes_repo):
        return

    sequence_to_look: str = get_sequence(command_args[0], sequences_repo)

    # Finds all cut points for the given enzymes
    cut_points: list[int] = []

    for enzyme_name in command_args[1:]:
        enzyme = get_enzyme(enzyme_name, enzymes_repo)
        enzyme_recognition: str = enzyme.recognition_site
        enzyme_cut: int = int(enzyme.cut_offset)

        positions: list[int] = find_cut_positions(sequence_to_look, enzyme_recognition)
        for position in positions:
            cut_index: int = position + enzyme_cut - 1
            if 0 < cut_index < len(sequence_to_look) and cut_index not in cut_points:
                cut_points.append(cut_index)

    # If no cut points were found, the sequence is not cut by the provided enzymes
    if cut_points == []:
        print(NO_FRAGS_PRODUCED.format(sequence_id=command_args[0]))
        return

    # Cuts the sequence into fragments based on the cut points
    fragments: list[str] = []
    fragments_info: list[tuple[int]] = []
    start: int = 0
    cut_points.sort()

    for cut_index in cut_points:
        fragments.append(sequence_to_look[start:cut_index])
        fragments_info.append((start + 1, cut_index, len(sequence_to_look[start:cut_index])))
        start = cut_index
    fragments.append(sequence_to_look[start:])
    fragments_info.append((start + 1, start + len(sequence_to_look[start:]), len(sequence_to_look[start:])))

    # Sorts the fragments by length and then by start position
    gel = sorted(fragments_info, key=lambda frag: (-frag[2], frag[0]))

    print(FRAGS_PRODUCED.format(sequence_id=command_args[0],enzyme_names=", ".join(command_args[1:])))
    for f in gel:
        print(LIST_FRAGS.format(num_bases=f[2], start=f[0], end=f[1]))
    return


# ------------------------------------
# 8. COMMAND HANDLING
# ------------------------------------
def command_runner(command_name: str, command_args: list[str], enzymes_repo: list[Enzyme], fasta_repo: list[str], sequences_repo: list[Sequence]) -> None:
    """Runs the command based on the command name and arguments"""
    if command_name == "LOAD_SEQUENCES":
        load_sequences(command_args, sequences_repo, fasta_repo)
        return
    if command_name == "LIST_SEQUENCES":
        list_sequences(sequences_repo)
        return
    if command_name == "SEQUENCE_INFO":
        sequence_info(command_args, sequences_repo)
        return
    if command_name == "FIND_SITES":
        find_sites(command_args, enzymes_repo, sequences_repo)
        return
    if command_name == "DIGEST":
        digest_sequence(command_args, enzymes_repo, sequences_repo)
        return

def command_interpreter(user_input: str) -> list[str, list[str]]:
    """Interprets user input and returns command name and arguments"""
    command_parts: str = user_input.split(" ")
    command, args = command_parts[0] , command_parts[1:]
    return [command, args]

def command_input(enzymes_repo: list[Enzyme]) -> None:
    """Handles user input and command execution (main program loop)"""
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


# ------------------------------------
# 9. MAIN FUNCTION
# ------------------------------------
def main() -> None:
    """Main function to load enzymes and start command input"""
    # Load enzymes from the enzymes.txt file into the enzymes repository
    enzymes_repo: list[Enzyme] = []
    file_path = os.path.join(DATA_FOLDER, ENZYMES_FOLDER)
    with open(file_path) as handle:
        enzymes_data = handle.read()
    # Load enzymes into the repository
    load_enzymes(enzymes_data, enzymes_repo)
    # Start the command input loop
    command_input(enzymes_repo)

if __name__ == "__main__":
    main()