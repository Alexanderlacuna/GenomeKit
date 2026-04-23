from __future__ import annotations


class Primer:
    """
    Analyse primer properties from a DNA sequence
    """

    def __init__(self, sequence: str) -> None:
        if len(sequence) < 20:
            raise ValueError("Sequence must be at least 20 bases to extract primers")
        self.sequence = sequence.upper()

    @classmethod
    def from_multiple(cls, sequences: list[str]) -> list[Primer]:
        return [cls(seq) for seq in sequences]

    def __str__(self) -> str:
        return self.sequence

    def __repr__(self) -> str:
        return self.__str__()

    def find_primer(self) -> Primer.PrimerFinderResults:
        """
        Check the first and last 20 bp for primer-like properties.
        Utilises 3 criteria
        1. Whether the gc content is between 40-60
        2. Whether the sequence can form an internal dime
        3. Whether the melting temperature is between 60-65c

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

        front_temp = self._melt_temp(front_seq)
        back_temp = self._melt_temp(back_seq)

        front_verdict = (40 <= front_gc <= 60) and not (front_hairpin) and (60 <= front_temp <= 65)
        back_verdict = (40 <= back_gc <= 60) and not (back_hairpin) and (60 <= back_temp <= 65)

        results = {
            "forward_primer": front_seq,
            "forward_verdict": front_verdict,
            "reverse_primer": back_seq,
            "reverse_verdict": back_verdict,
        }
        return self.PrimerFinderResults(results, factory=type(self))

    class PrimerFinderResults:
        def __init__(self, data_dict, factory):
            self.forward = data_dict["forward_primer"]
            self.for_verdict = data_dict["forward_verdict"]
            self.reverse = data_dict["reverse_primer"]
            self.rev_verdict = data_dict["reverse_verdict"]

        def __repr__(self):
            return (
                f"\n{'Primer Finder Results ':=^70}\n"
                f"Forward Primer Sequence: {self.forward} | Verdict: {self.for_verdict}\n"
                f"Backward Primer Sequence: {self.reverse} | Verdict: {self.rev_verdict}\n"
                f"{'=' * 70}"
            )

    def _gc_content(self, seq: str) -> float:
        """Return the GC content percentage of a sequence."""
        if len(seq) == 0:
            return 0.0
        return ((seq.count("G") + seq.count("C")) / len(seq)) * 100

    def _melt_temp(self, seq: str) -> float:
        if len(seq) == 0:
            return 0.0
        return 4 * (seq.count("G") + seq.count("C")) + 2 * (seq.count("A") + seq.count("T"))

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
