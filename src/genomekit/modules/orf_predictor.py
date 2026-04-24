def find_orfs(sequence: str):
    sequence = sequence.upper()
    orfs = []

    start = "ATG"
    stops = {"TAA", "TAG", "TGA"}

    for i in range(len(sequence) - 2):
        codon = sequence[i : i + 3]

        if codon == start:
            for j in range(i, len(sequence) - 2, 3):
                stop_codon = sequence[j : j + 3]
                if stop_codon in stops:
                    orfs.append(sequence[i : j + 3])
                    break

    return orfs
