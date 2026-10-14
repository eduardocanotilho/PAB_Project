HEADER_MARK = ">"
VALID_BASES = "ACGT"
FILE_LOADED = "File {} validated and loaded!"
FILE_ALREADY_LOADED = "File {} already loaded"
INVALID_BASES = "File {} could not be loaded. Sequence {} contains invalid nucleotides."
FILE_DUPLICATED = "File {} could not be loaded. Sequence {} is already in use"

def file_fasta(lines: list[str]) -> list[Sequence]:
	sequences: list[Sequence] = []
	current_id = ""
	sequence_pieces: list[str] = []
    for line in lines:
        line = line.strip()
        if line == "":
                continue
        if line.startswith(HEADER_MARK):
                if current_id != "":
                        sequences.append(Sequence(current_id, "".join(sequence_pieces)))
                