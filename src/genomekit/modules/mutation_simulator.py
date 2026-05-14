import random

import numpy as np


class MutSimulater:
    """
    create mutations in a seq

    """

    nucleotides = ["A", "T", "G", "C"]

    def __init__(self, seq: str) -> None:
        """
        Initiates mut_simulation class
        Checks for empty input sequences and invalid characters
        """
        if not isinstance(seq, str) or len(seq) == 0:
            raise ValueError("Input sequence is empty")
        invalid = set(seq.upper()) - set(self.nucleotides)
        if invalid:
            raise ValueError(f"Invalid sequence character {invalid} identified")

        self.seq = list(seq.upper())

    def insertion(self, old_seq: list[str], pos: int) -> list[str]:
        """adds a base"""
        base = random.choice(self.nucleotides)
        return old_seq[:pos] + [base] + old_seq[pos:]

    def deletion(self, old_seq: list[str], pos: int) -> list[str]:
        """delete a base"""
        return old_seq[:pos] + old_seq[pos + 1 :]

    def substitution(self, old_seq: list[str], pos: int) -> list[str]:
        """substitutes nucleotides"""

        base = random.choice(self.nucleotides)
        while old_seq[pos] == base:
            base = random.choice(self.nucleotides)
        return old_seq[:pos] + [base] + old_seq[pos + 1 :]

    def mut_simulation(self, mutation_freq=0.01):
        old_seq = self.seq.copy()
        len_seq = len(old_seq)
        num_mutations = np.random.poisson(len_seq * mutation_freq)
        mutation_pos = []
        for _ in range(num_mutations):
            if len(old_seq) == 0:
                break
            position = random.randint(0, len(old_seq) - 1)
            mutations = ["insertion", "deletion", "substitution"]
            mutation = random.choice(mutations)
            mutation_pos.append((mutation, position))

            if mutation == "insertion":
                old_seq = self.insertion(old_seq, position)

            elif mutation == "deletion":
                old_seq = self.deletion(old_seq, position)

            elif mutation == "substitution":
                old_seq = self.substitution(old_seq, position)

        self.seq = old_seq

        return mutation_pos, old_seq
