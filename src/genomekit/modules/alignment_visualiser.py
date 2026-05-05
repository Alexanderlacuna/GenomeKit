def dotplot(seq1: str, seq2: str, filename: str = "user_dotplot.txt") -> None:
    """
    Generate and save a 2D grid showing regions of sequence similarity between two sequences.

    Args:
        seq1 (str): Sequence used for rows
        seq2 (str): Sequence used for columns
        filename (str): Name of the output text file
            Defaults to "dotplot.txt"

    Returns:
        None
    """

    with open(filename, "w") as f:
        f.write("  " + " ".join(seq2) + "\n")

        for i in range(len(seq1)):
            row = seq1[i] + " "
            for j in range(len(seq2)):
                if seq1[i] == seq2[j]:
                    row += ". "
                else:
                    row += "  "
            f.write(row + "\n")
