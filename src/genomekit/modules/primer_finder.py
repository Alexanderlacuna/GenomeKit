from __future__ import annotations

from typing import Any


class PrimerFinder:
    """Analyzes the 5' and 3' ends of a DNA sequence for primer suitability."""

    def __init__(self, sequence: str) -> None:
        if len(sequence) < 20:
            raise ValueError("Sequence must be at least 20 bases to extract primers")
        self.sequence = sequence.upper()

    def find(self) -> list[dict[str, Any]]:
        """
        Check the first and last 20 bp for primer-like properties.

        Returns:
            A list with one dictionary containing the forward/reverse
            primer sequences and their verdicts.
        """
        front_seq = self.sequence[:20]
        back_seq = self.sequence[-20:]

        front_gc = self._gc_content(front_seq)
        back_gc = self._gc_content(back_seq)

        front_hairpin = self._find_hairpin(front_seq)
        back_hairpin = self._find_hairpin(back_seq)

        front_verdict = 40 <= front_gc <= 60 and not front_hairpin
        back_verdict = 40 <= back_gc <= 60 and not back_hairpin

        return [
            {
                "forward_primer": front_seq,
                "forward_verdict": front_verdict,
                "reverse_primer": back_seq,
                "reverse_verdict": back_verdict,
            }
        ]

    def _gc_content(self, seq: str) -> float:
        """Return the GC content percentage of a sequence."""
        if len(seq) == 0:
            return 0.0
        return ((seq.count("G") + seq.count("C")) / len(seq)) * 100

    def _find_hairpin(self, seq: str) -> bool:
        """
        Check whether a sequence can form a hairpin
        (complementary base pairing within the same sequence).

        Args:
            seq: The sequence to check.

        Returns:
            True if a hairpin is found, False otherwise.
        """
        comp = {"A": "T", "T": "A", "G": "C", "C": "G"}
        for i in range(len(seq)):
            # j starts after a minimum loop of 3; stem length is 3
            for j in range(i + 6, len(seq) - 2):
                stem_a = seq[i : i + 3]
                stem_b = seq[j : j + 3]
                target = "".join(comp.get(base, "N") for base in stem_a)[::-1]
                if target == stem_b:
                    return True
        return False
